#include "vPID.h"
/*
	Velocity PID Controller
*/


vPID::vPID(double* input, double* setpoint, double* output, double p, double i, double d, int ControllerDirection)
   :PID(input, setpoint, output, p , i, d, ControllerDirection)
	{
		
		SetOutputLimits(-255,255);

		// Sample Time is 10 ms
		SampleTime = 10;
	}

void vPID::SetMode(int Mode)
{
    bool newAuto = (Mode == AUTOMATIC);
    if(newAuto == !inAuto)
    {  /*we just went from manual to auto*/
        *mySetpoint = 0.0;
        *myOutput = 0.0;
        PID::Initialize();
    }

    inAuto = newAuto;
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
      double setpoint = *mySetpoint;
      if(setpoint == 0) 
        lastOutput = 0;
      double error = setpoint - input;
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
