import math
import statistics

def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def is_posture_correct(predictions):
    
    # Labels for everything
    hand = max(predictions, key=lambda d: d["confidence"])
    kps  = {kp["class"]: (kp["x"], kp["y"]) for kp in hand["keypoints"]}

    w   = kps["w"]
    j1, t1 = kps["j1"], kps["t1"]
    j2, t2 = kps["j2"], kps["t2"]
    j3     = kps["j3"]
    j4, t4 = kps["j4"], kps["t4"]
    j5, t5 = kps["j5"], kps["t5"]
    
    # Palm angle relative to horizontal
    dx, dy     = j3[0] - w[0], j3[1] - w[1]
    palm_angle = abs(math.degrees(math.atan2(dy, dx)))

    # Extension ratios for thumb & index only
    ext_thumb = distance(t1, j1) / max(distance(j1, w), 1e-6)
    ext_index = distance(t2, j2) / max(distance(j2, w), 1e-6)

    # Grip openness (thumb to index)
    grip = distance(t1, t2)

    # Spread std dev (gpt)
    joints = [j1, j2, j3, j4, j5]
    angles = [math.degrees(math.atan2(j[1]-w[1], j[0]-w[0])) for j in joints]
    spread_std = statistics.pstdev(angles)

    # Updated thresholds (gpt)
    palm_ok      = 30 < palm_angle < 150
    extension_ok = 0.7 < ext_thumb < 1.3 and 0.7 < ext_index < 1.3
    grip_ok      = 50 < grip < 130
    spread_ok    = spread_std < 60

    return palm_ok and extension_ok and grip_ok and spread_ok