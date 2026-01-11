# Pill Pal | Medication Adherence System 🏥

Pill Pal is an end-to-end hardware-software integration designed to improve patient medication compliance. The system uses computer vision logic to detect medication usage and reports data to a caregiver dashboard.

**🚀 The Tech Stack**

Backend Logic: Python

Hardware (Camera Module): ESP32-CAM

Image Processing: OpenCV (cv2), NumPy

GUI Framework: Tkinter

Communication: HTTP image capture (ESP32 web server)

UX Design: Figma

**🛠️ System Architecture**

Detection Layer (ESP32-CAM): The ESP32-CAM continuously hosts a small HTTP server that gives image captures from live footage.

Vision Processing Layer (Python): Python program continuously requests images from the ESP32-CAM IP address. A constant rolling buffer of images is maintained, and ‘pills taken’/motion detected is identified by checking for significant pixel change using Open CV.

Application Layer (Python): A multi-threaded dashboard listens for incoming signals, processes the event, updates the UI state in real-time, and persists the data to an audit log.

**⚡ Features**

Real-time Monitoring: Immediate UI feedback (Red/Green state) upon medication detection.

Automatic Reset: State-tracking logic that resets medication status daily.

Audit Logging: Time-stamped persistence of all medication events for caregiver review.

Multi-threaded Execution: Background image polling requests and image processing run in a separate thread ensuring the GUI remains responsive.
