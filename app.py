import asyncio
import sys

if sys.platform.startswith('win') and sys.version_info >= (3, 8):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av
import cv2
from pose.bench import Bench

class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.detector = Bench()

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        result_img = self.detector.track_bench(img)
        return av.VideoFrame.from_ndarray(result_img, format="bgr24")

st.title("🏋️ 即時臥推姿勢偵測器 + Reps 計數")
webrtc_streamer(key="bench-press", video_processor_factory=VideoProcessor)
