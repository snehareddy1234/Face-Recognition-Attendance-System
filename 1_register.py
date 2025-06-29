import streamlit as st
import cv2
import os
import numpy as np
from PIL import Image
import pandas as pd
import urllib.request

def ensure_haarcascade():
    # Download Haar Cascade if not exists
    if not os.path.exists('haarcascade_frontalface_default.xml'):
        url = 'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml'
        urllib.request.urlretrieve(url, 'haarcascade_frontalface_default.xml')
        st.success("Downloaded Haar Cascade file")

def register_student():
    ensure_haarcascade()
    st.title("Student Registration")
    
    col1, col2 = st.columns(2)
    with col1:
        enrollment = st.text_input("Enrollment Number")
    with col2:
        name = st.text_input("Student Name")
    
    if st.button("Take Images"):
        if not enrollment or not name:
            st.error("Please enter both enrollment number and name")
            return
            
        # Check if Haar Cascade file exists
        if not os.path.exists('haarcascade_frontalface_default.xml'):
            st.error("Haar Cascade file not found. Please try again.")
            return

        # Initialize camera and face detector
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        cam = cv2.VideoCapture(0)
        
        if not cam.isOpened():
            st.error("Could not open camera")
            return

        # Create necessary directories
        os.makedirs('dataset', exist_ok=True)
        os.makedirs('StudentDetails', exist_ok=True)
        
        img_count = 0
        st.warning("Taking images... Look at the camera")
        image_placeholder = st.empty()
        
        try:
            while img_count < 50:
                ret, frame = cam.read()
                if not ret:
                    st.error("Failed to capture image from camera")
                    break
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                
                for (x,y,w,h) in faces:
                    cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
                    img_count += 1
                    cv2.imwrite(f"dataset/{name}_{enrollment}_{img_count}.jpg", gray[y:y+h,x:x+w])
                
                image_placeholder.image(frame, channels="BGR")
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            if img_count == 0:
                st.error("No faces detected. Please try again with proper lighting.")
            else:
                # Save student details
                student_file = "StudentDetails/student_details.csv"
                if not os.path.exists(student_file):
                    pd.DataFrame(columns=['Enrollment', 'Name']).to_csv(student_file, index=False)
                
                df = pd.read_csv(student_file)
                df = pd.concat([df, pd.DataFrame({'Enrollment': [enrollment], 'Name': [name]})])
                df.drop_duplicates(subset=['Enrollment'], keep='first', inplace=True)
                df.to_csv(student_file, index=False)
                
                st.success(f"Successfully captured {img_count} images of {name}")

        finally:
            cam.release()
            cv2.destroyAllWindows()

    if st.button("Train Model"):
        train_model()

def train_model():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces = []
    ids = []

    if not os.path.exists('dataset'):
        st.error("No dataset found to train. Please capture images first.")
        return

    try:
        for image_name in os.listdir('dataset'):
            if image_name.endswith('.jpg'):
                img_path = os.path.join('dataset', image_name)
                img = Image.open(img_path).convert('L')
                img_np = np.array(img, 'uint8')
                
                # Extract ID from filename (assuming format: name_enrollment_number.jpg)
                enrollment = int(image_name.split('_')[1])
                
                faces.append(img_np)
                ids.append(enrollment)

        if len(faces) == 0:
            st.error("No valid images found in dataset. Please recapture images.")
            return
            
        recognizer.train(faces, np.array(ids))
        os.makedirs('trainer', exist_ok=True)
        recognizer.save('trainer/trainer.yml')
        st.success("Model trained successfully!")
        
    except Exception as e:
        st.error(f"Error during training: {str(e)}")

if __name__ == '__main__':
    register_student()
