# Smart Waste Segregation System

A computer-vision and IoT prototype for identifying waste items and directing a sorting mechanism toward recyclable or non-recyclable collection bins.

## Project overview

The intended workflow is:
1. A camera captures waste items moving through the inspection area.
2. A YOLO object-detection model identifies the waste class.
3. Python maps the detected class to a sorting category.
4. The application sends a local Wi-Fi command to an ESP32.
5. The ESP32 moves a servo to the configured sorting position.

## Current contents

```text
smart-waste-segregation/
├── config/
│   └── class_map.example.json
├── docs/
│   ├── architecture.md
│   └── hardware.md
├── firmware/
│   └── esp32_servo_controller.ino
├── src/
│   └── detect_and_sort.py
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10 or later
- An ESP32 board with Wi-Fi
- A compatible camera (USB webcam or supported camera source)
- A servo motor and suitable external power supply
- Arduino IDE with ESP32 board support
- The `ESP32Servo` Arduino library
- YOLO weights trained for the waste classes you intend to detect

## 1. Configure the ESP32

1. Open `firmware/esp32_servo_controller.ino` in Arduino IDE.
2. Replace `YOUR_WIFI_SSID` and `YOUR_WIFI_PASSWORD` with your local network credentials.
3. Check the servo GPIO and angles against your actual board and mechanism.
4. Upload the sketch to the ESP32.
5. Open Serial Monitor at 115200 baud and note the IP address printed by the board.

The controller listens on port 8080 and accepts:
- `/recyclable`
- `/not-recyclable`

Test the endpoints from a device on the same Wi-Fi network before connecting the camera application.

## 2. Set up the Python application

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS / Linux:
# source .venv/bin/activate
pip install -r requirements.txt
```

Copy `config/class_map.example.json` to `config/class_map.json` and adjust the class names to exactly match the names used by your trained model.

Run the detector with your model weights and ESP32 IP address:

```bash
python src/detect_and_sort.py --weights path/to/your-waste-model.pt --esp32-url http://192.168.1.50:8080 --class-map config/class_map.json
```

Press `q` in the camera window to stop the application.

## Important model configuration

The Python application does not assume that a general-purpose YOLO model knows how to classify your waste categories. Supply weights trained for your target classes and edit the class map to match the model's labels. Unknown labels are displayed but do not trigger the servo.

## Safety and limitations

- The Python detector is an integration starter; it must be tested with the correct trained weights and camera.
- Check the ESP32 board, servo GPIO, servo travel, power supply, and common ground before powering the mechanism.
- Power the servo from a suitable regulated supply; do not assume the ESP32 board can power the motor directly.
- Keep the ESP32 server on a trusted local network. It is a simple demonstration endpoint, not an authenticated production service.
- Do not commit real Wi-Fi credentials, model files you do not have rights to share, or private data.
- No model accuracy or end-to-end hardware performance is claimed until tested on the actual setup.

## Next improvements

- Add a labelled waste-image dataset and train/evaluate a custom YOLO model.
- Add a wiring diagram and camera/conveyor integration details for the actual hardware.
- Record test results, class-wise precision/recall, and sorting success rate.
- Add tests and a configuration file for the specific board and motor geometry.

See `docs/architecture.md` and `docs/hardware.md` for the design and hardware notes.