#include "BSSetup.h"

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);

  averageInit();
}

// the loop routine runs over and over again forever:
void loop() {
  bTotal = bTotal - bReadings[bReadIndex];
  bRaw = analogRead(button);
  bReadings[bReadIndex] = bRaw;
  bTotal = bTotal + bReadings[bReadIndex];
  bReadIndex = bReadIndex + 1;

  sTotal = sTotal - sReadings[sReadIndex];
  sRaw = analogRead(slider);
  sReadings[sReadIndex] = sRaw;
  sTotal = sTotal + sReadings[sReadIndex];
  sReadIndex = sReadIndex + 1;

  // if we're at the end of the array...
  if (bReadIndex >= bNumReadings) {
    bReadIndex = 0;}
  if (sReadIndex >= sNumReadings) {
    sReadIndex = 0;}

  // calculate the average:
  bAverage = bTotal / bNumReadings;
  sAverage = sTotal / sNumReadings;

  if (bAverage >= buttonThreshold) {buttonState = true;}
  if (bAverage < buttonThreshold) {buttonState = false;}

  sAverage = constrain(sAverage,sliderMin,sliderMax); 
  brightness = map(sAverage, sliderMin, sliderMax, 0, 100);
  
  Serial.print("Button: ");
  Serial.print(bRaw);
  Serial.print('\t');
  Serial.print(buttonState);
  Serial.print('\t');
  Serial.print("Slider: ");
  Serial.print(sRaw);
  Serial.print('\t');
  Serial.print(sAverage);
  Serial.print('\t');
  Serial.print("Brightness: ");
  Serial.print(brightness);
  Serial.print('\t');
  Serial.println();
}
