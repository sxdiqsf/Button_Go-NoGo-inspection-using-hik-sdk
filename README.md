# Button Go/No-Go Inspection System using HIK SDK

Industrial vision inspection system developed using Python, OpenCV, PyQt5, and HIK Vision Camera SDK for automated button inspection and Go/No-Go validation.

---

## Overview

This project is designed for real-time industrial inspection applications where buttons or circular components must be validated using machine vision techniques.

The system captures live images from a HIK Vision industrial camera, processes the image using OpenCV-based algorithms, and determines whether the inspected object passes or fails based on predefined conditions.

The application includes:
- Live camera acquisition
- Continuous image streaming
- ROI-based inspection
- Edge analysis
- Circle and feature detection
- Go/No-Go decision logic
- PyQt5 graphical interface
- HIK SDK camera integration

---

## Features

- Real-time industrial camera feed
- HIK Vision SDK integration
- PyQt5-based UI
- Continuous acquisition mode
- ROI (Region of Interest) inspection
- Edge-based analysis
- Circular feature detection
- Go/No-Go inspection logic
- Image processing using OpenCV
- Modular camera operation handling

---

## Technologies Used

- Python 3
- OpenCV
- PyQt5
- NumPy
- HIK Vision SDK (MvCameraControl)
- Industrial USB/GigE Camera

---

## Project Structure

```bash
Button_Go-NoGo-inspection-using-hik-sdk/
│
├── hik/                         # HIK SDK related files
├── dataset/                     # Sample datasets/images
│
├── BasicDemo.py                 # Main application
├── CamOperation_class.py        # Camera handling logic
├── PyUICBasicDemo.py            # Generated PyQt UI logic
├── PyUICBasicDemo.ui            # Qt Designer UI file
│
├── requirements.txt
├── README.md
└── .gitignore
