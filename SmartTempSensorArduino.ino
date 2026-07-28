#include "DHT.h"
#define Type DHT11
int sensePin = 3;
DHT HT(sensePin, Type);
float humidity;
float tempC;
float tempF;
int setTime = 500;
int dt = 1000;
int green_led = 5;
int red_led = 6;
int speedPin = 9;
int dir1 = 12;
int dir2 = 13;
int mSpeed = 90;
float temp_threshold = 76.0;

void setup() {
  Serial.begin(9600);
  HT.begin();
  pinMode(green_led, OUTPUT);
  pinMode(red_led, OUTPUT);
  pinMode(speedPin, OUTPUT);
  pinMode(dir1, OUTPUT);
  pinMode(dir2, OUTPUT);
  delay(setTime);
  digitalWrite(dir1, LOW);
  digitalWrite(dir2, HIGH);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "read_temp") {
      humidity = HT.readHumidity();
      tempC = HT.readTemperature();
      tempF = HT.readTemperature(true);

      if (tempF > temp_threshold) {
        digitalWrite(green_led, LOW);
        digitalWrite(red_led, HIGH);
        analogWrite(speedPin, mSpeed);
      } else {
        digitalWrite(green_led, HIGH);
        digitalWrite(red_led, LOW);
        analogWrite(speedPin, 0);
      }

      Serial.println(tempF, 2);
    }
    else if (command == "enable_fan") {
      analogWrite(speedPin, 255);
      Serial.println("Fan enabled");
    }
    else if (command == "disable_fan") {
      analogWrite(speedPin, 0);
      Serial.println("Fan disabled");
    }
    else {
      Serial.println("ERROR: Unknown command");
    }
  }
}