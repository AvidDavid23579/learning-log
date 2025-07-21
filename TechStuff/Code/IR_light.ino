// Define pin numbers
const int ledPin = 13;   // LED connected to digital pin 13
const int irSensorPin = 2; // IR Sensor connected to digital pin 2

void setup() {
  pinMode(ledPin, OUTPUT);   // Set the LED pin as output
  pinMode(irSensorPin, INPUT); // Set the IR sensor pin as input
}

void loop() {
  int sensorState = digitalRead(irSensorPin); 

  // The sensor outputs LOW when it detects an obstacle
  if (sensorState == LOW) {
    digitalWrite(ledPin, HIGH); 
  } else {
    digitalWrite(ledPin, LOW);  
  }
  delay(100);
}