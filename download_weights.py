import os
import urllib.request
from pathlib import Path

BASE = Path("app/models")
BASE.mkdir(parents=True, exist_ok=True)

urls = {
    "mediapipe/pose_landmarker_full.task":
        "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_full/float16/1/pose_landmarker_full.task",

    "yolo/yolov8n-pose.pt":
        "https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n-pose.pt",

    "roboflow/best.pt":
        "https://your-roboflow-project-url/direct-download-link",   # ← CHANGE THIS

    "mmpose/hrnet_w48_coco_384x288.pth":
        "https://download.openmmlab.com/mmpose/top_down/hrnet/hrnet_w48_coco_384x288-314c8526_20210722.pth",

    "posenet/posenet.tflite":
        "https://storage.googleapis.com/tfjs-models/savedmodel/posenet/mobilenet/float/075/model-stride16.json",  # we only need .tflite part (converted)
}

print("Downloading weights...\n")
for path, url in urls.items():
    full_path = BASE / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    if not full_path.exists():
        print(f"→ {path}")
        urllib.request.urlretrieve(url, full_path)
    else:
        print(f"✓ {path} (already exists)")

print("\nAll weights ready! Run: python -m app.main")