import pathlib

import cv2


def FrameCapture(path):
    vidObj = cv2.VideoCapture(path)
    frames_dir = pathlib.Path("") / "frames"
    frames_dir.mkdir(exist_ok=True)
    count = 0

    success = 1

    while success:
        success, image = vidObj.read()

        cv2.imwrite(str(frames_dir / f"frame{count}.jpg"), image)

        count += 1


if __name__ == '__main__':
    FrameCapture("bad_apple.mp4")
