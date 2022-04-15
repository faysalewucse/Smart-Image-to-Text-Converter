import cv2
import time


def take():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Take Picture to Convert")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("Take Picture to Convert", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed
            img_name = "opencv_frame_{}.png".format(round(time.time() * 1000))
            cv2.imwrite(img_name, frame)
            return img_name

    cam.release()

    cv2.destroyAllWindows()