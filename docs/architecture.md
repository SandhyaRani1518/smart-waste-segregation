# System Architecture

## Processing flow

```text
Camera
  | video frames
  v
Python application (OpenCV)
  |
  v
YOLO model (custom waste-class weights)
  | class label + confidence
  v
Class-to-category mapping
  | HTTP request over local Wi-Fi
  v
ESP32 controller
  | GPIO PWM signal
  v
Servo-driven sorting gate
```

## Responsibilities

- **Camera:** provides images of items in the detection zone.
- **Python/OpenCV:** captures frames and displays detections.
- **YOLO:** predicts object classes using the supplied trained weights.
- **Class map:** explicitly maps model labels to recyclable or not-recyclable commands.
- **ESP32:** accepts a local HTTP request and drives the servo.
- **Sorting mechanism:** physically directs the item to the selected bin.

## Integration contract

The Python application calls one of two ESP32 endpoints:

- `GET /recyclable`
- `GET /not-recyclable`

Both devices must be reachable on the same trusted local network. The controller sketch listens on port 8080 by default.

## Current boundaries

The current code includes the ESP32 control example and a Python integration starter. A compatible trained YOLO model, a camera setup, model label configuration, and physical sorting mechanism must be supplied and tested for a complete system.