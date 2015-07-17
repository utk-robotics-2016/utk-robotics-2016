#include <Servo.h>

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

void setup() {
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

    // Display ready LED
    digitalWrite(LED,HIGH);
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
    else if(args[0].equals(String("go"))) {
        if(numArgs == 4) {
            int speed = args[2].toInt();

            boolean dir = LOW;
            if(args[3].equals(String("ccw"))) {
                dir = HIGH;
            }

            if(args[1].equals(String("1"))) {
                analogWrite(CH1_PWM, speed);
                digitalWrite(CH1_DIR, dir);
                Serial.println("ok");
            }else if(args[1].equals(String("2"))) {
                analogWrite(CH2_PWM, speed);
                digitalWrite(CH2_DIR, dir);
                Serial.println("ok");
            }else if(args[1].equals(String("3"))) {
                analogWrite(CH3_PWM, speed);
                digitalWrite(CH3_DIR, dir);
                Serial.println("ok");
            }else if(args[1].equals(String("4"))) {
                analogWrite(CH4_PWM, speed);
                digitalWrite(CH4_DIR, dir);
                Serial.println("ok");
            }
        } else {
            Serial.println("error: usage - 'go [1/2/3/4] [speed] [cw/ccw]'");
        }
    }
    else {
        // Unrecognized command
        Serial.println("error: unrecognized command");
    }
}
