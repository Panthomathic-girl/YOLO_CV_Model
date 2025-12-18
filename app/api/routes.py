# app/api/routes.py
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import cv2
import tempfile
import os

from ..yolo.detector import detect as yolo_detect

router = APIRouter()

@router.post("/pose/yolo")
async def pose_yolo(file: UploadFile = File(...)):
    # Validate it's a video
    if not file.content_type.startswith("video/") and not file.filename.lower().endswith(('.mp4', '.mov', '.avi', '.webm')):
        return {"error": "Please upload a video file"}

    # Save uploaded video to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        cap = cv2.VideoCapture(tmp_path)
        if not cap.isOpened():
            return {"error": "Invalid video file"}

        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0

        all_frame_results = []

        frame_idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Run YOLO pose detection on this frame
            poses = yolo_detect(frame)

            # Optional: add timestamp in seconds
            timestamp = round(frame_idx / fps, 2) if fps > 0 else 0

            all_frame_results.append({
                "frame_number": frame_idx,
                "timestamp_sec": timestamp,
                "num_poses": len(poses),
                "poses": poses
            })

            frame_idx += 1

        cap.release()

        return JSONResponse(content={
            "video_info": {
                "total_frames": total_frames,
                "duration_sec": round(duration, 2),
                "fps": round(fps, 2)
            },
            "frames": all_frame_results
        })

    finally:
        # Always clean up the temp file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)