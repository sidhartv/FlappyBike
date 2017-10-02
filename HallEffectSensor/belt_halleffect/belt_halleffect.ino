/*
Arduino Hall Effect Sensor Project
by Arvind Sanjeev
Please check out  http://diyhacking.com for the tutorial of this project.
DIY Hacking
*/

//#include "Timer.h"

//Timer t;
int pin = 13;

 volatile byte half_revolutions;
 unsigned int rpm;
 unsigned long timeold;
 void setup()
 {
   Serial.begin(9600);
   attachInterrupt(0, magnet_detect, RISING);//Initialize the interrupt pin (Arduino digital pin 2)
   
   half_revolutions = 0;
   rpm = 500;
   timeold = 0;
 }
 void loop()//Measure RPM
 {
   
   /*rpm+=80;
   if (rpm > 1500) { rpm = 500; }
   delay(250);
   Serial.println(rpm); */
   
 }
 
 void magnet_detect()//This function is called whenever a magnet/interrupt is detected by the arduino
 {
   //Serial.println("detect");
   
   Serial.println(millis() - timeold);
   timeold = millis();
   
 }
