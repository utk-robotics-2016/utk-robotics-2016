#include <Servo.h>
#include <Wire.h>
#include "I2CEncoder.h"
#include "vPID.h"


// Globals
int ledState = HIGH;
// Command parsing
const int MAX_ARGS = 4;
String args[MAX_ARGS];
int numArgs = 0;

// Pin definitions
const char LED = 6;
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

// vPID
vPID pids[4];
double inputs[4];
double setpoints[4];
double outputs[4];


void setup() 
{
    // Init LED pin
    pinMode(LED, OUTPUT);
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

    // Init serial
    Serial.begin(115200);
    
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

    // vPID initialization
    inputs[REAR_RIGHT_ENC] = encoders[REAR_RIGHT_ENC].getVelocity();
    inputs[REAR_RIGHT_ENC] = encoders[REAR_RIGHT_ENC].getVelocity();
    inputs[FRONT_RIGHT_ENC] = encoders[FRONT_RIGHT_ENC].getVelocity();
    inputs[FRONT_LEFT_ENC] = encoders[FRONT_LEFT_ENC].getVelocity();

    setpoints[REAR_RIGHT_ENC] = 0;
    setpoints[REAR_RIGHT_ENC] = 0;
    setpoints[FRONT_RIGHT_ENC] = 0;
    setpoints[FRONT_LEFT_ENC] = 0;

    pids[REAR_LEFT_ENC] = new vPID(&inputs[REAR_LEFT_ENC], &outputs[REAR_LEFT_ENC], &setpoints[REAR_LEFT_ENC], .67, .02, 0, DIRECT)
    pids[REAR_RIGHT_ENC] = new vPID(&inputs[REAR_RIGHT_ENC], &outputs[REAR_RIGHT_ENC], &setpoints[REAR_RIGHT_ENC], .67, .02, 0, DIRECT)
    pids[FRONT_RIGHT_ENC] = new vPID(&inputs[FRONT_RIGHT_ENC], &outputs[FRONT_RIGHT_ENC], &setpoints[FRONT_RIGHT_ENC],.67, .02, 0, DIRECT)
    pids[FRONT_LEFT_ENC] = new vPID(&inputs[FRONT_LEFT_ENC], &outputs[FRONT_LEFT_ENC], &setpoints[FRONT_LEFT_ENC], .74, .02, 0, DIRECT)

    // Full reverse to full forwards on the motors
    pid[REAR_LEFT_ENC].SetOutputLimits(-255,255);
    pid[REAR_RIGHT_ENC].SetOutputLimits(-255,255);
    pid[FRONT_RIGHT_ENC].SetOutputLimits(-255,255);
    pid[FRONT_LEFT_ENC].SetOutputLimits(-255,255);

    pids[REAR_LEFT_ENC].SetMode(AUTOMATIC);
    pids[REAR_RIGHT_ENC].SetMode(AUTOMATIC);
    pids[FRONT_RIGHT_ENC].SetMode(AUTOMATIC);
    pids[FRONT_LEFT_ENC].SetMode(AUTOMATIC);

    // Display ready LED
    digitalWrite(LED,HIGH);
    
}

/* The loop is set up in two parts. First the Arduino does the work it needs to
 * do for every loop, next is runs the checkInput() routine to check and act on
 * any input from the serial connection.
 */
 void loop() 
 {
    int inbyte;

    // Accept and parse serial input
    checkInput();
    updatePID();
}

void parse_args(String command) 
{
    numArgs = 0;
    int beginIdx = 0;
    int idx = command.indexOf(" ");

    String arg;
    char charBuffer[16];

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
 void checkInput() 
 {
    int inbyte;
    static char incomingBuffer[128];
    static char bufPosition=0;

    if(Serial.available()>0) 
    {
        // Read only one character per call
        inbyte = Serial.read();
        if(inbyte==10||inbyte==13) 
        {
            // Newline detected
            incomingBuffer[bufPosition]='\0'; // NULL terminate the string
            bufPosition=0; // Prepare for next command

            // Supply a separate routine for parsing the command. This will
            // vary depending on the task.
            parseAndExecuteCommand(String(incomingBuffer));
        }
        else 
        {
            incomingBuffer[bufPosition]=(char)inbyte;
            bufPosition++;
            if(bufPosition==128) 
            {
                Serial.println("error: command overflow");
                bufPosition=0;
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
 void parseAndExecuteCommand(String command) 
 {
    Serial.println("> " + command);
    parse_args(command);
    if(args[0].equals(String("ping"))) 
    {
        if(numArgs == 1) 
        {
            Serial.println("ok");
        } 
        else 
        {
            Serial.println("error: usage - 'ping'");
        }
    }
    else if(args[0].equals(String("le"))) // led set
    {
        if(numArgs == 2) 
        {
            if(args[1].equals(String("on"))) 
            {
                ledState = HIGH;
                digitalWrite(LED,HIGH);
                Serial.println("ok");
            } 
            else if(args[1].equals(String("off"))) 
            {
                ledState = LOW;
                digitalWrite(LED,LOW);
                Serial.println("ok");
            } 
            else 
            {
                Serial.println("error: usage - 'le [on/off]'");
            }
        } 
        else 
        {
            Serial.println("error: usage - 'le [on/off]'");
        }
    }
    else if(args[0].equals(String("ma")))  //move laterally left
    {
        if(numArgs == 1) 
        {
            digitalWrite(CH2_DIR,HIGH);
            analogWrite(CH2_PWM,128);
            digitalWrite(CH3_DIR,LOW);
            analogWrite(CH3_PWM,128);
            digitalWrite(CH1_DIR,HIGH);
            analogWrite(CH1_PWM,128);
            digitalWrite(CH4_DIR,LOW);
            analogWrite(CH4_PWM,128);
            delay(100);
            analogWrite(CH1_PWM,0);
            analogWrite(CH2_PWM,0);
            analogWrite(CH3_PWM,0);
            analogWrite(CH4_PWM,0);
            Serial.println("ok");
        } 
        else 
        {
            Serial.println("error: usage - 'ma'");
        }
    }
    else if(args[0].equals(String("md")))  //move laterally right
    {
        if(numArgs == 1) 
        {
            digitalWrite(CH2_DIR,LOW);
            analogWrite(CH2_PWM,128);
            digitalWrite(CH3_DIR,HIGH);
            analogWrite(CH3_PWM,128);
            digitalWrite(CH1_DIR,LOW);
            analogWrite(CH1_PWM,128);
            digitalWrite(CH4_DIR,HIGH);
            analogWrite(CH4_PWM,128);
            delay(100);
            analogWrite(CH1_PWM,0);
            analogWrite(CH2_PWM,0);
            analogWrite(CH3_PWM,0);
            analogWrite(CH4_PWM,0);
            Serial.println("ok");
        } 
        else 
        {
            Serial.println("error: usage - 'md'");
        }
    }
    else if(args[0].equals(String("mw")))  //move laterally forward
    {
        if(numArgs == 1) 
        {
            digitalWrite(CH2_DIR,LOW);
            analogWrite(CH2_PWM,128);
            digitalWrite(CH3_DIR,LOW);
            analogWrite(CH3_PWM,128);
            digitalWrite(CH1_DIR,HIGH);
            analogWrite(CH1_PWM,128);
            digitalWrite(CH4_DIR,HIGH);
            analogWrite(CH4_PWM,128);
            delay(100);
            analogWrite(CH1_PWM,0);
            analogWrite(CH2_PWM,0);
            analogWrite(CH3_PWM,0);
            analogWrite(CH4_PWM,0);
            Serial.println("ok");
        } 
        else 
        {
            Serial.println("error: usage - 'mw'");
        }
    } 
    else if(args[0].equals(String("ms")))  //move laterally backward
    {
        if(numArgs == 1) 
        {
            digitalWrite(CH2_DIR,HIGH);
            analogWrite(CH2_PWM,128);
            digitalWrite(CH3_DIR,HIGH);
            analogWrite(CH3_PWM,128);
            digitalWrite(CH1_DIR,LOW);
            analogWrite(CH1_PWM,128);
            digitalWrite(CH4_DIR,LOW);
            analogWrite(CH4_PWM,128);
            delay(100);
            analogWrite(CH1_PWM,0);
            analogWrite(CH2_PWM,0);
            analogWrite(CH3_PWM,0);
            analogWrite(CH4_PWM,0);
            Serial.println("ok");
        } 
        else 
        {
            Serial.println("error: usage - 'ms'");
        }
    }
    else if(args[0].equals(String("rl")))  // read led
    {
        if(numArgs == 1) 
        {
            Serial.println(ledState);
        } 
        else 
        {
            Serial.println("error: usage - 'rl'");
        }
    }
    else if(args[0].equals(String("go"))) 
    {
        if(numArgs == 4) 
        {
            int speed = args[2].toInt();

            boolean dir = LOW;
            if(args[3].equals(String("ccw"))) 
            {
                dir = HIGH;
            }

            if(args[1].equals(String("1"))) 
            {
                analogWrite(CH1_PWM, speed);
                digitalWrite(CH1_DIR, dir);
                Serial.println("ok");
            }
            else if(args[1].equals(String("2"))) 
            {
                analogWrite(CH2_PWM, speed);
                digitalWrite(CH2_DIR, dir);
                Serial.println("ok");
            }
            else if(args[1].equals(String("3"))) 
            {
                analogWrite(CH3_PWM, speed);
                digitalWrite(CH3_DIR, dir);
                Serial.println("ok");
            }
            else if(args[1].equals(String("4"))) 
            {
                analogWrite(CH4_PWM, speed);
                digitalWrite(CH4_DIR, dir);
                Serial.println("ok");
            }
            else
            {
                Serial.println("error: usage - 'go [1/2/3/4] [speed] [cw/ccw]'");
            }
        } 
        else 
        {
            Serial.println("error: usage - 'go [1/2/3/4] [speed] [cw/ccw]'");
        }
    }
    else if(args[0].equals(String("ep"))) // encoder position (in rotations)
    { 
        if(numArgs == 1) 
        {
            String ret = "";
            ret += encoders[REAR_LEFT_ENC].getPosition();
            ret += " ";
            ret += encoders[REAR_RIGHT_ENC].getPosition();
            ret += " ";
            ret += encoders[FRONT_RIGHT_ENC].getPosition();
            ret += " ";
            ret += encoders[FRONT_LEFT_ENC].getPosition();
            Serial.println(ret);
        } 
        else 
        {
            Serial.println("error: usage - 'ep'");
        }
    }
    else if(args[0].equals(String("erp"))) // encoder raw position (in ticks)
    {
        if(numArgs == 1) 
        {
            String ret = "";
            ret += encoders[REAR_LEFT_ENC].getRawPosition();
            ret += " ";
            ret += encoders[REAR_RIGHT_ENC].getRawPosition();
            ret += " ";
            ret += encoders[FRONT_RIGHT_ENC].getRawPosition();
            ret += " ";
            ret += encoders[FRONT_LEFT_ENC].getRawPosition();
            Serial.println(ret);
        } 
        else 
        {
            Serial.println("error: usage - 'erp'");
        }
    }
    else if(args[0].equals(String("ev")))  // encoder velocity (in rotations per minute)
    {
        if(numArgs == 1) 
        {
            String ret = "";
            ret += encoders[REAR_LEFT_ENC].getVelocity();
            ret += " ";
            ret += encoders[REAR_RIGHT_ENC].getVelocity();
            ret += " ";
            ret += encoders[FRONT_RIGHT_ENC].getVelocity();
            ret += " ";
            ret += encoders[FRONT_LEFT_ENC].getVelocity();
            Serial.println(ret);
        } 
        else 
        {
            Serial.println("error: usage - 'ev'");
        }
    }
    else if(args[0].equals(String("ez")))  // encoder zero
    {    
        if(numArgs == 1) 
        {
            for(int i = 0; i < 4; i++) 
            {
                encoders[i].zero();
            }
            Serial.println("ok");
        } 
        else 
        {
            Serial.println("error: usage - 'ez'");
        }
    }
    else if(args[0].equals(String("vm"))) // set velocity pid mode to auto or manual
    {
        if(numArgs == 2)
        {
            if(args[1].equals(String("a")))
            {
                for(int i = 0; i < 4; i++)
                {
                    pids[i].SetMode(AUTOMATIC);
                }
                Serial.println("ok");
            }
            else if(args[1].equals(String("m"))
            {
                for(int i = 0; i < 4; i++)
                {
                    pids[i].SetMode(MANUAL);
                }
                Serial.println("ok");
            }
            else
            {
                Serial.println("error: usage - 'vm [a/m]'");
            }
        }
        else
        {
            Serial.println("error: usage - 'vm [a/m]'");
        }
    }
    else if(args[0].equals(String("vs"))) // set the desired velocites for the wheels
    {
        if(numArgs == 5)
        {
            for(int i = 1; i <= 4; i++)
            {
                setpoints[i] = args[i].toDouble();
            }
            Serial.println("ok");
        }
        else
        {
            Serial.println("error: usage - 'vs [velocity1] [velocity2] [velocity3] [velocity4]'");
        }
    }
    else if(args[0].equals(String("vp"))) // set the p parameter for the vPID
    {
        if(numArgs == 5)
        {
            int pidNum = args[1].toInt();
            double p = args[2].toDouble();
            double i = args[3].toDouble();
            double d = args[4].toDouble();
            if(pid > 0 && pid < 5)
            {
                vPIDs[pidNum].SetTunings(p,i,d)
                Serial.println("ok");
            }
            else
            {
                Serial.println("error: usage - 'vp [0/1/2/4] [kp] [ki] [kd]'");
            }
        }
        else
        {
            Serial.println("error: usage - 'vp [0/1/2/4] [kp] [ki] [kd]'");
        }
    }
    else 
    {
        // Unrecognized command
        Serial.println("error: unrecognized command");
    }
}

void updatePID()
{
    for(int i = 0; i < 4; i++)
    {
        inputs[i] = encoders[i].getVelocity();
    }

    for(int i = 0; i < 4; i++)
    {
        vPIDs[i].compute();
    }

    analogWrite(CH1_PWM, abs(outputs[REAR_LEFT_ENC]));
    digitalWrite(CH1_DIR, outputs[REAR_LEFT_ENC] > 0);

    analogWrite(CH2_PWM, abs(outputs[FRONT_LEFT_ENC]));
    digitalWrite(CH2_DIR, outputs[FRONT_LEFT_ENC] > 0);

    analogWrite(CH3_PWM, abs(outputs[FRONT_RIGHT_ENC]));
    digitalWrite(CH3_DIR, outputs[FRONT_RIGHT_ENC] > 0);

    analogWrite(CH4_PWM, abs(outputs[REAR_RIGHT_ENC]));
    digitalWrite(CH4_DIR, outputs[REAR_RIGHT_ENC] > 0);
}
