/* 
 Mike Soroka 06/2019

 Reads from Lux sensor and Range sensor
 Writes to python
 
 This example shows how to get single-shot range
 measurements from the VL53L0X. The sensor can optionally be
 configured with different ranging profiles, as described in
 the VL53L0X API user manual, to get better performance for
 a certain application. This code is based on the four
 "SingleRanging" examples in the VL53L0X API.

 The range readings are in units of mm. */

#include "Adafruit_VEML7700.h"
Adafruit_VEML7700 veml = Adafruit_VEML7700();

#include <Wire.h>
#include <VL53L0X.h>

VL53L0X sensor;

/*add to a module*/
int LightPin = A2;

const int bNumReadings = 50;
int bReadings[bNumReadings];      // the readings from the analog input
int bReadIndex = 0;              // the index of the current reading
int bTotal = 0;                  // the running total
int bAverage = 0;                // the average
int button = A1;
int bRaw = 0;
bool buttonState = false;
int buttonThreshold = 200;
int threshold = 500;

void averageInit(){  // initialize all the readings to 0:
  for (int bThisReading = 0; bThisReading < bNumReadings; bThisReading++) {
    bReadings[bThisReading] = 0;}
}
/*add to a module*/

// Uncomment this line to use long range mode. This
// increases the sensitivity of the sensor and extends its
// potential range, but increases the likelihood of getting
// an inaccurate reading because of reflections from objects
// other than the intended target. It works best in dark
// conditions.

//#define LONG_RANGE


// Uncomment ONE of these two lines to get
// - higher speed at the cost of lower accuracy OR
// - higher accuracy at the cost of lower speed

//#define HIGH_SPEED
//#define HIGH_ACCURACY

void setup()
{
  Serial.begin(115200);

  pinMode(LightPin, OUTPUT);
  averageInit();

  if (!veml.begin()) {
    Serial.println("VEML Sensor not found");
    while (1);
  }
  Serial.println("VEML Sensor found");

  veml.setGain(VEML7700_GAIN_1);
  veml.setIntegrationTime(VEML7700_IT_100MS);

  Serial.print(F("Gain: "));
  switch (veml.getGain()) {
    case VEML7700_GAIN_1: Serial.println("1"); break;
    case VEML7700_GAIN_2: Serial.println("2"); break;
    case VEML7700_GAIN_1_4: Serial.println("1/4"); break;
    case VEML7700_GAIN_1_8: Serial.println("1/8"); break;
  }

  Serial.print(F("Integration Time (ms): "));
  switch (veml.getIntegrationTime()) {
    case VEML7700_IT_25MS: Serial.println("25"); break;
    case VEML7700_IT_50MS: Serial.println("50"); break;
    case VEML7700_IT_100MS: Serial.println("100"); break;
    case VEML7700_IT_200MS: Serial.println("200"); break;
    case VEML7700_IT_400MS: Serial.println("400"); break;
    case VEML7700_IT_800MS: Serial.println("800"); break;
  }

  //veml.powerSaveEnable(true);
  //veml.setPowerSaveMode(VEML7700_POWERSAVE_MODE4);

  veml.setLowThreshold(10000);
  veml.setHighThreshold(20000);
  veml.interruptEnable(true);
  
  Wire.begin();

  sensor.init();
  sensor.setTimeout(500);

#if defined LONG_RANGE
  // lower the return signal rate limit (default is 0.25 MCPS)
  sensor.setSignalRateLimit(0.1);
  // increase laser pulse periods (defaults are 14 and 10 PCLKs)
  sensor.setVcselPulsePeriod(VL53L0X::VcselPeriodPreRange, 18);
  sensor.setVcselPulsePeriod(VL53L0X::VcselPeriodFinalRange, 14);
#endif

#if defined HIGH_SPEED
  // reduce timing budget to 20 ms (default is about 33 ms)
  sensor.setMeasurementTimingBudget(20000);
#elif defined HIGH_ACCURACY
  // increase timing budget to 200 ms
  sensor.setMeasurementTimingBudget(200000);
#endif
}

const long stepSize = 500;
unsigned long previousTime = 0; 
const long stepSize2 = 800;
unsigned long previousTime2 = 0;

void loop()
{

  unsigned long currentTime = millis();

  bTotal = bTotal - bReadings[bReadIndex];
  bRaw = analogRead(button);
  bReadings[bReadIndex] = bRaw;
  bTotal = bTotal + bReadings[bReadIndex];
  bReadIndex = bReadIndex + 1;

  // if we're at the end of the array...
  if (bReadIndex >= bNumReadings) {
    bReadIndex = 0;}

  // calculate the average:
  bAverage = bTotal / bNumReadings;

  if (bAverage >= buttonThreshold) {buttonState = true;}
  if (bAverage < buttonThreshold) {buttonState = false;}

  //if(currentTime - previousTime2 >= stepSize2) {

    
       
  //  previousTime2 = millis();
  //}
  
  if(currentTime - previousTime >= stepSize) {

    
    
    //Serial.print("- LeoPacket");
    //Serial.print('\t');
    Serial.print("Button: ");
    Serial.println(bRaw);
    Serial.print("Range: ");
    Serial.println(sensor.readRangeSingleMillimeters());
    //if (sensor.timeoutOccurred()) { Serial.print(" TIMEOUT"); }
    Serial.print("Lux: "); Serial.println(veml.readLux());
    Serial.print("White: "); Serial.println(veml.readWhite());
    Serial.print("Raw ALS: "); Serial.println(veml.readALS());

    if (bRaw < threshold){
      digitalWrite(LightPin, LOW);
    }

    if (bRaw >= threshold){
      digitalWrite(LightPin, HIGH);
    }
  
    /*
    uint16_t irq = veml.interruptStatus();
    if (irq & VEML7700_INTERRUPT_LOW) {
      Serial.println("** Low threshold"); 
    }
    if (irq & VEML7700_INTERRUPT_HIGH) {
      Serial.println("** High threshold"); 
    }
  
    Serial.println();
    */
    previousTime = millis();
  }
  //delay(500);
}
