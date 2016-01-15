/*
Arduino Hall Effect Sensor Project
by Arvind Sanjeev
Please check out  http://diyhacking.com for the tutorial of this project.
DIY Hacking
*/

#include "Timer.h"

Timer t;
int pin = 13;

 volatile byte half_revolutions;
 unsigned int rpm;
 unsigned long timeold;
 void setup()
 {
   Serial.begin(115200);
   attachInterrupt(0, magnet_detect, RISING);//Initialize the intterrupt pin (Arduino digital pin 2)
   half_revolutions = 0;
   rpm = 0;
   timeold = 0;
 }
 void loop()//Measure RPM
 {
   //Serial.println(millis() - timeold);
   
 }
 
 void magnet_detect()//This function is called whenever a magnet/interrupt is detected by the arduino
 {
   //Serial.println("detect");
   
   Serial.println(millis() - timeold);
   timeold = millis();
   
 }
