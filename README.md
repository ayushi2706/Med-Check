# Med-Check | Medication Adherence System 🏥

MedSentry is an end-to-end hardware-software integration designed to improve patient medication compliance. The system uses computer vision logic to detect medication usage and reports data to a caregiver dashboard.

**🚀 The Tech Stack
**
Backend Logic: Python

Hardware Interface: C++ (ESP32-CAM)

GUI Framework: Tkinter

Communication: Serial Protocol (via pyserial)

UX Design: Figma

**🛠️ System Architecture
**
Detection Layer (C++): An ESP32-CAM monitors the medication station. When pixels change, motion is detected, and a signal is triggered.

Integration Layer (Serial): The hardware sends an asynchronous interrupt signal (MOTION_DETECTED) over USB-to-TTL.

Application Layer (Python): A multi-threaded dashboard listens for incoming signals, processes the event, updates the UI state in real-time, and persists the data to an audit log.

**⚡ Features
**
Real-time Monitoring: Immediate UI feedback (Red/Green state) upon medication detection.

Automatic Reset: State-tracking logic that resets medication status daily.

Audit Logging: Time-stamped persistence of all medication events for caregiver review.

Multi-threaded Execution: Background hardware listening ensures the GUI remains responsive.
