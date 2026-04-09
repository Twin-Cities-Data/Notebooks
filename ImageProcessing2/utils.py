import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import os

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import drawing_utils, drawing_styles

# this function takes an mp4 and returns evenly sampeled frames. 

def sample_frames_from_mp4(path, n_frames):

    cap = cv2.VideoCapture(path)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    indices = np.linspace(0,total_frames - 1,n_frames,dtype=int)

    frames = []

    i = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        if i in indices:
            framergb=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            frames.append(framergb)

        i += 1

    cap.release()

    return np.array(frames)


def plot_frames(frames, cols=4, figsize=(15,8)):
    
    n = len(frames)

    rows = math.ceil(n / cols)

    plt.figure(figsize=figsize)

    for i in range(n):

        plt.subplot(rows, cols, i+1)

        plt.imshow(frames[i])

        plt.axis("off")

    plt.tight_layout()

    plt.show()

def get_frame_count(path):
    cap = cv2.VideoCapture(path)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    cap.release()
    
    return total_frames  

def get_fps(path):
    
    cap = cv2.VideoCapture(path)

    fps = int(cap.get(cv2.CAP_PROP_FPS))

    cap.release()
    
    return fps

def write_temp_images_for_llm(frames,foldername="temp_frames"):
    folder = foldername
    os.makedirs(folder, exist_ok=True)

    # delete old files
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)

        if os.path.isfile(path):
            try:
                os.remove(path)
            except OSError:
                pass

    image_paths = []

    for i, frame in enumerate(frames):
        path = os.path.join(folder, f"frame_{i}.png")

        # convert RGB back to BGR for cv2.imwrite
        cv2.imwrite(path, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

        image_paths.append(path)

    return image_paths

def annotate_image(rgb_image, detector):

  mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
  detection_result = detector.detect(mp_image)
  pose_landmarks_list = detection_result.pose_landmarks
  annotated_image = np.copy(rgb_image)

  #a little different from last go
  red_lines = drawing_utils.DrawingSpec(color=(255, 0, 0), thickness=3)   # RGB red
  red_points = drawing_utils.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2)

  for pose_landmarks in pose_landmarks_list:
    drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=pose_landmarks,
        connections=vision.PoseLandmarksConnections.POSE_LANDMARKS,
        landmark_drawing_spec=red_points,
        connection_drawing_spec=red_lines)

  return annotated_image,pose_landmarks_list

def pose_overlays_from_frames(frames,detector):
    overlays_rgb = []
    
    for frame in frames:
        annotated,data=annotate_image(frame,detector)
        overlays_rgb.append(annotated)

    return overlays_rgb


LANDMARK_NAMES = {
    0: "nose",
    1: "left_eye_inner",
    2: "left_eye",
    3: "left_eye_outer",
    4: "right_eye_inner",
    5: "right_eye",
    6: "right_eye_outer",
    7: "left_ear",
    8: "right_ear",
    9: "mouth_left",
    10: "mouth_right",
    11: "left_shoulder",
    12: "right_shoulder",
    13: "left_elbow",
    14: "right_elbow",
    15: "left_wrist",
    16: "right_wrist",
    17: "left_pinky",
    18: "right_pinky",
    19: "left_index",
    20: "right_index",
    21: "left_thumb",
    22: "right_thumb",
    23: "left_hip",
    24: "right_hip",
    25: "left_knee",
    26: "right_knee",
    27: "left_ankle",
    28: "right_ankle",
    29: "left_heel",
    30: "right_heel",
    31: "left_foot_index",
    32: "right_foot_index",
}