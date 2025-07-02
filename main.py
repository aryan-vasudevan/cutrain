import cv2

capture = cv2.VideoCapture(0)

while True:
    # Get and display the frame
    ret, frame = capture.read()
    cv2.imshow('Live Camera Feed', frame)

    # End the footage if "q" pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close the capture
cv2.destroyAllWindows()
