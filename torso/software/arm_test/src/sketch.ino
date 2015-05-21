#include <Servo.h>

Servo base;
int BASECENTER = 90;
Servo shoulder;
int SHOULDERCENTER = 90;
Servo elbow;
int ELBOWCENTER = 90;
Servo wrist;
int WRISTCENTER = 90;
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
