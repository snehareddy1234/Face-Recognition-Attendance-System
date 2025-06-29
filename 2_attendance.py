import streamlit as st
import cv2
import numpy as np
import pandas as pd
import time
from datetime import datetime
import os

def take_attendance():
    st.title("📝 Take Attendance")
    
    # Initialize session state for tracking
    if 'attendance_started' not in st.session_state:
        st.session_state.attendance_started = False
    if 'recognized_students' not in st.session_state:
        st.session_state.recognized_students = {}
    if 'final_attendance' not in st.session_state:
        st.session_state.final_attendance = []

    subject = st.text_input("Enter Subject Name", key="subject_name")
    
    if st.button("Start Attendance") and subject:
        st.session_state.attendance_started = True
        st.session_state.recognized_students = {}
        st.session_state.final_attendance = []
        st.success(f"Attendance started for {subject}")

    if st.button("Stop Attendance"):
        st.session_state.attendance_started = False
        save_attendance(subject)
        return

    if st.session_state.attendance_started:
        process_attendance(subject)

def process_attendance(subject):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    try:
        recognizer.read("trainer/trainer.yml")
    except:
        st.error("Model not found. Please train the model first.")
        return

    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    
    try:
        student_df = pd.read_csv("StudentDetails/student_details.csv")
    except:
        st.error("Student details not found. Please register students first.")
        return

    cam = cv2.VideoCapture(0)
    stframe = st.empty()
    message = st.empty()

    while st.session_state.attendance_started:
        ret, frame = cam.read()
        if not ret:
            st.error("Failed to capture frame")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

            if confidence < 70:  # Lower confidence = better match
                student_info = student_df[student_df['Enrollment'] == id]
                if not student_info.empty:
                    enrollment = student_info['Enrollment'].values[0]
                    name = student_info['Name'].values[0]

                    if enrollment not in st.session_state.recognized_students:
                        st.session_state.recognized_students[enrollment] = {
                            "name": name,
                            "timestamp": datetime.now().strftime("%H:%M:%S")
                        }
                        message.success(f"✅ Recognized: {name} ({enrollment})")

                    cv2.putText(frame, name, (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 
                               0.8, (255,255,255), 2)

        stframe.image(frame, channels="BGR", use_column_width=True)
        time.sleep(0.1)  # Reduce CPU usage

    cam.release()
    cv2.destroyAllWindows()

def save_attendance(subject):
    if not st.session_state.recognized_students:
        st.warning("No students recognized during this session")
        return

    attendance_list = [{
        "Enrollment": enrollment,
        "Name": data["name"],
        "Time": data["timestamp"],
        "Date": datetime.now().strftime("%Y-%m-%d")
    } for enrollment, data in st.session_state.recognized_students.items()]

    attendance_df = pd.DataFrame(attendance_list)
    
    # Create directory if not exists
    os.makedirs(f"Attendance/{subject}", exist_ok=True)
    
    # Save with date in filename
    filename = f"Attendance/{subject}/attendance_{datetime.now().strftime('%Y%m%d')}.csv"
    attendance_df.to_csv(filename, index=False)
    
    st.success(f"Attendance saved for {len(attendance_list)} students")
    st.dataframe(attendance_df)

if __name__ == '__main__':
    take_attendance()
