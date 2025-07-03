import cv2
import os

def beep():
    os.system('say "alert"')

def display_feedback(correct_posture: bool, frame):
    if correct_posture:
        cv2.putText(frame, "Keep going!", (30, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1.2, (0, 255, 0), 3, cv2.LINE_AA)
    else:
        cv2.putText(frame, "Fix posture!", (30, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1.2, (0, 0, 255), 3, cv2.LINE_AA)
        beep()
