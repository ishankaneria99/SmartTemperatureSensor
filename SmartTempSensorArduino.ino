#include "DHT.h"
#define Type DHT11
int sensePin = 3;
DHT HT(sensePin, Type);
float humidity;
float tempC;
float tempF;
int setTime = 500;
int dt = 1000;
int redPin = 5;
int greenPin = 6;
int bluePin = 11;
int speedPin = 9;
int dir1 = 12;
int dir2 = 13;
int mSpeed = 90;
float temp_threshold = 76.0;
bool forwardDirection = true;

void setup() {
  Serial.begin(9600);
  HT.begin();
  pinMode(greenPin, OUTPUT);
  pinMode(redPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
  pinMode(speedPin, OUTPUT);
  pinMode(dir1, OUTPUT);
  pinMode(dir2, OUTPUT);
  delay(setTime);
  digitalWrite(dir1, LOW);
  digitalWrite(dir2, HIGH);
}

void loop() {
  if (Serial.available() > 0) {                    // ← restored
    String command = Serial.readStringUntil('\n'); // ← restored
    command.trim();                                 // ← restored

    if (command == "read_temp") 
    {
      humidity = HT.readHumidity();
      tempC = HT.readTemperature();
      tempF = HT.readTemperature(true);

      if (isnan(tempF) || isnan(humidity)) 
      {
        Serial.println("ERROR: Sensor read failed");
      }
      else 
      {
        if (tempF >= temp_threshold + 5) 
        {
          digitalWrite(greenPin, LOW);
          digitalWrite(redPin, HIGH);
          digitalWrite(bluePin, LOW);
          analogWrite(speedPin, 255);
        } 
        else if (tempF >= temp_threshold)
        {
          digitalWrite(greenPin, HIGH);
          digitalWrite(redPin, HIGH);
          digitalWrite(bluePin, LOW);
          analogWrite(speedPin, mSpeed);
        }
        else
        {
          digitalWrite(greenPin, HIGH);
          digitalWrite(redPin, LOW);
          digitalWrite(bluePin, LOW);
          analogWrite(speedPin, 0);
        }
        Serial.println(tempF, 2);
      }
    }
    else if (command == "enable_fan") 
    {
      analogWrite(speedPin, 255);
      Serial.println("Fan enabled");
    }
    else if (command == "disable_fan") 
    {
      analogWrite(speedPin, 0);
      Serial.println("Fan disabled");
    }
    else if (command == "turn_on_green")
    {
      digitalWrite(greenPin, HIGH);
      digitalWrite(redPin, LOW);
      digitalWrite(bluePin, LOW);
      Serial.println("Green LED on");
    }
    else if (command == "turn_on_red")
    {
      digitalWrite(greenPin, LOW);
      digitalWrite(redPin, HIGH);
      digitalWrite(bluePin, LOW);
      Serial.println("Red LED on");
    }
    else if (command == "change_fan_dir") 
    {
      forwardDirection = !forwardDirection;

      if (forwardDirection) 
      {
        digitalWrite(dir1, LOW);
        digitalWrite(dir2, HIGH);
        Serial.println("Fan direction: forward");
      } 
      else 
      {
        digitalWrite(dir1, HIGH);
        digitalWrite(dir2, LOW);
        Serial.println("Fan direction: reverse");
      }
    }
    else 
    {
      Serial.println("ERROR: Unknown command");
    }
  }
}
