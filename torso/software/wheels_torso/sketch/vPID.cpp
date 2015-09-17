#include "vPID.h"
/*
	Velocity PID Controller
*/


vPID::vPID(double* input, double* setpoint, double* output, double p, double i, double d, int ControllerDirection)
	:(input, setpoint, output, p, i, d, ControllerDirection)
	{
		
		SetOutputLimits(-255,255);

		// Sample Time is 10 ms
		SampleTime = 10;
	}

bool vPID::Compute()
{
   if(!inAuto) return false;
   unsigned long now = millis();
   unsigned long timeChange = (now - lastTime);
   if(timeChange>=SampleTime)
   {
      /*Compute all the working error variables*/
	  double input = *myInput;
      double error = *mySetpoint - input;
      ITerm+= (ki * error);
      // Modified from the original
      // Caps the Integral Term to prevent windup and lagging
      if(ITerm + lastOutput > outMax) ITerm= outMax-lastOutput;
      else if(ITerm + lastOutput < outMin) ITerm= outMin - lastOutput;
      double dInput = (input - lastInput);
 
      /*Compute PID Output*/
      double output = lastOutput + kp * error + ITerm- kd * dInput;
      
	  if(output > outMax) output = outMax;
      else if(output < outMin) output = outMin;
	  *myOutput = output;
	  
      /*Remember some variables for next time*/
      lastInput = input;
      lastTime = now;
      lastOutput = output;
	  return true;
   }
   else return false;

}