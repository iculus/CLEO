#define leds 22
#define rows 11

uint32_t thisColor;

#define NUMPIXELS leds*rows // Number of LEDs in strip
Adafruit_DotStar strip(NUMPIXELS, DOTSTAR_BRG);

uint32_t OFF = strip.Color(0,0,0);

uint32_t RED_2 = strip.Color(0,9,0);
uint32_t RED_3 = strip.Color(0,31,0);
uint32_t RED_4 = strip.Color(0,75,0);
uint32_t RED_5 = strip.Color(0,147,0);
uint32_t RED_6 = strip.Color(0,255,0);


uint32_t ORANGE_2 = strip.Color(3,9,0);
uint32_t ORANGE_3 = strip.Color(12,31,0);
uint32_t ORANGE_4 = strip.Color(29,75,0);
uint32_t ORANGE_5 = strip.Color(57,147,0);
uint32_t ORANGE_6 = strip.Color(100,255,0);


uint32_t YELLOW_2 = strip.Color(9,9,0);
uint32_t YELLOW_3 = strip.Color(31,31,0);
uint32_t YELLOW_4 = strip.Color(75,75,0);
uint32_t YELLOW_5 = strip.Color(147,147,0);
uint32_t YELLOW_6 = strip.Color(255,255,0);


uint32_t GREEN_2 = strip.Color(9,0,0);
uint32_t GREEN_3 = strip.Color(31,0,0);
uint32_t GREEN_4 = strip.Color(75,0,0);
uint32_t GREEN_5 = strip.Color(147,0,0);
uint32_t GREEN_6 = strip.Color(255,0,0);


uint32_t TEAL_2 = strip.Color(9,0,9);
uint32_t TEAL_3 = strip.Color(31,0,31);
uint32_t TEAL_4 = strip.Color(75,0,75);
uint32_t TEAL_5 = strip.Color(147,0,147);
uint32_t TEAL_6 = strip.Color(255,0,255);


uint32_t BLUE_2 = strip.Color(0,0,9);
uint32_t BLUE_3 = strip.Color(0,0,31);
uint32_t BLUE_4 = strip.Color(0,0,75);
uint32_t BLUE_5 = strip.Color(0,0,147);
uint32_t BLUE_6 = strip.Color(0,0,255);


uint32_t FUCHA_2 = strip.Color(0,9,3);
uint32_t FUCHA_3 = strip.Color(0,31,12);
uint32_t FUCHA_4 = strip.Color(0,75,29);
uint32_t FUCHA_5 = strip.Color(0,147,57);
uint32_t FUCHA_6 = strip.Color(0,255,100);


uint32_t PURPLE_2 = strip.Color(0,6,9);
uint32_t PURPLE_3 = strip.Color(0,21,31);
uint32_t PURPLE_4 = strip.Color(0,50,75);
uint32_t PURPLE_5 = strip.Color(0,98,147);
uint32_t PURPLE_6 = strip.Color(0,170,255);


uint32_t WHITE_2 = strip.Color(9,9,9);
uint32_t WHITE_3 = strip.Color(31,31,31);
uint32_t WHITE_4 = strip.Color(75,75,75);
uint32_t WHITE_5 = strip.Color(147,147,147);
uint32_t WHITE_6 = strip.Color(255,255,255);


uint32_t picker(int value){
  if (value == 0){thisColor = OFF;}
  if (value == 1){thisColor = PURPLE_6;}
  if (value == 2){thisColor = GREEN_6;}
  if (value == 3){thisColor = TEAL_6;}
  if (value == 4){thisColor = RED_6;}
  if (value == 5){thisColor = YELLOW_6;}
  if (value == 6){thisColor = FUCHA_6;}
  if (value == 7){thisColor = BLUE_6;}
  if (value == 8){thisColor = ORANGE_6;}
  if (value == 9){thisColor = WHITE_6;}
  if (value == 12) {thisColor = RED_2;}
  if (value == 13) {thisColor = RED_3;}
  if (value == 14) {thisColor = RED_4;}
  if (value == 15) {thisColor = RED_5;}
  if (value == 16) {thisColor = RED_6;}
  if (value == 22) {thisColor = ORANGE_2;}
  if (value == 23) {thisColor = ORANGE_3;}
  if (value == 24) {thisColor = ORANGE_4;}
  if (value == 25) {thisColor = ORANGE_5;}
  if (value == 26) {thisColor = ORANGE_6;}
  if (value == 32) {thisColor = YELLOW_2;}
  if (value == 33) {thisColor = YELLOW_3;}
  if (value == 34) {thisColor = YELLOW_4;}
  if (value == 35) {thisColor = YELLOW_5;}
  if (value == 36) {thisColor = YELLOW_6;}
  if (value == 42) {thisColor = GREEN_2;}
  if (value == 43) {thisColor = GREEN_3;}
  if (value == 44) {thisColor = GREEN_4;}
  if (value == 45) {thisColor = GREEN_5;}
  if (value == 46) {thisColor = GREEN_6;}
  if (value == 52) {thisColor = TEAL_2;}
  if (value == 53) {thisColor = TEAL_3;}
  if (value == 54) {thisColor = TEAL_4;}
  if (value == 55) {thisColor = TEAL_5;}
  if (value == 56) {thisColor = TEAL_6;}
  if (value == 62) {thisColor = BLUE_2;}
  if (value == 63) {thisColor = BLUE_3;}
  if (value == 64) {thisColor = BLUE_4;}
  if (value == 65) {thisColor = BLUE_5;}
  if (value == 66) {thisColor = BLUE_6;}
  if (value == 72) {thisColor = FUCHA_2;}
  if (value == 73) {thisColor = FUCHA_3;}
  if (value == 74) {thisColor = FUCHA_4;}
  if (value == 75) {thisColor = FUCHA_5;}
  if (value == 76) {thisColor = FUCHA_6;}
  if (value == 82) {thisColor = PURPLE_2;}
  if (value == 83) {thisColor = PURPLE_3;}
  if (value == 84) {thisColor = PURPLE_4;}
  if (value == 85) {thisColor = PURPLE_5;}
  if (value == 86) {thisColor = PURPLE_6;}
  /*
  if (value == 92) {thisColor = WHITE_2;}
  if (value == 93) {thisColor = WHITE_3;}
  if (value == 94) {thisColor = WHITE_4;}
  if (value == 95) {thisColor = WHITE_5;}
  if (value == 96) {thisColor = WHITE_6;}
  if (value > 96) {thisColor = WHITE_6;}
  */
  return thisColor;}
