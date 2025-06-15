import serial
import numpy as np
import time
import csv
from datetime import datetime

# Replace with your COM ports
PORT_A = 'COM3'
PORT_B = 'COM6'
PORT_C = 'COM5'
BAUD_RATE = 115200

# 3D coordinates of anchors
A = np.array([0.0, 0.0, 0.0])
B = np.array([3.0, 0.0, 0.0])
C = np.array([0.0, 4.0, 2.0])

# Convert RSSI to distance
def rssi_to_distance(rssi, A0=-45, n=2.0):
    return 10 ** ((A0 - rssi) / (10 * n))

# Read RSSI from serial
def read_rssi(serial_port):
    try:
        line = serial_port.readline().decode().strip()
        if "RSSI" in line:
            return int(line.split(":")[1].strip())
    except:
        return None

# Open serial ports
serA = serial.Serial(PORT_A, BAUD_RATE, timeout=1)
serB = serial.Serial(PORT_B, BAUD_RATE, timeout=1)
serC = serial.Serial(PORT_C, BAUD_RATE, timeout=1)

# Prepare CSV file
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"rssi_log_{timestamp}.csv"
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([
        "Time",
        "RSSI_A", "RSSI_B", "RSSI_C",
        "Dist_A", "Dist_B", "Dist_C",
        "Pos_X", "Pos_Y", "Pos_Z"
    ])

    print(f"📝 Logging to {filename}... Press Ctrl+C to stop.\n")

    while True:
        try:
            rssiA = read_rssi(serA)
            rssiB = read_rssi(serB)
            rssiC = read_rssi(serC)

            if rssiA and rssiB and rssiC:
                dA = rssi_to_distance(rssiA)
                dB = rssi_to_distance(rssiB)
                dC = rssi_to_distance(rssiC)

                print(f"RSSI -> Distance (m): A={dA:.2f}, B={dB:.2f}, C={dC:.2f}")
               

                # Trilateration
                P1, P2, P3 = A, B, C
                ex = (P2 - P1) / np.linalg.norm(P2 - P1)
                i = np.dot(ex, P3 - P1)
                ey = (P3 - P1 - i * ex) / np.linalg.norm(P3 - P1 - i * ex)
                ez = np.cross(ex, ey)
                d = np.linalg.norm(P2 - P1)
                j = np.dot(ey, P3 - P1)

                x = (dA ** 2 - dB ** 2 + d ** 2) / (2 * d)
                y = (dA ** 2 - dC ** 2 + i ** 2 + j ** 2 - 2 * i * x) / (2 * j)
                z_sq = dA ** 2 - x ** 2 - y ** 2
                z = np.sqrt(z_sq) if z_sq > 0 else 0

                pos = P1 + x * ex + y * ey + z * ez
                print(f"Estimated Position: {np.round(pos, 2)}\n")

                # Write to CSV
                writer.writerow([
                    datetime.now().strftime("%H:%M:%S"),
                    rssiA, rssiB, rssiC,
                    round(dA, 2), round(dB, 2), round(dC, 2),
                    round(pos[0], 2), round(pos[1], 2), round(pos[2], 2)
                ])

            time.sleep(1)

        except KeyboardInterrupt:
            print("\n🛑 Logging stopped by user.")
            break

# Cleanup
serA.close()
serB.close()
serC.close()
