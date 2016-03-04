#include <I2CEncoder.h>
#include <Wire.h>

#define STR1(x)  #x
#define STR(x)  STR1(x)

// Globals
int ledState = HIGH;
// Command parsing
const int MAX_ARGS = 6;
String args[MAX_ARGS];
int numArgs = 0;

// Pin definitions
const char LED = 13;

// For motor driver:
#define BRAKEVCC 0
#define FW   1
#define BW  2
#define BRAKEGND 3
#define CS_THRESHOLD 100

/*  VNH2SP30 pin definitions
 xxx[0] controls '1' outputs
 xxx[1] controls '2' outputs */
int inApin[2] = {7, 4};  // INA: Clockwise input
int inBpin[2] = {8, 9}; // INB: Counter-clockwise input
int pwmpin[2] = {5, 6}; // PWM input
int cspin[2] = {2, 3}; // CS: Current sense ANALOG input
int wing_extend_enpin[2] = {A0, A1};
int lift_enpin[2] = {A4, A5};

// For encoders:
I2CEncoder encoders[3];

//Left is 19, right is 18
Servo loader_right;
Servo loader_left;

void switch_to_wing_extend() {
    for (int i=0; i<2; i++)
    {
        // Disable lift motor driver
        digitalWrite(lift_enpin[i], LOW);
        // Enable wing motor drivers
        digitalWrite(wing_extend_enpin[i], HIGH);
    }
}

void switch_to_lift() {
    for (int i=0; i<2; i++)
    {
        // Disable wing motor drivers
        digitalWrite(wing_extend_enpin[i], LOW);
        // Enable lift motor driver
        digitalWrite(lift_enpin[i], HIGH);
    }
}

void setup() {
    // Init LED pin
    pinMode(LED, OUTPUT);

    // Init serial
    Serial.begin(115200);

    // Display ready LED
    digitalWrite(LED,HIGH);

    // Initialize digital pins as outputs
    for (int i=0; i<2; i++)
    {
        pinMode(inApin[i], OUTPUT);
        pinMode(inBpin[i], OUTPUT);
        pinMode(pwmpin[i], OUTPUT);

        pinMode(wing_extend_enpin[i], OUTPUT);
        pinMode(lift_enpin[i], OUTPUT);
    }
    switch_to_wing_extend();
    // Initialize braked
    for (int i=0; i<2; i++)
    {
        digitalWrite(inApin[i], LOW);
        digitalWrite(inBpin[i], LOW);
    }

    Wire.begin();
    // From the docs: you must call the init() of each encoder method in the
    // order that they are chained together. The one plugged into the Arduino
    // first, then the one plugged into that and so on until the last encoder.
    encoders[0].init(MOTOR_393_TORQUE_ROTATIONS, MOTOR_393_TIME_DELTA); // Right extend
    encoders[1].init(MOTOR_393_TORQUE_ROTATIONS, MOTOR_393_TIME_DELTA); // Left extend
    encoders[2].init(MOTOR_393_TORQUE_ROTATIONS, MOTOR_393_TIME_DELTA); // Width
    // Ideally, moving forward should count as positive rotation.
    // Make this happen:
    encoders[0].setReversed(true);
    encoders[2].setReversed(true);
}

void motorOff(int motor)
{
    digitalWrite(inApin[motor], LOW);
    digitalWrite(inBpin[motor], LOW);
    analogWrite(pwmpin[motor], 0);
}

/* motorGo() will set a motor going in a specific direction
 the motor will continue going in that direction, at that speed
 until told to do otherwise.
 
 motor: this should be either 0 or 1, will selet which of the two
 motors to be controlled
 
 direct: Should be between 0 and 3, with the following result
 0: Brake to VCC
 1: Clockwise
 2: CounterClockwise
 3: Brake to GND
 
 pwm: should be a value between ? and 255, higher the number, the faster
 it'll go
 */
void motorGo(uint8_t motor, uint8_t direct, uint8_t pwm)
{
  if (motor <= 1)
  {
    if (direct <=4)
    {
      // Set inA[motor]
      if (direct <=1)
        digitalWrite(inApin[motor], HIGH);
      else
        digitalWrite(inApin[motor], LOW);

      // Set inB[motor]
      if ((direct==0)||(direct==2))
        digitalWrite(inBpin[motor], HIGH);
      else
        digitalWrite(inBpin[motor], LOW);

      analogWrite(pwmpin[motor], pwm);
    }
  }
}

/* The loop is set up in two parts. First the Arduino does the work it needs to
 * do for every loop, next is runs the checkInput() routine to check and act on
 * any input from the serial connection.
 */
void loop() {
    int inbyte;

    // Accept and parse serial input
    checkInput();
}

void parse_args(String command) {
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
void checkInput() {
    int inbyte;
    static char incomingBuffer[128];
    static char bufPosition=0;

    if(Serial.available()>0) {
        // Read only one character per call
        inbyte = Serial.read();
        if(inbyte==10||inbyte==13) {
            // Newline detected
            incomingBuffer[bufPosition]='\0'; // NULL terminate the string
            bufPosition=0; // Prepare for next command

            // Supply a separate routine for parsing the command. This will
            // vary depending on the task.
            parseAndExecuteCommand(String(incomingBuffer));
        }
        else {
            incomingBuffer[bufPosition]=(char)inbyte;
            bufPosition++;
            if(bufPosition==128) {
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
void parseAndExecuteCommand(String command) {
    Serial.println("> " + command);
    parse_args(command);
    if(args[0].equals(String("ping"))) {
        if(numArgs == 1) {
            Serial.println("ok");
        } else {
            Serial.println("error: usage - 'ping'");
        }
    }
    else if(args[0].equals(String("le"))) { // led set
        if(numArgs == 2) {
            if(args[1].equals(String("on"))) {
                ledState = HIGH;
                digitalWrite(LED,HIGH);
                Serial.println("ok");
            } else if(args[1].equals(String("off"))) {
                ledState = LOW;
                digitalWrite(LED,LOW);
                Serial.println("ok");
            } else {
                Serial.println("error: usage - 'le [on/off]'");
            }
        } else {
            Serial.println("error: usage - 'le [on/off]'");
        }
    }
    else if(args[0].equals(String("rl"))) { // read led
        if(numArgs == 1) {
            Serial.println(ledState);
        } else {
            Serial.println("error: usage - 'rl'");
        }
    }
    else if(args[0].equals(String("mod"))) { // motor drive
        if(numArgs == 4) {
            int speed = args[2].toInt();
            int mot = args[1].toInt();
            int dir = FW;

            if(args[3].equals(String("bw"))) {
                dir = BW;
            }

            if (mot >= 2) {
                switch_to_lift();
                mot = mot - 2;
            } else {
                switch_to_wing_extend();
            }

            motorGo(mot, dir, speed);
            Serial.println("ok");
        } else {
            Serial.println("error: usage - 'mod [0/1/2/3] [speed] [fw/bw]'");
        }
    }
    else if(args[0].equals(String("mos"))) { // motor stop
        if(numArgs == 2) {
            int mot = args[1].toInt();
            if (mot >= 2) {
                mot = mot - 2;
            }
            motorOff(mot);
            Serial.println("ok");
        } else {
            Serial.println("error: usage - 'mos [0/1/2/3]'");
        }
    }
    else if(args[0].equals(String("ep"))) { // encoder position (in rotations)
        if(numArgs == 2) {
            int enc = args[1].toInt();
            if(enc >= 0 && enc < 3){
            double pos = encoders[enc].getPosition();
            Serial.println(pos);
            }
            else{
                Serial.println("error: usage - 'ep [0/1/2]'");
            }
        } else {
            Serial.println("error: usage - 'ep [0/1/2]'");
        }
    }
    else if(args[0].equals(String("erp"))) { // encoder raw position (in ticks)
        if(numArgs == 2) {
            int enc = args[1].toInt();
            if(enc >= 0 && enc < 3){
            long pos = encoders[enc].getRawPosition();
            Serial.println(pos);
            }
            else{
                Serial.println("error: usage - 'ep [0/1/2]'");
            }
        } else {
            Serial.println("error: usage - 'erp [0/1/2]'");
        }
    }
    else if(args[0].equals(String("ez"))) { // encoder zero
        if(numArgs == 2) {
            int enc = args[1].toInt();
            if(enc >= 0 && enc < 3){
            encoders[enc].zero();
            Serial.println("ok");
            }
            else{
                Serial.println("error: usage - 'ep [0/1/2]'");
            }
        } else {
            Serial.println("error: usage - 'ez [0/1/2]'");
        }
    }
    else if(args[0].equals(String("sls"))) { // set loader servos
        if(numArgs == 3) {
            int rightpos = args[1].toInt();
            int leftpos = args[2].toInt();
            if (!loader_right.attached()) {
                loader_right.attach(3);
            }
            if (!loader_left.attached()) {
                loader_left.attach(2);
            }
            loader_right.write(rightpos);
            loader_left.write(leftpos);
            Serial.println("ok");
        } else {
            Serial.println("error: usage - 'sls [rightpos] [leftpos]'");
        }
    }
    else if(args[0].equals(String("dls"))) { // detach loader servos
        if(numArgs == 1) {
            loader_right.detach();
            loader_left.detach();
            Serial.println("ok");
        } else {
            Serial.println("error: usage - 'ds'");
        }
    }
    else if(args[0].equals(String("ver"))) { // version information
        if(numArgs == 1) {
            String out = "Source last modified: ";
            out += __TIMESTAMP__;
            out += "\r\nPreprocessor timestamp: " __DATE__ " " __TIME__;
            out += "\r\nSource code line number: ";
            out += __LINE__;
            out += "\r\nUsername: " STR(__USER__);
            out += "\r\nDirectory: " STR(__DIR__);
            out += "\r\nGit hash: " STR(__GIT_HASH__);
            Serial.println(out);
        } else {
            Serial.println("error: usage - 'ver'");
        }
    }
    else {
        // Unrecognized command
        Serial.println("error: unrecognized command");
    }
}
