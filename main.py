import os
import threading
import time
import argparse
import cv2
import numpy as np
import serial
from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_resize


def get_size(file_path):
    # Load the video clip
    clip = VideoFileClip(file_path)

    # Get the width and height of the video
    original_width, original_height = clip.size

    # Calculate the aspect ratio
    aspect_ratio = original_width / original_height

    # Calculate the new dimensions while maintaining the aspect ratio
    if original_width > original_height:
        width = 16
        height = round(width / aspect_ratio)
    else:
        height = 16
        width = round(height * aspect_ratio)

    # Ensure the dimensions are even numbers
    width -= width % 2
    height -= height % 2

    # Close the clip
    clip.close()

    return width, height


def resize_video(input_file, output_file, size):
    if os.path.exists(output_file):
        os.remove(output_file)
    ffmpeg_resize(input_file, output_file, size)


def process_frame(frame):
    # Display the frame
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    map_lambda = lambda x: 1 if x > 127 else 0
    map_vectorized = np.vectorize(map_lambda)
    mapped_grey = map_vectorized(grey)

    bars = np.zeros((int((16 - mapped_grey.shape[0]) / 2), 16))

    grey16x16 = np.vstack([bars, mapped_grey, bars]).astype(int)

    frame_bytes = bytes(np.packbits(grey16x16))

    return frame_bytes


def play_video(video_file, serial_port):
    # Create a VideoCapture object
    cap = cv2.VideoCapture(video_file)
    try:
        ser = serial.Serial(serial_port)
    except serial.SerialException:
        raise Exception("Error opening serial port")

    # Check if video opened successfully
    if not cap.isOpened():
        raise Exception("Error opening video file")

    # Read until the video is completed
    while cap.isOpened():
        # Capture frame-by-frame
        start = time.time()
        ret, frame = cap.read()
        if ret:
            # Get the processed frame bytes
            frame_bytes = process_frame(frame)

            # Write the processed frame to the serial port
            ser.write(frame_bytes)

            frame_time = 1 / 30 - (time.time() - start)
            if frame_time > 0:
                time.sleep(frame_time)
        else:
            break

    # Release the VideoCapture object
    cap.release()


# Create the parser
parser = argparse.ArgumentParser(description="Process some integers.")

# Add the arguments
parser.add_argument('--input', type=str, help='The input file')
parser.add_argument('--output', type=str, help='The output file', default='output.mp4')
parser.add_argument('--port', type=str, help='The serial port')

# Parse the arguments
args = parser.parse_args()

serial_port = args.port
input_file = args.input
output_file = args.output

if not os.path.exists(input_file):
    raise Exception("Input file does not exist")

width, height = get_size(input_file)
size = (width, height)
resize_video(input_file, output_file, size)
while True:
    try:
        play_video(output_file, serial_port)
    except Exception as e:
        print(e)
        break
