# Smart Waste Segregation System using YOLO and IoT

An academic internship project exploring automated waste classification and sorting with computer vision and microcontroller-based actuation.

## Project overview

The internship report describes a system that identifies waste items from camera images using YOLO object detection, then directs items toward recyclable or non-recyclable collection areas using a servo-based mechanism.

The report discusses a conveyor belt, camera, ESP32 / Arduino-class controller, servo motor, optional ultrasonic sensing, Python, OpenCV, and YOLO. The recovered firmware here is a small ESP32 Wi-Fi/servo controller example, not the complete end-to-end detection system.

## Repository status

**Partially recovered from the original internship report.** The report contains an ESP32 controller listing, but it does not include the complete Python YOLO detection script, trained model weights, dataset, or complete circuit documentation. Those parts are not claimed as implemented here.

## Repository structure

```text
smart-waste-segregation/
├── README.md
└── firmware/
    └── esp32_servo_controller.ino
```

## Recovered firmware

The sketch in `firmware/esp32_servo_controller.ino`:
- Connects an ESP32 to Wi-Fi.
- Starts a simple server on port 8080.
- Accepts a recyclable or not-recyclable request.
- Moves a servo to a configured position and returns it to neutral.

## Hardware and tools referenced by the report

| Component / tool | Purpose described in the report |
|---|---|
| Camera | Capture images of waste items |
| YOLO | Detect and classify waste objects |
| Python and OpenCV | Process camera frames and run detection |
| ESP32 / Arduino | Receive classification and control outputs |
| Servo motor | Move the sorting mechanism |
| Conveyor belt | Move items through the sorting area |
| Ultrasonic sensor | Detect item presence in the described methodology |
| Arduino IDE | Develop and upload controller firmware |

The report uses both Arduino Uno and ESP32 terminology in different sections. The recovered code imports `WiFi.h` and `ESP32Servo.h`, so it is written for an ESP32-compatible environment. Confirm the actual board and wiring before hardware use.

## Run the recovered ESP32 sketch

1. Install Arduino IDE and ESP32 board support.
2. Install the `ESP32Servo` library.
3. Open `firmware/esp32_servo_controller.ino`.
4. Set `YOUR_WIFI_SSID` and `YOUR_WIFI_PASSWORD` to your local test-network credentials.
5. Select the correct ESP32 board and serial port, then upload.
6. Open Serial Monitor at 115200 baud and note the ESP32 IP address.
7. From another device on the same Wi-Fi network, test:
   - `http://<ESP32-IP>:8080/recyclable`
   - `http://<ESP32-IP>:8080/not-recyclable`

The route handling and timeout behavior in this recovered sketch have been cleaned up to make the example easier to test; they are not a byte-for-byte copy of the report listing.

## Safety and security notes

- Do not commit real Wi-Fi credentials, passwords, or private configuration.
- Check servo angles, GPIO assignment, power supply, and mechanical travel before connecting the mechanism.
- This sample server is intended for a controlled local test network, not direct exposure to the public internet.
- The recovered material has not been verified against the original physical hardware.

## Internship context

The submitted report is titled **Smart Waste Segregation System leveraging IoT and the YOLO algorithm** and describes work in an IoT Developer role during a Siemens-related internship programme at NIT Warangal (2024–2025 academic period).

## Next items to recover

- Python YOLO / OpenCV camera-detection script.
- Model configuration and trained weights.
- Dataset and class labels.
- ESP32/Arduino communication code used by the detector.
- Wiring diagram, pin map, and additional hardware photographs.

When original files are available, they can be added and documented here. Until then, this repository remains a partial recovery of the project materials.
