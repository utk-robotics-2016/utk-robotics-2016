#include <Servo.h>

Servo base;
int BASECENTER = 89; // more positive moves to the right
Servo shoulder;
int SHOULDERCENTER = 95; // more positive moves backward
Servo elbow;
int ELBOWCENTER = 126; // more positive moves down
int ELBOWUP = ELBOWCENTER-90; // more positive moves down
Servo wrist;
int WRISTCENTER = 95; // more positive flexes up
int WRISTDOWN = WRISTCENTER-82;
Servo wristrotate;
int WRISTROTATECENTER = 90;
Servo suction;
int SUCTIONCENTER = 90;

void setup()
{
    base.attach(3);
    base.write(BASECENTER);
    shoulder.attach(5);
    shoulder.write(SHOULDERCENTER);
    elbow.attach(6);
    /*elbow.write(ELBOWCENTER);*/
    elbow.write(ELBOWUP);
    wrist.attach(9);
    wrist.write(WRISTCENTER);
    /*wrist.write(WRISTDOWN);*/
    wristrotate.attach(10);
    wristrotate.write(WRISTROTATECENTER);
    suction.attach(11);
    suction.write(SUCTIONCENTER);
}


void loop()
{
    //base.write(90);
    //base.write(90);
}
