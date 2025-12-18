# app/utils/formatter.py

COCO17 = [
    "nose", "left_eye", "right_eye", "left_ear", "right_ear",
    "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
    "left_wrist", "right_wrist", "left_hip", "right_hip",
    "left_knee", "right_knee", "left_ankle", "right_ankle"
]

def to_unified(poses_list, img_w, img_h):
    result = []
    for idx, (kpts, confs) in enumerate(poses_list):
        keypoints = []
        total_score = 0
        count = 0
        for i, name in enumerate(COCO17):
            x, y = kpts[i]
            score = confs[i]
            keypoints.append({
                "name": name,
                "position": {"x": round(x, 2), "y": round(y, 2)},
                "score": round(score, 4)
            })
            total_score += score
            count += 1
        avg_score = total_score / count if count > 0 else 0
        result.append({
            "pose_id": idx + 1,
            "score": round(avg_score, 4),
            "keypoints": keypoints
        })
    return result