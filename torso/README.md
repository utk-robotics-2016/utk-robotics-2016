Torso code is anything that operates at a lower level than head code. The code in this section will typically be some sort of microcontroller (ie: Arduino) code.

We currently have two onboard microcontrollers:

### Arduino Mega (mega)

Currently has a [Sainsmart sensor/servo shield](http://www.sainsmart.com/sainsmart-sensor-shield-v2-for-arduino-mega-2560-r3-1280-iic-bluetooth-lcd-sd-io.html) attached allowing us to connect plenty of servos, limit switches, sensors, etc. Currently the main device connected to this shield is the Arm, so naturally the commands to control the arm get sent to here.

### Teensy (teensy)

The Teensy is presently attached to a purple PCB designed 3 years ago that functions well with the Rover 5 motor driver shield. This purple PCB also has support for a dual motor driver chip that we are planning on using soon. We added this board and microcontroller because of its existing support for motor drivers.
