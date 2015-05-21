#include <Servo.h>

Servo base;
int BASECENTER = 86; // more positive moves to the right
int BASERIGHT = BASECENTER+85;
int BASELEFT = BASECENTER-85;
Servo shoulder;
int SHOULDERCENTER = 95; // more positive moves backward
int SHOULDERDOWN = SHOULDERCENTER-79;
Servo elbow;
int ELBOWCENTER = 126; // more positive moves down
int ELBOWUP = ELBOWCENTER-90;
Servo wrist;
int WRISTCENTER = 95; // more positive flexes up
int WRISTDOWN = WRISTCENTER-82;

// Probably no calibration needed
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
    elbow.write(ELBOWCENTER);
    wrist.attach(9);
    wrist.write(WRISTCENTER);
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
