const int IR = 2;
const int GAS = A0;
const int trigPin = 9;
const int echoPin = 10;
const int buzzer = 4;
const int led = 3;
const int fan = 7;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(led, OUTPUT);
  pinMode(buzzer, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(fan, OUTPUT);
  digitalWrite(fan, HIGH);
  delay(2000);
}

void loop() {
  // put your main code here, to run repeatedly:
  
  // ultrasonic sensor
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH, 30000);

  // sensor variables
  bool s = digitalRead(IR);
  int g = analogRead(GAS);
  float d = duration / 58.0;
  
  // IR buzzer
  if (s == 0){
    digitalWrite(buzzer, HIGH);
  }
  else{
    digitalWrite(buzzer, LOW);
  }
  
  // ultrasonic LED and fan
  int led_brightness = map(duration, 2000, 0, 0, 255);  // closer = brighter
  led_brightness = constrain(led_brightness, 0, 255);
  analogWrite(led, led_brightness);

  if (d < 10){
    digitalWrite(fan, LOW);
  }
  else{
    digitalWrite(fan, HIGH);
  }

  // CSV logging
  if (!isnan(s) && !isnan(g) && !isnan(d)){
    Serial.print(s);
    Serial.print(",");
    Serial.print(g);
    Serial.print(",");
    Serial.println(d);
  }



  // serial delay
  delay(100);
}
