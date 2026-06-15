CODE FOR WEBCAM TO SCAN QRCODE

import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import time

# Start webcam
cap = cv2.VideoCapture(0)

# Open attendance file in append mode
attendance_file = 'attendance.txt'
names = set()  # Use a set to store unique names

# Load existing names from the attendance file if it exists
try:
    with open('attendance.txt' 'r') as f:
        for line in f.readlines():
            names.add(line.strip())
except FileNotFoundError:
    print(f"File '{attendance_file}' not found. Creating new one.")

print('Reading QR codes...')

# Function to enter data into the attendance file
def enter_data(name):
    if name not in names:
        names.add(name)
        with open(attendance_file, 'a') as f:
            f.write(name + '\n')
        print(f'Added {name} is present.')
    else:
        print(f'{name} is present.')

# Function to check if data is already in attendance
def check_data(data):
    name = data.decode('utf-8')
    if name not in names:
        enter_data(name)
    else:
        print(f'{name} is already in present.')

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame.")
        break

    decoded_objects = pyzbar.decode(frame)

    for obj in decoded_objects:
        check_data(obj.data)

    cv2.imshow('Frame', frame)

    # Close window if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()

# Print final attendance list
print("\nFinal Present List:")
for name in names:
    print(name)

# Close the file after the loop
print(f"Attendance file '{attendance_file}' updated.")
