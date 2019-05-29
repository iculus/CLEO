#include <Adafruit_DotStar.h>
#include <SPI.h>

#include "setup.h"
#include "message.h"
#include "colors.h"
#include "display.h"

void setup() {

  pinMode(LED_BUILTIN, OUTPUT);
  
  Serial.begin(115200);    // opens serial port, sets data rate to 9600 bps
  
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'

}

bool wasTrue = false;
bool condition = false;
int timer = millis();
// this number will make akward pauses, keep it as low as possible
int timeFilter = 30;

void loop() {
  
  //Init struct
  struct Message1 msg1;
  static char payload[MSG_LEN];
  static size_t num_payload_chars = MSG_LEN + 1;

  if (Serial.available() > 0)  {serAvail = true;}
  if (Serial.available() == 0) {serAvail = false;}

  //if serial available switched from true to false but it has only been a short time DONT update condition
  //if serial available switched from true to false some time ago DO update condition 
  //fi serial available switched from false to tru DO update condition immediately 

  if (serAvail == true) {
    wasTrue = true;
    condition = true;
    timer = millis();
  }

  if (serAvail == false and wasTrue == true) {
    //just switched 
    //if time has elapse set condition to false
    if (millis() - timer > timeFilter){
      condition = false;
      wasTrue = false; 
    }
  }

  if (serAvail == false and wasTrue == false){
    condition = false;
  }

  digitalWrite(LED_BUILTIN, serAvail);

  // send data only when you receive data:
  if (condition) {
    incomingByte = Serial.read();
    // accumilate enough bytes
    // look for start bytes
    // 
    // pull out the payload
  
    if (num_payload_chars == MSG_LEN + 1) {
      if (incomingByte == 255) {
        num_payload_chars = 0;
      }
    } else if (num_payload_chars < MSG_LEN) {
      payload[num_payload_chars] = incomingByte;
      num_payload_chars++;
    } else if (num_payload_chars == MSG_LEN) {
      if (incomingByte == 254) {
        Serial.println("okay");
        //process message
        memcpy(&msg1, payload, sizeof(msg1));
        
        handleMessage(msg1);
        
        num_payload_chars = MSG_LEN + 1;
      } else {
        Serial.print("dropper");
        Serial.print(MSG_LEN);
        Serial.println(incomingByte);
        num_payload_chars = MSG_LEN + 1;  // invalid packet, drop data
        
      }
    } else {
      Serial.println("strange spot");
      //assert(false);
    }    
  }
  else if(not condition) {
    checkTime = millis();
    row = random(0,rows);
    col = random(0,leds);
    sz = random(1,4+1);
    
    if (checkTime-startTime>=1000){
      DrawCircle(row,col,15, sz, YELLOW_6); // row,col,wait,size(1=small,4=large), color
      startTime = checkTime;
    }
  }
}

void handleMessage(struct Message1 msg1){

  uint8_t numFing = msg1.bit242;
  uint8_t brights = msg1.bit243;
  
  int seq[] = {  msg1.bit0,  msg1.bit1,  msg1.bit2,  msg1.bit3,  msg1.bit4,  msg1.bit5,  msg1.bit6,  msg1.bit7,  msg1.bit8,  msg1.bit9,  msg1.bit10, msg1.bit11, msg1.bit12, msg1.bit13, msg1.bit14, msg1.bit15, msg1.bit16, msg1.bit17, msg1.bit18, msg1.bit19, msg1.bit20, msg1.bit21,
      msg1.bit22, msg1.bit23, msg1.bit24, msg1.bit25, msg1.bit26, msg1.bit27, msg1.bit28, msg1.bit29, msg1.bit30, msg1.bit31, msg1.bit32, msg1.bit33, msg1.bit34, msg1.bit35, msg1.bit36, msg1.bit37, msg1.bit38, msg1.bit39, msg1.bit40, msg1.bit41, msg1.bit42, msg1.bit43,
      msg1.bit44, msg1.bit45, msg1.bit46, msg1.bit47, msg1.bit48, msg1.bit49, msg1.bit50, msg1.bit51, msg1.bit52, msg1.bit53, msg1.bit54, msg1.bit55, msg1.bit56, msg1.bit57, msg1.bit58, msg1.bit59, msg1.bit60, msg1.bit61, msg1.bit62, msg1.bit63, msg1.bit64, msg1.bit65,
      msg1.bit66, msg1.bit67, msg1.bit68, msg1.bit69, msg1.bit70, msg1.bit71, msg1.bit72, msg1.bit73, msg1.bit74, msg1.bit75, msg1.bit76, msg1.bit77, msg1.bit78, msg1.bit79, msg1.bit80, msg1.bit81, msg1.bit82, msg1.bit83, msg1.bit84, msg1.bit85, msg1.bit86, msg1.bit87,
      msg1.bit88, msg1.bit89, msg1.bit90, msg1.bit91, msg1.bit92, msg1.bit93, msg1.bit94, msg1.bit95, msg1.bit96, msg1.bit97, msg1.bit98, msg1.bit99, msg1.bit100,  msg1.bit101,  msg1.bit102,  msg1.bit103,  msg1.bit104,  msg1.bit105,  msg1.bit106,  msg1.bit107,  msg1.bit108,  msg1.bit109,
      msg1.bit110,  msg1.bit111,  msg1.bit112,  msg1.bit113,  msg1.bit114,  msg1.bit115,  msg1.bit116,  msg1.bit117,  msg1.bit118,  msg1.bit119,  msg1.bit120,  msg1.bit121,  msg1.bit122,  msg1.bit123,  msg1.bit124,  msg1.bit125,  msg1.bit126,  msg1.bit127,  msg1.bit128,  msg1.bit129,  msg1.bit130,  msg1.bit131,
      msg1.bit132,  msg1.bit133,  msg1.bit134,  msg1.bit135,  msg1.bit136,  msg1.bit137,  msg1.bit138,  msg1.bit139,  msg1.bit140,  msg1.bit141,  msg1.bit142,  msg1.bit143,  msg1.bit144,  msg1.bit145,  msg1.bit146,  msg1.bit147,  msg1.bit148,  msg1.bit149,  msg1.bit150,  msg1.bit151,  msg1.bit152,  msg1.bit153,
      msg1.bit154,  msg1.bit155,  msg1.bit156,  msg1.bit157,  msg1.bit158,  msg1.bit159,  msg1.bit160,  msg1.bit161,  msg1.bit162,  msg1.bit163,  msg1.bit164,  msg1.bit165,  msg1.bit166,  msg1.bit167,  msg1.bit168,  msg1.bit169,  msg1.bit170,  msg1.bit171,  msg1.bit172,  msg1.bit173,  msg1.bit174,  msg1.bit175,
      msg1.bit176,  msg1.bit177,  msg1.bit178,  msg1.bit179,  msg1.bit180,  msg1.bit181,  msg1.bit182,  msg1.bit183,  msg1.bit184,  msg1.bit185,  msg1.bit186,  msg1.bit187,  msg1.bit188,  msg1.bit189,  msg1.bit190,  msg1.bit191,  msg1.bit192,  msg1.bit193,  msg1.bit194,  msg1.bit195,  msg1.bit196,  msg1.bit197,
      msg1.bit198,  msg1.bit199,  msg1.bit200,  msg1.bit201,  msg1.bit202,  msg1.bit203,  msg1.bit204,  msg1.bit205,  msg1.bit206,  msg1.bit207,  msg1.bit208,  msg1.bit209,  msg1.bit210,  msg1.bit211,  msg1.bit212,  msg1.bit213,  msg1.bit214,  msg1.bit215,  msg1.bit216,  msg1.bit217,  msg1.bit218,  msg1.bit219,
      msg1.bit220,  msg1.bit221,  msg1.bit222,  msg1.bit223,  msg1.bit224,  msg1.bit225,  msg1.bit226,  msg1.bit227,  msg1.bit228,  msg1.bit229,  msg1.bit230,  msg1.bit231,  msg1.bit232,  msg1.bit233,  msg1.bit234,  msg1.bit235,  msg1.bit236,  msg1.bit237,  msg1.bit238,  msg1.bit239,  msg1.bit240,  msg1.bit241};

  DrawLines(seq, seqLen, brights, numFing); //onOff vals, len, color, brightness

  //uncomment below to send the list to the serial terminal
  //for (int indx = 0; indx < (sizeof(seq)/sizeof(seq[0])); indx ++){
  //  Serial.print(seq[indx]);
  //}
}

#define ARRAY_LEN(a)    (sizeof(a) / sizeof(a[0]))

uint16_t TransformMatrix(uint16_t row, uint16_t col) {
  // 0,0 is bottom left
  //row = Wrap(row,rows);
  //col = Wrap(col,leds);
  uint16_t ColAdder;
  if (row%2 == 1) {
    ColAdder = leds-col-1;
  }
  else {
    ColAdder = col;
  }
  return row*leds + ColAdder;
}

void SetPixelMatrix(uint16_t row, uint16_t col, uint32_t c) {
  uint16_t i = TransformMatrix(row, col);
  strip.setPixelColor(i, c);
}

void DrawCircle(uint16_t row, uint16_t col, uint8_t wait, uint16_t condition, uint32_t colr) {
  static int xx4[] = {-3,-3,-2,-1,0,1,2,3,3,3,2,1,0,-1,-2,-3};
  static int yy4[] = {0,1,2,3,3,3,2,1,0,-1,-2,-3,-3,-3,-2,-1};
  static int xx3[] = {-1,0,1,2,2,2,1,0,-1,-2,-2,-2};
  static int yy3[] = {2,2,2,1,0,-1,-2,-2,-2,-1,0,1};
  static int xx2[] = {-1,-1,0,1,1,1,0,-1};
  static int yy2[] = {0,1,1,1,0,-1,-1,-1};
  static int xx1[] = {0};
  static int yy1[] = {0};
  
  for (int b = 0; b <= 100; b++) {
    if (b==0){
      for (int i=0; i<22*11; i++){
        strip.setPixelColor(i,strip.Color(0,0,0));
      }
    }
    if (condition >= 4) {addressShape(xx4,yy4,row,col,ARRAY_LEN(xx4),strip.Color( 0,255,255 ));}
    if (condition >= 3) {addressShape(xx3,yy3,row,col,ARRAY_LEN(xx3),strip.Color( 0,0,255 ));}
    if (condition >= 2) {addressShape(xx2,yy2,row,col,ARRAY_LEN(xx2),strip.Color( 0,255,0 ));}
    if (condition >= 1) {addressShape(xx1,yy1,row,col,ARRAY_LEN(xx1),colr);}
    strip.setBrightness( 255/50 * (50-abs(50-b)) ); //sets the triangle
    strip.show();
    delay(wait);
  }
}


void addressShape(int* xArray, int* yArray, uint8_t thisrow, uint8_t thiscol, uint8_t arraylen,uint32_t c){
  for (uint8_t dot=0; dot < arraylen; dot++) {
    if ((xArray[dot]+thisrow)>=0 && (yArray[dot]+thiscol)>=0 && (xArray[dot]+thisrow)<rows && (yArray[dot]+thiscol)<leds) {
      SetPixelMatrix(xArray[dot]+thisrow,yArray[dot]+thiscol, c);
    }
  }
}
