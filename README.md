# Footfall Counter

A minimal web-based footfall counting system using Flask and OpenCV. Users can upload a video, manually provide line coordinates, and get the number of people crossing the line. The processed video with marked line and counts is returned.

---

## Features

- Upload video files via web interface.
- Enter line coordinates manually (X1, Y1, X2, Y2).
- Automatic detection of line orientation (vertical/horizontal) based on coordinates.
- Outputs processed video and in/out counts.
- Minimal setup, runs locally in a Flask server.

---

## Folder Structure

footfall_counter/
├─ app.py 
├─ main.py 
├─ templates/
│ └─ index.html 
├─ static/
│ ├─ uploads/ 
│ └─ outputs/ 
├─ requirements.txt 
└─ README.md 

----