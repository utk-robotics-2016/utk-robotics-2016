#include <Servo.h>
#include <Wire.h>
#include "I2CEncoder.h"
#include "PID.h"
#include "vPID.h"

// Globals
int ledState = HIGH;
// Command parsing
const int MAX_ARGS = 4;
String args[MAX_ARGS];
int numArgs = 0;

// For motor driver:
#define BRAKEVCC 0
#define FW   1
#define BW  2
#define BRAKEGND 3

// Pin definitions
const char LED = A1;
const char CH1_PWM = 3;  // Rear Left
const char CH1_DIR = 2;
const char CH1_CUR = 4;
const char CH2_PWM = 5;  // Front Left
const char CH2_DIR = A3;
const char CH2_CUR = A2;
const char CH3_PWM = 11;  // Front Right
const char CH3_DIR = 7;
const char CH3_CUR = 8;
const char CH4_PWM = 9;  // Rear Right
const char CH4_DIR = 12;
const char CH4_CUR = 13;

// For encoders:
I2CEncoder encoders[4];
#define REAR_LEFT_ENC 0
#define REAR_RIGHT_ENC 1
#define FRONT_RIGHT_ENC 2
#define FRONT_LEFT_ENC 3

// vPIDs:
double lastPositions[4];
double Inputs[4], Setpoints[4], Outputs[4];
vPID pidRL(&Inputs[REAR_LEFT_ENC], &Outputs[REAR_LEFT_ENC], &Setpoints[REAR_LEFT_ENC], .1, 0, 0, DIRECT);
vPID pidRR(&Inputs[REAR_RIGHT_ENC], &Outputs[REAR_RIGHT_ENC], &Setpoints[REAR_RIGHT_ENC], .1, 0, 0, DIRECT);
vPID pidFR(&Inputs[FRONT_RIGHT_ENC], &Outputs[FRONT_RIGHT_ENC], &Setpoints[FRONT_RIGHT_ENC], .1, 0, 0, DIRECT);
vPID pidFL(&Inputs[FRONT_LEFT_ENC], &Outputs[FRONT_LEFT_ENC], &Setpoints[FRONT_LEFT_ENC], .1, 0, 0, DIRECT);
vPID pids[4] = {pidRL, pidRR, pidFR, pidFL};

void setup() {
  // Init LED pin
  pinMode(LED, OUTPUT);
  // Init Rover 5 pins
  pinMode(CH1_PWM, OUTPUT);
  pinMode(CH1_DIR, OUTPUT);
  pinMode(CH1_CUR, INPUT);
  pinMode(CH2_PWM, OUTPUT);
  pinMode(CH2_DIR, OUTPUT);
  pinMode(CH2_CUR, INPUT);
  pinMode(CH3_PWM, OUTPUT);
  pinMode(CH3_DIR, OUTPUT);
  pinMode(CH3_CUR, INPUT);
  pinMode(CH4_PWM, OUTPUT);
  pinMode(CH4_DIR, OUTPUT);
  pinMode(CH4_CUR, INPUT);

  // Init serial
  Serial.begin(115200);

  Wire.begin();
  
  // Delay to allow mega time to start up and power on the encoders
  long t = millis();
  while(millis() - t < 200);
  
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
  encoders[REAR_LEFT_ENC].zero();
  encoders[REAR_RIGHT_ENC].zero();
  encoders[FRONT_RIGHT_ENC].zero();
  encoders[FRONT_LEFT_ENC].zero();
  for (int i = 0; i < 4; i++)
  {
    Inputs[i] = 0.0;
    Setpoints[i] = 0.0;
    Outputs[i] = 0.0;
    lastPositions[i] = 0.0;
    pids[i].SetMode(AUTOMATIC);
  }
  // Display ready LED
  digitalWrite(LED, HIGH);
}

/* The loop is set up in two parts. First the Arduino does the work it needs to
 * do for every loop, next is runs the checkInput() routine to check and act on
 * any input from the serial connection.
 */
void loop() {
  // Accept and parse serial input
  checkInput();
  updatePID();
}

void parse_args(String command) {
  numArgs = 0;
  int beginIdx = 0;
  int idx = command.indexOf(" ");

  String arg;

  while (idx != -1)
  {
    arg = command.substring(beginIdx, idx);

    // add error handling for atoi:
    args[numArgs++] = arg;
    beginIdx = idx + 1;
    idx = command.indexOf(" ", beginIdx);
  }

  arg = command.substring(beginIdx);
  args[numArgs++] = arg;
}

/* This routine checks for any input waiting on the serial line. If any is
 * available it is read in and added to a 128 character buffer. It sends back
 * an error should the buffer overflow, and starts overwriting the buffer
 * at that point. It only reads one character per call. If it receives a
 * newline character is then runs the parseAndExecuteCommand() routine.
 */
void checkInput() {
  int inbyte;
  static char incomingBuffer[64];
  static char bufPosition = 0;

  if (Serial.available() > 0) {
    // Read only one character per call
    inbyte = Serial.read();
    //Serial.write(inbyte);
    if (inbyte == 10 || inbyte == 13) {
      // Newline detected
      incomingBuffer[bufPosition] = '\0'; // NULL terminate the string
      bufPosition = 0; // Prepare for next command

      // Supply a separate routine for parsing the command. This will
      // vary depending on the task.
      parseAndExecuteCommand(String(incomingBuffer));
    }
    else {
      incomingBuffer[bufPosition] = (char)inbyte;
      bufPosition++;
      if (bufPosition == 128) {
        Serial.println(F("error: command overflow"));
        bufPosition = 0;
      }
    }
  }
}


/* This routine parses and executes any command received. It will have to be
 * rewritten for any sketch to use the appropriate commands and arguments for
 * the program you design. I find it easier to separate the input assembly
 * from parsing so that I only have to modify this function and can keep the
 * checkInput() function the same in each sketch.
 */
void parseAndExecuteCommand(String command) {
  Serial.println("> " + command);
  parse_args(command);
  if (args[0].equals(String("ping"))) {
    if (numArgs == 1) {
      Serial.println("ok");
    } else {
      Serial.println(F("error: usage - 'ping'"));
    }
  }
  else if (args[0].equals(String("le"))) { // led set
    if (numArgs == 2) {
      if (args[1].equals(String("on"))) {
        ledState = HIGH;
        digitalWrite(LED, HIGH);
        Serial.println(F("ok"));
      } else if (args[1].equals(String("off"))) {
        ledState = LOW;
        digitalWrite(LED, LOW);
        Serial.println(F("ok"));
      } else {
        Serial.println(F("error: usage - 'le [on/off]'"));
      }
    } else {
      Serial.println(F("error: usage - 'le [on/off]'"));
    }
  }
  else if (args[0].equals(String("ma"))) { //move laterally left
    if (numArgs == 1) {
      for (int i = 0; i < 4; i++)
      {
        pids[i].SetMode(MANUAL);
      }
      digitalWrite(CH2_DIR, HIGH);
      analogWrite(CH2_PWM, 128);
      digitalWrite(CH3_DIR, LOW);
      analogWrite(CH3_PWM, 128);
      digitalWrite(CH1_DIR, HIGH);
      analogWrite(CH1_PWM, 128);
      digitalWrite(CH4_DIR, LOW);
      analogWrite(CH4_PWM, 128);
      delay(100);
      analogWrite(CH1_PWM, 0);
      analogWrite(CH2_PWM, 0);
      analogWrite(CH3_PWM, 0);
      analogWrite(CH4_PWM, 0);
      Serial.println("ok");
    } else {
      Serial.println(F("error: usage - 'ma'"));
    }
  }
  else if (args[0].equals(String("md"))) { //move laterally right
    if (numArgs == 1) {
      for (int i = 0; i < 4; i++)
      {
        pids[i].SetMode(MANUAL);
      }
      digitalWrite(CH2_DIR, LOW);
      analogWrite(CH2_PWM, 128);
      digitalWrite(CH3_DIR, HIGH);
      analogWrite(CH3_PWM, 128);
      digitalWrite(CH1_DIR, LOW);
      analogWrite(CH1_PWM, 128);
      digitalWrite(CH4_DIR, HIGH);
      analogWrite(CH4_PWM, 128);
      delay(100);
      analogWrite(CH1_PWM, 0);
      analogWrite(CH2_PWM, 0);
      analogWrite(CH3_PWM, 0);
      analogWrite(CH4_PWM, 0);
      Serial.println("ok");
    } else {
      Serial.println(F("error: usage - 'md'"));
    }
  }
  else if (args[0].equals(String("mw"))) { //move laterally forward
    if (numArgs == 1) {
      for (int i = 0; i < 4; i++)
      {
        pids[i].SetMode(MANUAL);
      }
      digitalWrite(CH2_DIR, LOW);
      analogWrite(CH2_PWM, 128);
      digitalWrite(CH3_DIR, LOW);
      analogWrite(CH3_PWM, 128);
      digitalWrite(CH1_DIR, HIGH);
      analogWrite(CH1_PWM, 128);
      digitalWrite(CH4_DIR, HIGH);
      analogWrite(CH4_PWM, 128);
      delay(100);
      analogWrite(CH1_PWM, 0);
      analogWrite(CH2_PWM, 0);
      analogWrite(CH3_PWM, 0);
      analogWrite(CH4_PWM, 0);
      Serial.println("ok");
    } else {
      Serial.println(F("error: usage - 'mw'"));
    }
  }
  else if (args[0].equals(String("ms"))) { //move laterally backward
    if (numArgs == 1) {
      for (int i = 0; i < 4; i++)
      {
        pids[i].SetMode(MANUAL);
      }
      digitalWrite(CH2_DIR, HIGH);
      analogWrite(CH2_PWM, 128);
      digitalWrite(CH3_DIR, HIGH);
      analogWrite(CH3_PWM, 128);
      digitalWrite(CH1_DIR, LOW);
      analogWrite(CH1_PWM, 128);
      digitalWrite(CH4_DIR, LOW);
      analogWrite(CH4_PWM, 128);
      delay(100);
      analogWrite(CH1_PWM, 0);
      analogWrite(CH2_PWM, 0);
      analogWrite(CH3_PWM, 0);
      analogWrite(CH4_PWM, 0);
      Serial.println("ok");
    } else {
      Serial.println(F("error: usage - 'ms'"));
    }
  }
  else if (args[0].equals(String("rl"))) { // read led
    if (numArgs == 1) {
      Serial.println(ledState);
    } else {
      Serial.println(F("error: usage - 'rl'"));
    }
  }
  else if (args[0].equals(String("go"))) {
    if (numArgs == 4) {
      for (int i = 0; i < 4; i++)
      {
        pids[i].SetMode(MANUAL);
      }

      int speed = args[2].toInt();

      boolean dir = LOW;
      if (args[3].equals(String("ccw"))) {
        dir = HIGH;
      }

      if (args[1].equals(String("1"))) {
        analogWrite(CH1_PWM, speed);
        digitalWrite(CH1_DIR, dir);
        Serial.println("ok");
      } else if (args[1].equals(String("2"))) {
        analogWrite(CH2_PWM, speed);
        digitalWrite(CH2_DIR, dir);
        Serial.println("ok");
      } else if (args[1].equals(String("3"))) {
        analogWrite(CH3_PWM, speed);
        digitalWrite(CH3_DIR, dir);
        Serial.println("ok");
      } else if (args[1].equals(String("4"))) {
        analogWrite(CH4_PWM, speed);
        digitalWrite(CH4_DIR, dir);
        Serial.println("ok");
      }
    } else {
      Serial.println(F("error: usage - 'go [1/2/3/4] [speed] [cw/ccw]'"));
    }
  }
  else if (args[0].equals(String("ep"))) { // encoder position (in rotations)
    if (numArgs == 1) {
      String ret = "";
      char dts[256];
      dtostrf(encoders[REAR_LEFT_ENC].getPosition(), 0, 6, dts);
      ret += dts;
      ret += " ";
      dtostrf(encoders[REAR_RIGHT_ENC].getPosition(), 0, 6, dts);
      ret += dts;
      ret += " ";
      dtostrf(encoders[FRONT_RIGHT_ENC].getPosition(), 0, 6, dts);
      ret += dts;
      ret += " ";
      dtostrf(encoders[FRONT_LEFT_ENC].getPosition(), 0, 6, dts);
      ret += dts;
      Serial.println(ret);
    } else {
      Serial.println(F("error: usage - 'ep'"));
    }
  }
  else if (args[0].equals(String("erp"))) { // encoder raw position (in ticks)
    if (numArgs == 1) {
      String ret = "";
      char dts[256];
      dtostrf(encoders[REAR_LEFT_ENC].getRawPosition(), 0, 6, dts);
      ret += dts;
      ret += " ";
      dtostrf(encoders[REAR_RIGHT_ENC].getRawPosition(), 0, 6, dts);
      ret += dts;
      ret += " ";
      dtostrf(encoders[FRONT_RIGHT_ENC].getRawPosition(), 0, 6, dts);
      ret += dts;
      ret += " ";
      dtostrf(encoders[FRONT_LEFT_ENC].getRawPosition(), 0, 6, dts);
      ret += dts;
      Serial.println(ret);
    } else {
      Serial.println(F("error: usage - 'erp'"));
    }
  }
  else if (args[0].equals(String("es"))) { // encoder speed (in revolutions per minute)
    if (numArgs == 1) {
      String ret = "";
      char dts[256];
      dtostrf(encoders[REAR_LEFT_ENC].getSpeed(), 0, 6, dts);
      ret += dts;
      ret += " ";
      dtostrf(encoders[REAR_RIGHT_ENC].getSpeed(), 0, 6, dts);
      ret += dts;
      ret += " ";
      dtostrf(encoders[FRONT_RIGHT_ENC].getSpeed(), 0, 6, dts);
      ret += dts;
      ret += " ";
      dtostrf(encoders[FRONT_LEFT_ENC].getSpeed(), 0, 6, dts);
      ret += dts;
      Serial.println(ret);
    } else {
      Serial.println(F("error: usage - 'es'"));
    }
  }
  else if (args[0].equals(String("ez"))) { // encoder zero
    if (numArgs == 1)
    {
      for (int i = 0; i < 4; i++) {
        encoders[i].zero(); 
      }
      Serial.println(F("ok"));
    } else {
      Serial.println(F("error: usage - 'ez'"));
    }
  }
  else if (args[0].equals(String("vss"))) { // Set the setpoint for a specific velocity PID
    if (numArgs == 3)
    {
      int pidNum = args[1].toInt() - 1;
      if (pidNum < 4 && pidNum > -1)
      {
        pids[pidNum].SetMode(AUTOMATIC);
        Setpoints[pidNum] = toDouble(args[2]);
        Serial.println(F("ok"));
      }
      else
      {
        Serial.println(F("error: usage - 'vss [1/2/3/4] [velocity]'"));
      }
    }
    else
    {
      Serial.println(F("error: usage - 'vss [1/2/3/4] [velocity]'"));
    }
  }
  else if (args[0].equals(String("vs"))) { // Set all the setpoints for the velocity PIDs
    if (numArgs == 5)
    {
      for (int i = 0; i < 4; i++)
      {
        pids[i].SetMode(AUTOMATIC);
      }
      Setpoints[REAR_LEFT_ENC] = toDouble(args[1]);
      Setpoints[REAR_RIGHT_ENC] = toDouble(args[2]);
      Setpoints[FRONT_RIGHT_ENC] = toDouble(args[3]);
      Setpoints[FRONT_LEFT_ENC] = toDouble(args[4]);
      Serial.println("ok");
    }
    else
    {
      Serial.println(F("error: usage - 'vs [velocity1] [velocity2] [velocity3] [velocity4]'"));
    }
  }
  else if (args[0].equals(String("vp"))) { // Modify the pid constants
    if (numArgs == 5)
    {
      int pidNum = args[1].toInt() - 1;
      if (pidNum < 4 && pidNum > -1)
      {
        pids[pidNum].SetTunings(toDouble(args[2]), toDouble(args[3]), toDouble(args[4]));
        Serial.println("ok");
      }
      else
      {
        Serial.println(F("error: usage - 'vp [1/2/3/4] [kp] [ki] [kd]'"));
      }
    }
    else
    {
      Serial.println(F("error: usage - 'vp [1/2/3/4] [kp] [ki] [kd]'"));
    }
  }
  else if(args[0].equals(String("ram"))){ // Check RAM
    Serial.println(freeRam());
  }
  /*else if (args[0].equals(String("i"))) { // Display Inputs
    String ret = "";
    ret += Inputs[REAR_LEFT_ENC];
    ret += " ";
    ret += Inputs[REAR_RIGHT_ENC];
    ret += " ";
    ret += Inputs[FRONT_RIGHT_ENC];
    ret += " ";
    ret += Inputs[FRONT_LEFT_ENC];
    Serial.println(ret);
  }
  else if (args[0].equals(String("s"))) { // Display Setpoints
    String ret = "";
    ret += Setpoints[REAR_LEFT_ENC];
    ret += " ";
    ret += Setpoints[REAR_RIGHT_ENC];
    ret += " ";
    ret += Setpoints[FRONT_RIGHT_ENC];
    ret += " ";
    ret += Setpoints[FRONT_LEFT_ENC];
    Serial.println(ret);
  }
  else if (args[0].equals(String("o"))) { // Display Outputs
    String ret = "";
    ret += Outputs[REAR_LEFT_ENC];
    ret += " ";
    ret += Outputs[REAR_RIGHT_ENC];
    ret += " ";
    ret += Outputs[FRONT_RIGHT_ENC];
    ret += " ";
    ret += Outputs[FRONT_LEFT_ENC];
    Serial.println(ret);
  }
  else if (args[0].equals(String("p"))) { // Display Inputs, Setpoints, and Outputs
    String ret = "";
    ret += Inputs[REAR_LEFT_ENC];
    ret += " ";
    ret += Inputs[REAR_RIGHT_ENC];
    ret += " ";
    ret += Inputs[FRONT_RIGHT_ENC];
    ret += " ";
    ret += Inputs[FRONT_LEFT_ENC];
    ret += " ";
    ret += Setpoints[REAR_LEFT_ENC];
    ret += " ";
    ret += Setpoints[REAR_RIGHT_ENC];
    ret += " ";
    ret += Setpoints[FRONT_RIGHT_ENC];
    ret += " ";
    ret += Setpoints[FRONT_LEFT_ENC];
    ret += " ";
    ret += Outputs[REAR_LEFT_ENC];
    ret += " ";
    ret += Outputs[REAR_RIGHT_ENC];
    ret += " ";
    ret += Outputs[FRONT_RIGHT_ENC];
    ret += " ";
    ret += Outputs[FRONT_LEFT_ENC];
    Serial.println(ret);
  }*/
  else {
    // Unrecognized command
    Serial.println(F("error: unrecognized command"));
  }
}

double toDouble(String s)
{
  char buf[s.length() + 1];
  s.toCharArray(buf, s.length() + 1);
  return atof(buf);
}

void updatePID()
{
  bool updated[4];
  for (int i = 0; i < 4; i++)
  {
    double position = encoders[i].getPosition();
    Inputs[i] = encoders[i].getSpeed();
    if (position - lastPositions[i] < 0) Inputs[i] *= -1;
    updated[i] = pids[i].Compute();
    lastPositions[i] = position;
  }

  if (updated[REAR_LEFT_ENC])
  {
    analogWrite(CH1_PWM, abs(Outputs[REAR_LEFT_ENC]));
    digitalWrite(CH1_DIR, Outputs[REAR_LEFT_ENC] > 0);
  }

  if (updated[REAR_RIGHT_ENC])
  {
    analogWrite(CH4_PWM, abs(Outputs[REAR_RIGHT_ENC]));
    digitalWrite(CH4_DIR, Outputs[REAR_RIGHT_ENC] > 0);
  }

  if (updated[FRONT_RIGHT_ENC])
  {
    analogWrite(CH3_PWM, abs(Outputs[FRONT_RIGHT_ENC]));
    digitalWrite(CH3_DIR, Outputs[FRONT_RIGHT_ENC] < 0);
  }

  if (updated[FRONT_LEFT_ENC])
  {
    analogWrite(CH2_PWM, abs(Outputs[FRONT_LEFT_ENC]));
    digitalWrite(CH2_DIR, Outputs[FRONT_LEFT_ENC] < 0);
  }
}

int freeRam () 
{
  extern int __heap_start, *__brkval; 
  int v; 
  return (int) &v - (__brkval == 0 ? (int) &__heap_start : (int) __brkval); 
}
