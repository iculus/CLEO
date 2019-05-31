const int bNumReadings = 500;
int bReadings[bNumReadings];      // the readings from the analog input
int bReadIndex = 0;              // the index of the current reading
int bTotal = 0;                  // the running total
int bAverage = 0;                // the average
int button = A1;
int bRaw = 0;

const int sNumReadings = 2000;
int sReadings[sNumReadings];      // the readings from the analog input
int sReadIndex = 0;              // the index of the current reading
int sTotal = 0;                  // the running total
int sAverage = 0;                // the average
int slider = A2;
int sRaw = 0;

bool buttonState = false;
int buttonThreshold = 200;

int brightness = 0;
int sliderMin = 50;
int sliderMax = 850;

void averageInit(){  // initialize all the readings to 0:
  for (int bThisReading = 0; bThisReading < bNumReadings; bThisReading++) {
    bReadings[bThisReading] = 0;}
  for (int sThisReading = 0; sThisReading < sNumReadings; sThisReading++) {
    sReadings[sThisReading] = 0;}
}
