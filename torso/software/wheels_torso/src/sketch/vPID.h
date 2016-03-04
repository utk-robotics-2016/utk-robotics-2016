#ifndef vPID_h
#define vPID_h
#include <Arduino.h>
#include "PID.h"

class vPID : public PID
{
public:
	vPID(double*, double*, double*, double, double, double, int);
	void SetMode(int Mode);
	bool Compute();
private:
	double lastOutput;
};
#endif
