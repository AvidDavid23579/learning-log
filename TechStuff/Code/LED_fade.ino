void setup() {
  // put your setup code here, to run once:
  pinMode(9, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  // Fade in
  for (int i = 0; i <= 255; i++){
    analogWrite(9,i);
    delay(10);
  }
  // Fade out
  for (int i = 255; i >= 0; i--){
    analogWrite(9,i);
    delay(10);
  }
}
