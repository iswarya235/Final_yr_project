#include <ESP8266WiFi.h>
#include "ThingSpeak.h" // always include thingspeak header file after other header files and custom macros
char ssid[] ="Project";   // your network SSID (name) 
char pass[] = "12345678";   // your network password
int keyIndex = 0;            // your network key Index number (needed only for WEP)
WiFiClient  client;
#include "DHTesp.h"
#include <Adafruit_ADS1X15.h>
int ldr=0;
#include <LCD_I2C.h>

LCD_I2C lcd(0x27);
Adafruit_ADS1115 ads; 
float adc_voltage = 0.0;
float in_voltage = 0.0;

 String st="";
// Floats for resistor values in divider (in ohms)
float R1 = 30000.0;
float R2 = 7500.0; 
 
// Float for Reference Voltage
float ref_voltage = 5.0;
 
// Integer for ADC value
int adc_value = 0;
 
#ifdef ESP32
#pragma message(THIS EXAMPLE IS FOR ESP8266 ONLY!)
#error Select ESP8266 board.
#endif

DHTesp dht;

int count = 0;

void setup() {
  pinMode(D5,OUTPUT);
  pinMode(D6,OUTPUT);
  //digitalWrite(D6,HIGH);
 pinMode(A0,INPUT);
  Serial.begin(9600);
  lcd.begin(); // If you are using more I2C devices using the Wire library use lcd.begin(false)
                 // this stop the library(LCD_I2C) from calling Wire.begin()
    lcd.backlight();
    lcd.setCursor(0, 0);
    lcd.print("HOME"); // You can make spaces using well... spaces
    lcd.setCursor(0, 1); // Or setting the cursor in the desired position.
    lcd.print("MONITORING");
    delay(2500);
    lcd.clear();
if (!ads.begin()) {
    Serial.println("Failed to initialize ADS.");
    while (1);
  }
   dht.setup(D0, DHTesp::DHT11);
   WiFi.mode(WIFI_STA); 
  ThingSpeak.begin(client);
   if(WiFi.status() != WL_CONNECTED){

    while(WiFi.status() != WL_CONNECTED){
      WiFi.begin(ssid, pass);  // Connect to WPA/WPA2 network. Change this line if using open or WEP network
      Serial.print(".");
      delay(5000);     
    } 
    Serial.println("\nConnected.");
  } 
}

void loop() {
  ldr=analogRead(A0);
  delay(dht.getMinimumSamplingPeriod());
ldr=ldr/250;
  float humidity = dht.getHumidity();
  float temperature = dht.getTemperature();
lcd.setCursor(0, 0);
    lcd.print("TEMPERATURE"); // You can make spaces using well... spaces
    lcd.setCursor(0, 1); // Or setting the cursor in the desired position.
    lcd.print(temperature);
    delay(500);
    lcd.clear();
 
int16_t adc0, adc1, adc2, adc3;
  float volts0, volts1, volts2, volts3;

  adc0 = ads.readADC_SingleEnded(0);
  adc1 = ads.readADC_SingleEnded(1);
  adc2 = ads.readADC_SingleEnded(2);
  adc3 = ads.readADC_SingleEnded(3);
adc0=adc0/4000;
adc1=adc1/4000;
analogWrite(D5,(adc0*4));
analogWrite(D6,(adc1*40));
if(ldr==0)
{
  ldr=1;
  }
  volts0 = ads.computeVolts(adc0);
  volts1 = ads.computeVolts(adc1);
  volts2 = ads.computeVolts(adc2);
  volts3 = ads.computeVolts(adc3);
Serial.println(adc0);
lcd.setCursor(0, 0);
    lcd.print("POT-1"); // You can make spaces using well... spaces
    lcd.setCursor(0, 1); // Or setting the cursor in the desired position.
    lcd.print(adc0);
    delay(500);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("POT-2"); // You can make spaces using well... spaces
    lcd.setCursor(0, 1); // Or setting the cursor in the desired position.
    lcd.print(adc1);
    delay(500);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("LDR"); // You can make spaces using well... spaces
    lcd.setCursor(0, 1); // Or setting the cursor in the desired position.
    lcd.print(ldr);
    delay(500);
    lcd.clear();
Serial.println(adc1);
 ThingSpeak.setField(1,temperature );
  ThingSpeak.setField(2,ldr);
  ThingSpeak.setField(3,adc0);
  ThingSpeak.setField(4,adc1);
   int xrt = ThingSpeak.writeFields(2049359, "6Y4L3ZDOATSXYZYM");

    
}
