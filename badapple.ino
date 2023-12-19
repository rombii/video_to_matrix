#include "LedControl.h"
//  pin 12 is connected to the DataIn 
//  pin 11 is connected to the CLK 
//  pin 10 is connected to LOAD 
//  4 devices connected together
const byte sus[] =
{
0x00, 0x00, 0x00, 0x00, 0x0f, 0xf0, 0x0f, 0xf0, 0x0c, 0x0c, 0x0c, 0x0c, 0x3c, 0x0c, 0x3c, 0x0c, 0x3f, 0xfc, 0x3f, 0xfc, 0x3f, 0xfc, 0x3f, 0xfc, 0x0f, 0x3c, 0x0f, 0x3c, 0x0f, 0x3c, 0x0f, 0x3c
};
bool got_video = false;
LedControl lc=LedControl(12,11,10,4);

byte bytes[32];

void setup() {
  Serial.begin(9600);
  int devices=lc.getDeviceCount();
  for(int address=0;address<devices;address++) {
    lc.shutdown(address,false);
    lc.setIntensity(address,8);
    lc.clearDisplay(address);
  }
}

void loop() { 
  if (Serial.available()) {
    Serial.readBytes(bytes, 32);
    got_video = true;
    updateFrame(bytes);
    
  }
  else {
    if(!got_video) {
      updateFrame(sus);
    }
  }

}

void updateFrame(byte array[]) {
  lc.setRow(0, 0, array[0]);
  lc.setRow(0, 1, array[2]);
  lc.setRow(0, 2, array[4]);
  lc.setRow(0, 3, array[6]);
  lc.setRow(0, 4, array[8]);
  lc.setRow(0, 5, array[10]);
  lc.setRow(0, 6, array[12]);
  lc.setRow(0, 7, array[14]);

  lc.setRow(1, 0, array[1]);
  lc.setRow(1, 1, array[3]);
  lc.setRow(1, 2, array[5]);
  lc.setRow(1, 3, array[7]);
  lc.setRow(1, 4, array[9]);
  lc.setRow(1, 5, array[11]);
  lc.setRow(1, 6, array[13]);
  lc.setRow(1, 7, array[15]);

  lc.setRow(2, 0, array[16]);
  lc.setRow(2, 1, array[18]);
  lc.setRow(2, 2, array[20]);
  lc.setRow(2, 3, array[22]);
  lc.setRow(2, 4, array[24]);
  lc.setRow(2, 5, array[26]);
  lc.setRow(2, 6, array[28]);
  lc.setRow(2, 7, array[30]);

  lc.setRow(3, 0, array[17]);
  lc.setRow(3, 1, array[19]);
  lc.setRow(3, 2, array[21]);
  lc.setRow(3, 3, array[23]);
  lc.setRow(3, 4, array[25]);
  lc.setRow(3, 5, array[27]);
  lc.setRow(3, 6, array[29]);
  lc.setRow(3, 7, array[31]);
}

  

