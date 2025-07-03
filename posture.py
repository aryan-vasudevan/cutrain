import math
from typing import List, Dict, Tuple

def finger_tilt_angle(J: Tuple[float, float], T: Tuple[float, float]) -> float:
    """
    Angle between the joint→tip vector and vertical axis.
    0° = perfectly vertical; 90° = perfectly horizontal.
    """
    dx, dy = T[0] - J[0], T[1] - J[1]
    return math.degrees(math.atan2(abs(dx), abs(dy)))

def is_posture_correct(predictions: List[Dict]) -> bool:
    """
    Returns True if at least 3 out of 5 fingers on the LEFT hand
    have tilt <= TILT_THRESHOLD (i.e. are sufficiently vertical/curled).
    """
    if not predictions:
        return False

    # 1) Pick the left-hand detection
    left = [d for d in predictions if d.get("class") == "left hand"]
    if not left:
        return False
    hand = max(left, key=lambda d: d["confidence"])

    # 2) Map keypoints
    kps = {kp["class"]:(kp["x"], kp["y"]) for kp in hand["keypoints"]}

    # 3) Ensure we have all five knuckles & tips
    for i in range(1,6):
        if f"j{i}" not in kps or f"t{i}" not in kps:
            return False

    # 4) Compute tilt for each finger
    tilts = [
        finger_tilt_angle(kps[f"j{i}"], kps[f"t{i}"])
        for i in range(1,6)
    ]

    # 5) Count how many are near‑vertical
    TILT_THRESHOLD = 30.0  # degrees from vertical
    near_vertical = sum(1 for angle in tilts if angle <= TILT_THRESHOLD)

    # 6) Posture is correct if ≥3 fingers are near‑vertical
    return near_vertical >= 3