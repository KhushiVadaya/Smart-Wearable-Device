#include <WiFi.h>
#include <HTTPClient.h>
#include "ThingSpeak.h"
// WiFi credentials
const char* ssid = "Wokwi-GUEST";
const char* password = "";  // Your WiFi Password

// ThingSpeak configuration
const String apiKey = "K9HUW7WMOD8JLUO1";    // Replace with your ThingSpeak Write API Key
const String baseURL = "https://api.thingspeak.com/update?api_key=" + apiKey;

// Define pins for ultrasonic sensors
const int trigPinFront = 23;
const int echoPinFront = 22;
const int trigPinBack = 19;
const int echoPinBack = 18;
const int trigPinLeft = 5;
const int echoPinLeft = 17;
const int trigPinRight = 16;
const int echoPinRight = 4;

// Define pin for buzzer
const int buzzerPin = 21;

// Define distance threshold for obstacle detection
int obstacleDistanceThreshold = 50; // in centimeters

void setup() {
  // Initialize serial monitor for debugging
  Serial.begin(115200);  // Use higher baud rate for ESP32

  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Set up Ultrasonic Sensor pins as OUTPUT and INPUT
  pinMode(trigPinFront, OUTPUT);
  pinMode(echoPinFront, INPUT);
  pinMode(trigPinBack, OUTPUT);
  pinMode(echoPinBack, INPUT);
  pinMode(trigPinLeft, OUTPUT);
  pinMode(echoPinLeft, INPUT);
  pinMode(trigPinRight, OUTPUT);
  pinMode(echoPinRight, INPUT);

  // Set up Buzzer pin as OUTPUT
  pinMode(buzzerPin, OUTPUT);
}

void loop() {
  // Measure distances from all sensors
  int distanceFront = measureDistance(trigPinFront, echoPinFront);
  int distanceBack = measureDistance(trigPinBack, echoPinBack);
  int distanceLeft = measureDistance(trigPinLeft, echoPinLeft);
  int distanceRight = measureDistance(trigPinRight, echoPinRight);

  // Variable to hold obstacle direction
  String obstacleDirection = "";

  // Check for obstacles in each direction
  if (distanceFront < obstacleDistanceThreshold) {
    playTone(4000);  // Play front obstacle tone
    obstacleDirection = "Front";
    Serial.println("Obstacle in Front!");
  } else if (distanceBack < obstacleDistanceThreshold) {
    playTone(3000);  // Play back obstacle tone
    obstacleDirection = "Back";
    Serial.println("Obstacle at the Back!");
  } else if (distanceLeft < obstacleDistanceThreshold) {
    playTone(1500);  // Play left obstacle tone
    obstacleDirection = "Left";
    Serial.println("Obstacle on the Left!");
  } else if (distanceRight < obstacleDistanceThreshold) {
    playTone(400);  // Play right obstacle tone
    obstacleDirection = "Right";
    Serial.println("Obstacle on the Right!");
  } else {
    noTone(buzzerPin);  // Turn off the buzzer if no obstacle is detected
  }

  // Send data to ThingSpeak
  sendToThingSpeak(distanceFront, distanceBack, distanceLeft, distanceRight, obstacleDirection);

  delay(100);  // Delay for stability
}

int measureDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH);  // Read the time for the echo
  int distance = duration * 0.034 / 2;  // Calculate distance in cm
  return distance;  // Return distance value
}

void playTone(int toneFrequency) {
  tone(buzzerPin, toneFrequency);  // Play tone at specified frequency
}

void sendToThingSpeak(int front, int back, int left, int right, String direction) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    
    String url = baseURL + "&field1=" + String(front) + "&field2=" + String(back) +
                 "&field3=" + String(left) + "&field4=" + String(right) + 
                 "&field5=" + direction;

    http.begin(url);  // Specify the URL
    int httpResponseCode = http.GET();  // Make the request

    if (httpResponseCode > 0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
    } else {
      Serial.print("Error on sending GET: ");
      Serial.println(httpResponseCode);
    }

    http.end();  // Free resources
  } else {
    Serial.println("WiFi Disconnected");
  }
}
