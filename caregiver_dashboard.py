import tkinter as tk
from datetime import datetime
import serial
import threading

class care_giver_dashboard():

    def __init__(self, root):
        self.root = root
        root.title("Caregiver's Dashboard")
        root.geometry("500x700")
        root.configure(bg="#2c3e50")

        #status display
        self.status_frame = tk.Frame(root, bg="red", height=150)
        self.status_frame.pack(fill="x")
        self.status_text = tk.Label(self.status_frame, text="MEDICATION LATE", fg="white", bg="red", font=("Arial", 24, "bold"))
        self.status_text.pack(pady=40)

        #system Log
        tk.Label(root, text="System Log:", font=("Arial", 12, "bold")).pack(pady=10)
        self.log = tk.Text(root, height=12, width=50, bg="#f0f0f0")
        self.log.pack(padx=20, pady=5)

        #buttons
        #simulates the camera signal if hardware isn't connected
        self.test_btn = tk.Button(root, text="Simulate Camera Signal", command=self.record_dose, height=2, width=25)
        self.test_btn.pack(pady=10)

        self.reset_btn = tk.Button(root, text="Manual Reset", command=self.reset_system, font=("Arial", 10))
        self.reset_btn.pack(pady=5)

        #serial setup
        try:
            # Note: For Mac, this is often '/dev/cu.usbserial-...' not 'COM3'
            self.ser = serial.Serial('COM3', 115200, timeout=1)
            self.log.insert(tk.END, "Connected to Hardware... Monitoring started.\n")
        except:
            self.log.insert(tk.END, "Running in Simulation Mode (No Camera).\n")

        self.listen_thread = threading.Thread(target=self.listen_for_hardware, daemon=True)
        self.listen_thread.start()

    def listen_for_hardware(self):
        while True:
            #midnight reset
            now_time = datetime.now().strftime("%H:%M")
            if now_time == "00:00":
                self.root.after(0, self.reset_system)

            #read fromm serial
            if hasattr(self, 'ser') and self.ser.in_waiting > 0:
                try:
                    line = self.ser.readline().decode('utf-8').strip()
                    if line == "MOTION_DETECTED":
                        self.record_dose()
                except:
                    pass

    def record_dose(self):
        timestamp = datetime.now().strftime("%H:%M:%S")
        # Use .after() to update UI from a background thread safely
        self.root.after(0, lambda: self.status_frame.config(bg="green"))
        self.root.after(0, lambda: self.status_text.config(text="MEDICATION TAKEN", bg="green"))
        self.root.after(0, lambda: self.log.insert(tk.END, f"[{timestamp}] - Camera Triggered: Meds Processed\n"))

        self.save_to_file(timestamp)

    def save_to_file(self, time_string):
        with open("med_history.txt", "a") as file:
            file.write(f"Medication taken at: {time_string}\n")
            
    def reset_system(self):
        self.status_frame.config(bg="red")
        self.status_text.config(text="MEDICATION LATE", bg="red")
        self.log.insert(tk.END, "--- System Reset for New Day ---\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = care_giver_dashboard(root)
    root.mainloop()

