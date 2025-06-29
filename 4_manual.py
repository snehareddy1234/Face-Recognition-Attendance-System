import streamlit as st
import pandas as pd
import datetime
import os

def manual_entry():
    st.title("Manual Attendance Entry")
    
    subject = st.text_input("Subject Name")
    if not subject:
        st.warning("Please enter subject name")
        return
    
    enrollment = st.text_input("Enrollment Number")
    name = st.text_input("Student Name")
    
    if st.button("Add to Attendance"):
        if not enrollment or not name:
            st.error("Please enter both fields")
            return
            
        # Create or append to CSV
        filename = f"manual_attendance/{subject}.csv"
        os.makedirs("manual_attendance", exist_ok=True)
        
        if os.path.exists(filename):
            df = pd.read_csv(filename)
        else:
            df = pd.DataFrame(columns=["Enrollment", "Name", "Date", "Time"])
        
        new_entry = {
            "Enrollment": enrollment,
            "Name": name,
            "Date": datetime.date.today().strftime("%Y-%m-%d"),
            "Time": datetime.datetime.now().strftime("%H:%M:%S")
        }
        
        df = df.append(new_entry, ignore_index=True)
        df.to_csv(filename, index=False)
        st.success(f"Added {name} to {subject} attendance")

manual_entry()
