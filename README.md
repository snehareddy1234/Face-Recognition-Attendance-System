 Attendance Management System

A facial recognition-based attendance tracking system built with Streamlit and OpenCV.

## Features
- Student registration with face capture
- Real-time attendance tracking
- Attendance record viewing
- Manual attendance entry
- Camera testing

## Installation
1. Clone this repository
2. Install requirements:
   ```bash
   pip install -r requirements.txt

   Folder Structure:
   attendance-system/
├── .streamlit/
│   └── config.toml
├── assets/
│   ├── logo.jpg         # Your logo/image
│   └── haarcascade_frontalface_default.xml  # Haar Cascade file
├── pages/
│   ├── 1_register.py     # Student registration
│   ├── 2_attendance.py  # Take attendance
│   ├── 3_view.py        # View attendance records
│   ├── 4_manual.py       # Manual attendance entry
│   └── 5_test.py        # Camera test
├── dataset/             # Auto-created: Stores student face images
├── trainer/             # Auto-created: Stores trained model (trainer.yml)
├── StudentDetails/       # Auto-created: Stores student_details.csv
├── Attendance/           # Auto-created: Stores attendance records
├── manual_attendance/    # Auto-created: Stores manual attendance records
├── main.py               # Main Streamlit app
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
