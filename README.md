# Indoor-Localization-RSSI
 Indoor 3D Localization using ESP32 + RSSI + Python Trilateration
 # Indoor 3D Localization using ESP32 and Python

This project demonstrates how to implement indoor localization using 3 ESP32 devices and RSSI-based trilateration.

## 🔧 What It Does

- ESP32 devices scan Wi-Fi RSSI strength
- Python script reads RSSI and calculates 3D position using trilateration
- Displays target location in terminal

---

## 🛠 Software Required

- VS Code
- PlatformIO Extension for VS Code
- Python 3.10 or higher
- PySerial & NumPy: `pip install -r requirements.txt`
- Git (optional: to upload to GitHub)

---

## 📁 Project Structure
- Create a separate folder for 3 Anchors for ESP32 Devices by using PlatformIO in VS Code
-📁 AnchorA
-📁 AnchorB
-📁 AnchorC
---
### 1. Upload Firmware to 3 ESP32s
- Open each Anchor_X folder in VS Code with PlatformIO
- Upload using `PlatformIO: Upload`
- All ESP32s must connect to the same Wi-Fi hotspot

### 2. Run Python Script
- Open `Python_Script/python.py`
- Edit COM port values for each anchor
- Run the code after running the 3Anchors Code(Don't open the serial monitor) 



