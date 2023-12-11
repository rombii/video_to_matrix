from moviepy.video.io.ffmpeg_tools import ffmpeg_resize
import sys


def resize_video(input_file, output_file, size):
    ffmpeg_resize(input_file, output_file, size)



import cv2
import numpy as np
import serial


def play_video(video_file):
    # Create a VideoCapture object
    cap = cv2.VideoCapture(video_file)
    ser = serial.Serial('COM3')

    # Check if video opened successfully
    if not cap.isOpened():
        print("Error opening video file")
        return

    # Read until the video is completed
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret:
            # Display the frame
            grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # cv2.imshow("Frame", grey)
            map_lambda = lambda x: 1 if x > grey.mean() else 0
            map_vectorized = np.vectorize(map_lambda)
            mapped_grey = map_vectorized(grey)

            bars = np.zeros((2, 16))

            grey16x16 = np.vstack([bars, mapped_grey, bars]).astype(int)

            frame_bytes = bytes(np.packbits(grey16x16))

            ser.write(frame_bytes)

            # Press Q on keyboard to exit
            if cv2.waitKey(25) == ord('q'):
                break
        else:
            break

    # Release the VideoCapture object
    cap.release()

    # Close all the frames
    cv2.destroyAllWindows()


input_file = 'input.mp4'
output_file = 'output1612.mp4'
size = (int(16), int(12))
# resize_video(input_file, output_file, size)
play_video(output_file)
