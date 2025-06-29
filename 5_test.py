import streamlit as st
import cv2

def test_camera():
    st.title("Camera Test")
    
    cam = cv2.VideoCapture(0)
    st.warning("Testing camera feed. Press 'Stop' when done.")
    
    image_placeholder = st.empty()
    stop_button = st.button("Stop Camera")
    
    while not stop_button:
        ret, frame = cam.read()
        if ret:
            image_placeholder.image(frame, channels="BGR")
        else:
            st.error("Failed to access camera")
            break
    
    cam.release()
    st.success("Camera test completed")

test_camera()
