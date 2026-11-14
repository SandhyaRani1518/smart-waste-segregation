#include <WiFi.h>
#include <ESP32Servo.h>

// Reconstructed from the implementation listing in the internship report.
// Wi-Fi credentials are placeholders. Do not commit real credentials.

const char* WIFI_SSID = "YOUR_WIFI_SSID";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

constexpr uint8_t SERVO_PIN = 12;
constexpr int SERVO_NEUTRAL_ANGLE = 90;
constexpr int SERVO_NON_RECYCLABLE_ANGLE = 180;
constexpr int SERVO_RECYCLABLE_ANGLE = 0;

WiFiServer server(8080);
Servo sortingServo;

void sendHttpResponse(WiFiClient& client, const String& message) {
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/plain; charset=utf-8");
  client.println("Connection: close");
  client.println();
  client.println(message);
}

void setSortingPosition(bool recyclable) {
  if (recyclable) {
    Serial.println("Classification: recyclable");
    sortingServo.write(SERVO_RECYCLABLE_ANGLE);
  } else {
    Serial.println("Classification: not recyclable");
    sortingServo.write(SERVO_NON_RECYCLABLE_ANGLE);
  }

  delay(1000);
  sortingServo.write(SERVO_NEUTRAL_ANGLE);
}

void setup() {
  Serial.begin(115200);
  sortingServo.attach(SERVO_PIN);
  sortingServo.write(SERVO_NEUTRAL_ANGLE);

  Serial.println("Connecting to Wi-Fi...");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print('.');
  }

  Serial.println();
  Serial.println("Wi-Fi connected");
  Serial.print("ESP32 IP address: ");
  Serial.println(WiFi.localIP());

  server.begin();
  Serial.println("HTTP server started on port 8080");
}

void loop() {
  WiFiClient client = server.available();
  if (!client) {
    return;
  }

  Serial.println("Client connected");

  const unsigned long waitStarted = millis();
  while (!client.available() && (millis() - waitStarted < 5000)) {
    delay(1);
  }

  if (!client.available()) {
    client.stop();
    Serial.println("Client timed out");
    return;
  }

  String requestLine = client.readStringUntil('\r');
  requestLine.trim();
  Serial.print("Request: ");
  Serial.println(requestLine);

  // Test: http://<ESP32-IP>:8080/recyclable
  // Test: http://<ESP32-IP>:8080/not-recyclable
  if (requestLine.indexOf("GET /not-recyclable") >= 0) {
    setSortingPosition(false);
    sendHttpResponse(client, "ESP32: not recyclable item selected");
  } else if (requestLine.indexOf("GET /recyclable") >= 0) {
    setSortingPosition(true);
    sendHttpResponse(client, "ESP32: recyclable item selected");
  } else {
    sendHttpResponse(client, "Use /recyclable or /not-recyclable");
  }

  delay(1);
  client.stop();
  Serial.println("Client disconnected");
}
