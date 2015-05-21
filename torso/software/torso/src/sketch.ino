#include <Servo.h>

// Globals
int ledState = HIGH;
// Command parsing
const int MAX_ARGS = 6;
String args[MAX_ARGS];
int numArgs = 0;

// Servo configuration
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

// Pin definitions
const char LED = 13;

void setup() {
    // Init LED pin
    pinMode(LED, OUTPUT);

    // Init sevos
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

    // Init serial
    Serial.begin(9600);

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
    else if(args[0].equals(String("sa"))) { // set arm
        if(numArgs == 6) {
            int posbase = args[1].toInt();
            int posshoulder = args[2].toInt();
            int poselbow = args[3].toInt();
            int poswrist = args[4].toInt();
            int poswristrotate = args[5].toInt();
            base.write(posbase);
            shoulder.write(posshoulder);
            elbow.write(poselbow);
            wrist.write(poswrist);
            wristrotate.write(poswristrotate);
        } else {
            Serial.println("error: usage - 'sa [base] [shoulder] [elbow] [wrist] [wristrotate]'");
        }
    }
    else if(args[0].equals(String("ss"))) { // set suction
        if(numArgs == 2) {
            int pos= args[1].toInt();
            suction.write(pos);
        } else {
            Serial.println("error: usage - 'ss [pos]'");
        }
    }
    else {
        // Unrecognized command
        Serial.println("error: unrecognized command");
    }
}
