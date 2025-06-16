import serial
import time
import numpy as np
import csv
from datetime import datetime

# === Serial Port of the Receiver ESP32 ===
PORT = 'COM5'   # Change to your receiver's COM port
BAUD = 115200

# === Known positions of the anchors (in meters) ===
ANCHORS = {
    "Anchor_A": np.array([0.0, 0.0, 0.0]),
    "Anchor_B": np.array([1.0, 0.0, 0.0]),
    "Anchor_C": np.array([0.0, 0.5, 1.0])
}

RSSI_VALUES = {}

# === RSSI to Distance Conversion ===
def rssi_to_distance(rssi, A0=-45, n=2.0):
    return 10 ** ((A0 - rssi) / (10 * n))

# === Trilateration Calculation ===
def trilaterate(distances):
    A = ANCHORS["Anchor_A"]
    B = ANCHORS["Anchor_B"]
    C = ANCHORS["Anchor_C"]
    dA = distances["Anchor_A"]
    dB = distances["Anchor_B"]
    dC = distances["Anchor_C"]

    ex = (B - A) / np.linalg.norm(B - A)
    i = np.dot(ex, C - A)
    ey = (C - A - i * ex) / np.linalg.norm(C - A - i * ex)
    ez = np.cross(ex, ey)
    d = np.linalg.norm(B - A)
    j = np.dot(ey, C - A)

    x = (dA**2 - dB**2 + d**2) / (2 * d)
    y = (dA**2 - dC**2 + i**2 + j**2 - 2 * i * x) / (2 * j)
    z = np.sqrt(abs(dA**2 - x**2 - y**2))

    return A + x * ex + y * ey + z * ez

# === Initialize CSV Logging ===
csv_file = open('localization_log.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Timestamp", "RSSI_A", "RSSI_B", "RSSI_C",
                     "Dist_A", "Dist_B", "Dist_C", "X", "Y", "Z"])

# === Serial Reading and Logging Loop ===
ser = serial.Serial(PORT, BAUD)
print("Listening on", PORT)

try:
    while True:
        line = ser.readline().decode().strip()
        if "SSID" in line and "RSSI" in line:
            parts = line.split()
            ssid = parts[1]
            rssi = int(parts[3])
            RSSI_VALUES[ssid] = rssi
            print(f"{ssid} -> RSSI: {rssi}")

        if all(k in RSSI_VALUES for k in ANCHORS):
            distances = {k: rssi_to_distance(RSSI_VALUES[k]) for k in ANCHORS}
            pos = trilaterate(distances)

            # Log to CSV
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            row = [
                now,
                RSSI_VALUES["Anchor_A"],
                RSSI_VALUES["Anchor_B"],
                RSSI_VALUES["Anchor_C"],
                round(distances["Anchor_A"], 2),
                round(distances["Anchor_B"], 2),
                round(distances["Anchor_C"], 2),
                round(pos[0], 2),
                round(pos[1], 2),
                round(pos[2], 2),
            ]
            csv_writer.writerow(row)
            print("Logged:", row)
            csv_file.flush()  # Ensure data is written
            time.sleep(1)

except KeyboardInterrupt:
    print("Stopped by user.")
finally:
    ser.close()
    csv_file.close()
