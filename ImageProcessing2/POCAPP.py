
# MediaPipe for pose detection and overlay generation, Ollama for LLM critique,
# Streamlit for the web app interface
# Pydantic for defining the output schema of the critique.
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import drawing_utils, drawing_styles

from utils import *
import ollama
import streamlit as st
from pydantic import BaseModel, Field

import time
import tempfile
import os
############################################################
# Define the output schema for the critique using Pydantic
############################################################
class ThrowCritique(BaseModel):
    score: int = Field(ge=1, le=10)
    feedback: str = Field(
        description="Brief coaching feedback in 2-4 sentences."
    )




############################################################
# Setup MediaPipe Pose Landmarker
############################################################
MODEL_PATH = "pose_landmarker.task"

base_options = python.BaseOptions(model_asset_path=MODEL_PATH)

options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    min_pose_detection_confidence=0.1,
    min_pose_presence_confidence=0.1,
    min_tracking_confidence=0.1
)
detector = vision.PoseLandmarker.create_from_options(options)


############################################################
# Set prompt for the LLM critique
############################################################

throwprompt = """
You are an elite Olympic discus coach and biomechanist.

You have been given a sequence of images showing a complete discus throw from beginning to end.

Evaluate the thrower's technique using these criteria:
- balance and posture
- rotation mechanics
- footwork
- hip and shoulder separation
- release position
- follow-through

Be strict but fair. Rate the throw from 1-10 where:
1 = very poor form
5 = average high school athlete
8 = strong collegiate athlete
10 = world class technique

Give 2-4 sentences of specific, actionable feedback.
"""


############################################################
# Critique function that sends images and prompt to the LLM and parses the response
############################################################

def critique_throw(image_paths: list,
                   mod: str = "llava:7b",
                   prompt: str = throwprompt,  
                   temp: float = 0.0):
    
    resp = ollama.chat(
        model=mod,
        messages=[
            {
                "role": "system",
                "content": prompt,
                "images": image_paths
            }
        ],
        format=ThrowCritique.model_json_schema(),
        options={"temperature": temp}
    )

    raw = resp["message"]["content"]
    return ThrowCritique.model_validate_json(raw)


############################################################
# Streamlit app layout
############################################################
st.header("AI Coach Protoype")
right_col, left_col = st.columns(2)

with right_col:

    uploaded_file = st.file_uploader(
        "Drag and drop an MP4 file here",
        type=["mp4"],
    )
    if uploaded_file is not None:
        
        st.video(uploaded_file,width=200)

with left_col:
    st.header("Get Feedback on Your Throw")
    if st.button("Run Analysis"):
        
        if uploaded_file is None:
            st.warning("Upload an MP4 first.")
            st.stop()

        progress_bar = st.progress(0,text="Turning video into frames...")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            tmp.write(uploaded_file.getbuffer())
            video_path = tmp.name

        try:
            time.sleep(1)
            frames = sample_frames_from_mp4(video_path,18)
            progress_bar.progress(25,text="Generating pose overlays...")
            time.sleep(1)
            overs=pose_overlays_from_frames(frames,detector)
            progress_bar.progress(50,text="Writing temporary images for AI Coach...")
            time.sleep(1)
            img_paths=write_temp_images_for_llm(overs)
            progress_bar.progress(75,text="AI Coach is thinking now..")
            crit=critique_throw(image_paths=img_paths,mod='gemma4:e4b',prompt=throwprompt )
            progress_bar.progress(100,text="Done!")
            st.write(crit)
        
        finally:
            if os.path.exists(video_path):
                os.remove(video_path)