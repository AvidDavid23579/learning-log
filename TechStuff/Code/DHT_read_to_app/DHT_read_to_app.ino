#include <DHT.h>

#define DHTPIN 2     
#define DHTTYPE DHT11   
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  dht.begin();
  delay(2000);
}

void loop() {
  // put your main code here, to run repeatedly:
  float t = dht.readTemperature();
  float h = dht.readHumidity();

    if (!isnan(t) && !isnan(h)) {
      Serial.print(t);
      Serial.print(",");
      Serial.println(h);
  }
  delay(1000);
}

