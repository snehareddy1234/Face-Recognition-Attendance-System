import streamlit as st
import pandas as pd
import os

def view_attendance():
    st.title("View Attendance Records")
    
    if not os.path.exists("attendance"):
        st.warning("No attendance records found")
        return
    
    subjects = [d for d in os.listdir("attendance") if os.path.isdir(f"attendance/{d}")]
    if not subjects:
        st.warning("No subjects found")
        return
    
    subject = st.selectbox("Select Subject", subjects)
    files = os.listdir(f"attendance/{subject}")
    
    if not files:
        st.warning(f"No attendance files for {subject}")
        return
    
    selected_file = st.selectbox("Select Date", files)
    df = pd.read_csv(f"attendance/{subject}/{selected_file}")
    
    st.dataframe(df)
    
    # Calculate statistics
    total_students = len(df)
    st.metric("Total Students Present", total_students)

view_attendance()
