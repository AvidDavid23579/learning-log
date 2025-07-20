#include <Wire.h>
#include <LiquidCrystal_I2C.h>

void display(String disp);
LiquidCrystal_I2C lcd(0x27, 16, 2); 
String disp = "GOOD AFTERNOON!";
int d = disp.length();

void setup() {
  lcd.begin(16,2);        
  lcd.backlight();
  display(disp);
}    
  
void loop() {
}

void display(String disp){
  lcd.setCursor(0,0);
  for (int i = 0; i < d; i++){
    lcd.print(disp[i]);
    delay(100); 
  }
}
