#include <WiFi.h>

const char* ssid = "Anchor_A";  // Change this to Anchor_B, Anchor_C for other ESPs
const char* password = "12345678";

void setup() {
  Serial.begin(115200);
  WiFi.softAP(ssid, password);
  Serial.println("Access Point Started: ");
  Serial.println(ssid);
}

void loop() {
  delay(100); // Nothing else to do
}
