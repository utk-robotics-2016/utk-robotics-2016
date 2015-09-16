/*
    Include Project: Sharp GP2D12 Precision Measurement
    Author: Nick Winston, et al. 2015 (UTK IEEE Robotics 2015-2016)
    
    Desc: Precision library for the Sharp GP2D12 IR Rangefinder
    
    Usage:
        1) Include file into sketch
        2) Initialize by init_ir func and include analog pin tied to the sensor
        3) Read distance with read_ir function (Outputs in centimeters as a float) max update speed 2mSec, include analog pin tied to the sensor & 0xFF for close range
            
            OPTIONAL: TBA ; Read distance precisely by providing reflectivity value with read_ir_precise function (Outputs the same as read_ir)
*/

//Local variables
double prev_dist = 0.0;  //Memory distance to differentiate different ranges 


//Function Defines
void init_ir(byte ir_analog_pin) {
    pinMode(ir_analog_pin, INPUT);
    
    analogReference(DEFAULT);
    analogRead(ir_analog_pin);
    
    //Serial.println("ok");
    
    return;
}

int read_ir_raw(byte ir_analog_pin) { //Read raw IR
    int tmp = 0;
    
    analogRead(ir_analog_pin); //Throw out junk data
    
    delay(5);
    
    tmp += analogRead(ir_analog_pin); delay(2); tmp += analogRead(ir_analog_pin); delay(2); tmp += analogRead(ir_analog_pin);
    
    tmp = tmp/3;
    
    return tmp;
}

double read_ir(byte ir_analog_pin, char close_range) {  // "Close Range!?!" -Central Officer Bradford
    int tmp = 0;
    double adc_volts = 0.0;
    
    analogRead(ir_analog_pin); //Throw out junk data
    
    delay(5);
    
    tmp += analogRead(ir_analog_pin); delay(2); tmp += analogRead(ir_analog_pin); delay(2); tmp += analogRead(ir_analog_pin);
    adc_volts = (tmp / 3) * 0.00488;    //  Average the readings and bump up to proper voltage values (5V / 1024)
    
    //Serial.print("IR Read Volt:"); Serial.print(adc_volts); Serial.print(" Dist(cm): ");
    
    if(close_range != 0xFF) {
        //  100cm to 50cm range averaged to the 50% reflectivity curve
        if(adc_volts <= 1.3) {
            prev_dist = (-64.689*log(adc_volts)+63.772);
        }
    
        //  50cm to 30cm range averaged to the 50% reflectivity curve
        else if((adc_volts > 1.3) && (adc_volts <= 1.9)) {
            prev_dist = (-42.35*log(adc_volts)+58.305);
        }   
    
        //  30cm to 17cm range averaged to the 50% reflectivity curve
        else if(adc_volts > 1.9) {
            prev_dist = (-42.941*log(adc_volts)+88.93);
        }
    
    } else {        //  17cm to 0cm range
        prev_dist = (-11.07*log(adc_volts)+1.344);
    }
    
    //Serial.println(prev_dist);
    
    return prev_dist;
}