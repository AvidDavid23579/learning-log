#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);
#define DHTPIN 2     
#define DHTTYPE DHT11   
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  // put your setup code here, to run once:
  lcd.begin(16,2);
  lcd.backlight();
  dht.begin();
  lcd.setCursor(0,0);
  lcd.print("Sensor Ready");
  delay(2000);
  lcd.clear();
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(2000);
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();

    if (isnan(temp) || isnan(hum)) {
    lcd.setCursor(0, 1);
    lcd.print("Read error");
    return;
  }

  // Display on LCD
  lcd.setCursor(0, 0);
  lcd.print("T:");
  lcd.print(temp, 1);
  lcd.print((char)223);  // degree symbol
  lcd.print("C ");

  lcd.setCursor(0, 1);
  lcd.print("H:");
  lcd.print(hum, 0);
  lcd.print("% ");


}

