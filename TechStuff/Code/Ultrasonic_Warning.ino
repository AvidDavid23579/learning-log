#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);
const int trigPin = 9;
const int echoPin = 10;
const int red = 13;
const int green = 12;

void setup() {
  // put your setup code here, to run once:
  pinMode(red, OUTPUT);
  pinMode(green, OUTPUT);
  lcd.begin(16,2);
  lcd.backlight();
  lcd.setCursor(0,0);
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  lcd.print("Radar Active");
  delay(2000);
  lcd.clear();
}

void loop() {
  // put your main code here, to run repeatedly:
  // Send pulse
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Read pulse
  long duration = pulseIn(echoPin, HIGH);

  // Convert to distance(cm)
  float distance = duration / 58.0;

  // Print result
  lcd.print("D: ");
  lcd.print(distance);
  lcd.println(" cm");

  lcd.clear();                // Clear display at start of update 
  lcd.setCursor(0, 0);        // First row
  lcd.print("D: ");
  lcd.print(distance);
  lcd.print(" cm");

  lcd.setCursor(0, 1);        // Second row
  if (distance < 30) {
    lcd.print("DANGEROUS!");
    digitalWrite(red, HIGH);
    digitalWrite(green, LOW);
  }  
  else {
    lcd.print("SAFE!");
    digitalWrite(green, HIGH);
    digitalWrite(red, LOW);
  }
delay(300);
}
