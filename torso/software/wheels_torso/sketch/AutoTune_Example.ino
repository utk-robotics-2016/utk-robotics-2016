#include <Servo.h>
#include <Wire.h>
#include <I2CEncoder.h>
#include "../vPID.h"
#include "../vPID_AutoTune.h"

const char CH1_PWM = 24;
const char CH1_DIR = 20;
const char CH1_CUR = 38;
const char CH2_PWM = 25;
const char CH2_DIR = 21;
const char CH2_CUR = 39;
const char CH3_PWM = 26;
const char CH3_DIR = 22;
const char CH3_CUR = 40;
const char CH4_PWM = 14;
const char CH4_DIR = 23;
const char CH4_CUR = 41;

// For encoders:
I2CEncoder encoders[4];
#define REAR_LEFT_ENC 0
#define REAR_RIGHT_ENC 1
#define FRONT_RIGHT_ENC 2
#define FRONT_LEFT_ENC 3

byte ATuneModeRemember=2;
double input=80, output=50, setpoint=180;
double kp=2,ki=0.5,kd=2;

double kpmodel=1.5, taup=100, theta[50];
double outputStart=5;
double aTuneStep=50, aTuneNoise=1, aTuneStartValue=100;
unsigned int aTuneLookBack=20;

boolean tuning = false;
unsigned long  modelTime, serialTime;

PID myPID(&input, &output, &setpoint,kp,ki,kd, DIRECT);
PID_ATune aTune(&input, &output);

//set to false to connect to the real world
boolean useSimulation = true;

void setup()
{
    // Init Rover 5 pins
    pinMode(CH1_PWM,OUTPUT);
    pinMode(CH1_DIR,OUTPUT);
    pinMode(CH1_CUR,INPUT);
    pinMode(CH2_PWM,OUTPUT);
    pinMode(CH2_DIR,OUTPUT);
    pinMode(CH2_CUR,INPUT);
    pinMode(CH3_PWM,OUTPUT);
    pinMode(CH3_DIR,OUTPUT);
    pinMode(CH3_CUR,INPUT);
    pinMode(CH4_PWM,OUTPUT);
    pinMode(CH4_DIR,OUTPUT);
    pinMode(CH4_CUR,INPUT);

        Wire.begin();
    // From the docs: you must call the init() of each encoder method in the
    // order that they are chained together. The one plugged into the Arduino
    // first, then the one plugged into that and so on until the last encoder.
    encoders[REAR_LEFT_ENC].init(MOTOR_393_TORQUE_ROTATIONS, MOTOR_393_TIME_DELTA);
    encoders[REAR_RIGHT_ENC].init(MOTOR_393_TORQUE_ROTATIONS, MOTOR_393_TIME_DELTA);
    encoders[FRONT_RIGHT_ENC].init(MOTOR_393_TORQUE_ROTATIONS, MOTOR_393_TIME_DELTA);
    encoders[FRONT_LEFT_ENC].init(MOTOR_393_TORQUE_ROTATIONS, MOTOR_393_TIME_DELTA);
    // Ideally, moving forward should count as positive rotation.
    // Make this happen:
    encoders[REAR_RIGHT_ENC].setReversed(true);
    encoders[FRONT_RIGHT_ENC].setReversed(true);

  //Setup the pid 
  myPID.SetMode(AUTOMATIC);

  if(tuning)
  {
    tuning=false;
    changeAutoTune();
    tuning=true;
  }
  
  serialTime = 0;
  Serial.begin(9600);

}

void loop()
{

  unsigned long now = millis();


  input = encoders[REAR_LEFT_ENC].getSpeed();
  
  
  if(tuning)
  {
    byte val = (aTune.Runtime());
    if (val!=0)
    {
      tuning = false;
    }
    if(!tuning)
    { //we're done, set the tuning parameters
      kp = aTune.GetKp();
      ki = aTune.GetKi();
      kd = aTune.GetKd();
      myPID.SetTunings(kp,ki,kd);
      AutoTuneHelper(false);
    }
  }
  else myPID.Compute();
  
  
  analogWrite(CH1_PWM,abs(output));
  digitalWrite(CH1_DIR, output > 0); 
  
  
  //send-receive with processing if it's time
  if(millis()>serialTime)
  {
    SerialReceive();
    SerialSend();
    serialTime+=500;
  }
}

void changeAutoTune()
{
 if(!tuning)
  {
    //Set the output to the desired starting frequency.
    output=aTuneStartValue;
    aTune.SetNoiseBand(aTuneNoise);
    aTune.SetOutputStep(aTuneStep);
    aTune.SetLookbackSec((int)aTuneLookBack);
    AutoTuneHelper(true);
    tuning = true;
  }
  else
  { //cancel autotune
    aTune.Cancel();
    tuning = false;
    AutoTuneHelper(false);
  }
}

void AutoTuneHelper(boolean start)
{
  if(start)
    ATuneModeRemember = myPID.GetMode();
  else
    myPID.SetMode(ATuneModeRemember);
}


void SerialSend()
{
  Serial.print("setpoint: ");Serial.print(setpoint); Serial.print(" ");
  Serial.print("input: ");Serial.print(input); Serial.print(" ");
  Serial.print("output: ");Serial.print(output); Serial.print(" ");
  if(tuning){
    Serial.println("tuning mode");
  } else {
    Serial.print("kp: ");Serial.print(myPID.GetKp());Serial.print(" ");
    Serial.print("ki: ");Serial.print(myPID.GetKi());Serial.print(" ");
    Serial.print("kd: ");Serial.print(myPID.GetKd());Serial.println();
  }
}

void SerialReceive()
{
  if(Serial.available())
  {
   char b = Serial.read(); 
   Serial.flush(); 
   if((b=='1' && !tuning) || (b!='1' && tuning))changeAutoTune();
  }
}

void DoModel()
{
  //cycle the dead time
  for(byte i=0;i<49;i++)
  {
    theta[i] = theta[i+1];
  }
  //compute the input
  input = (kpmodel / taup) *(theta[0]-outputStart) + input*(1-1/taup) + ((float)random(-10,10))/100;

}
