# Hardware Setup Notes

## Components

- ESP32 development board with Wi-Fi
- Servo motor compatible with the sorting gate
- Camera supported by the computer or Raspberry Pi running the Python application
- Regulated power supply sized for the servo
- Jumper wires and a stable mechanical mount
- Optional conveyor belt and item-presence sensor, depending on the physical build

## ESP32 firmware settings

The example firmware currently defines:

- Servo signal pin: GPIO 12
- Neutral position: 90 degrees
- Recyclable position: 0 degrees
- Not-recyclable position: 180 degrees
- HTTP server port: 8080

These are example settings. Confirm the correct GPIO, safe servo travel, and mechanical direction for your actual hardware before powering the mechanism.

## Power and wiring precautions

- Do not power a servo directly from an ESP32 3.3 V pin.
- Use a regulated supply with sufficient current for the servo.
- Connect the external servo supply ground and ESP32 ground together.
- Check the servo's voltage rating and the board's GPIO voltage limits.
- Keep motor power wiring separate from sensitive signal wiring where practical.
- Test the servo with the mechanism disconnected before connecting the gate or linkage.

## Camera and conveyor

Position the camera so the object is visible in a consistent detection zone. Use stable lighting and avoid placing the camera where vibration or the conveyor can move the view. Add a physical item-presence sensor only if the actual build requires it.

## Verify before use

1. Confirm the exact ESP32 board model and pinout.
2. Confirm the servo signal, power, and ground wiring.
3. Test the firmware endpoints with the servo linkage disconnected.
4. Verify both sorting directions at low mechanical load.
5. Test the camera and YOLO predictions separately before enabling automatic servo commands.