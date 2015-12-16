  #define address 0x1E //0011110b, I2C 7bit address of HMC5883
#include <Wire.h>
#include <math.h>
#include "gp2d12_ir.h"

#include <LiquidCrystalFast.h>

LiquidCrystalFast lcd(12, 10, 11, 5, 4, 3, 2);
void setup(){
  //Initialize Serial and I2C communications
  Wire.begin();

  lcd.begin(16, 2);
  init_ir(A1); //Init Sharp GP2D12 IR Rangefinder
  // Print a message to the LCD.

  //Put the HMC5883 IC into the correct operating mode
  Wire.beginTransmission(address); //open communication with HMC5883
  Wire.write(0x02); //select mode register
  Wire.write(0x00); //continuous measurement mode
  Wire.endTransmission();
}

void loop(){

  int x,y,z; //triple axis data
  double heading;

  lcd.setCursor(0, 1);
  // print the number of seconds since reset:

  //Tell the HMC5883L where to begin reading data
  Wire.beginTransmission(address);
  Wire.write(0x03); //select register 3, X MSB register
  Wire.endTransmission();


  //Read data from each axis, 2 registers per axis
  Wire.requestFrom(address, 6);
  if(6<=Wire.available()){
    x = Wire.read()<<8; //X msb
    x |= Wire.read(); //X lsb
    z = Wire.read()<<8; //Z msb
    z |= Wire.read(); //Z lsb
    y = Wire.read()<<8; //Y msb
    y |= Wire.read(); //Y lsb
  }


  //Convert azimuth to degrees
  if (x <= 0) {
    if (x < 0) {
      heading = 180 - atan2(y,x)*(57.32);
    } 
    else {
      if (y < 0) {
        heading = 90;
      } 
      else {
        heading = 270;
      }
    }
  } 
  else {
    if (y < 0) {
      heading = -1 * atan2(y,x)*(57.32);
    } 
    else {
      heading = 360 - atan2(y,x)*(57.32);
    }
  }  
  
  //Print out values of each axis
  lcd.setCursor(0,0);
  lcd.print(x);
  lcd.print(",");
  lcd.print(y);
  lcd.print(";D:");
  lcd.print(heading);
  lcd.setCursor(0, 1);
  //lcd.print("x: ");
  //lcd.print(x);
  //lcd.print("  y: ");
  //lcd.print(y);
  //lcd.print("  z: ");
  //lcd.println(z);
  lcd.print("Rng:");
  lcd.print(read_ir(A1));


  delay(250);
}

