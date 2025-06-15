#include <WiFi.h>

const char* ssid = "MOTO G85";         // Change this
const char* password = "charanreddy";  // Change this

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
    Serial.print(".");
  }
  Serial.println("\nConnected!");
}

void loop() {
  int rssi = WiFi.RSSI();
  Serial.print("RSSI: ");
  Serial.println(rssi);
  delay(1000); // Adjust speed as needed
}
