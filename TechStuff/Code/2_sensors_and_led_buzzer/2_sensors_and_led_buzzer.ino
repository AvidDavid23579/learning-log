#include <DHT.h>

#define DHTPIN 2   
#define DHTTYPE DHT11 
const int buzzerPin = 3;  
const int trigPin = 9;
const int echoPin = 10;
const int red = 4;
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  dht.begin();
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(buzzerPin, OUTPUT);
  pinMode(red, OUTPUT);
  delay(5000);
}

void loop() {
  // put your main code here, to run repeatedly:

  // passive sensors
  float t = dht.readTemperature();
  float h = dht.readHumidity();

  // ultrasonic sensor
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH);
  float d = duration / 58.0;
    if (d < 10) {
      digitalWrite(red, HIGH);
      digitalWrite(buzzerPin, HIGH);
      delay(500);
      digitalWrite(buzzerPin, LOW);
      digitalWrite(red, LOW);
    }

    if (!isnan(t) && !isnan(h) && !isnan(d)) {
      Serial.print(t);
      Serial.print(",");
      Serial.print(h);
      Serial.print(",");
      Serial.println(d);

  }
  delay(300);
}

