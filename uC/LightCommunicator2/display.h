uint8_t ZIG(uint8_t in, uint8_t width){
  uint8_t j = 0; 
  uint8_t maths = in/width;
  if(maths%2){
    j = (width-1)+(width*maths) - (in-(width*maths));
  }
  else {j = in;}
  return j;
}

void DrawLines (int sequence[], uint8_t arLen, uint8_t brightness, uint8_t nums){

  for (uint8_t i = 0; i < arLen; i++){
    uint8_t j = ZIG(i,22);
    
    if (sequence[i] > 0){
      uint32_t thisColor = picker(sequence[i]);
      strip.setPixelColor(j, thisColor);
    }
  }
  if (nums != 5){ strip.setBrightness(brightness); }
  if (nums == 5){ strip.setBrightness(255); }
  //strip.show();
  if (nums == 5 or nums ==0){
    for (int k=0; k<strip.numPixels(); k++){
      uint8_t L = ZIG(k,22);
      if (sequence[k] == 0){
        strip.setPixelColor(L, strip.Color(0,0,0));
      }
    }
  }
  strip.show();
}
