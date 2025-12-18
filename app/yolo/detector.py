# app/yolo/detector.py
from ultralytics import YOLO
import torch
from app.utils.format import to_unified

model = YOLO("app/models/yolo/yolov8n-pose.pt")

def detect(image_bgr):
    results = model(image_bgr, conf=0.3)[0]
    h, w = image_bgr.shape[:2]
    poses = []
    if results.keypoints is not None:
        xy = results.keypoints.xy.cpu().numpy()
        conf = results.keypoints.conf.cpu().numpy()
        for xys, cfs in zip(xy, conf):
            kpts = [(float(x), float(y)) for x, y in xys[:17]]
            poses.append((kpts, cfs[:17].tolist()))
    return to_unified(poses, w, h)