
#define interrupt 4
#define colorLED 5

uint16_t row = 0;
uint16_t col = 0;
uint16_t sz = 0;
uint16_t finger = 0;
uint8_t numFingers = 0;

uint8_t incomingByte = 0;    // for incoming serial data

bool serAvail = false;
//bool closeToIt = false;
//uint8_t threshold = 100;
uint8_t i = 0;

unsigned long startTime = millis();
unsigned long checkTime = millis();

uint8_t seqLen = 22*11;
