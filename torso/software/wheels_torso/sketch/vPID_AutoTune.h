#ifndef vPID_AutoTune
#define vPID_AutoTune

class vPID_ATune
{

  public:
  //commonly used functions **************************************************************************
    vPID_ATune(double*, double*);                       	// * Constructor.  links the Autotune to a given PID
    int Runtime();						   			   	// * Similar to the PID Compue function, returns non 0 when done
	void Cancel();									   	// * Stops the AutoTune	
	
	void SetOutputStep(double);						   	// * how far above and below the starting value will the output step?	
	double GetOutputStep();							   	// 
	
	void SetControlType(int); 						   	// * Determies if the tuning parameters returned will be PI (D=0)
	int GetControlType();							   	//   or PID.  (0=PI, 1=PID)			
	
	void SetLookbackSec(int);							// * how far back are we looking to identify peaks
	int GetLookbackSec();								//
	
	void SetNoiseBand(double);							// * the autotune will ignore signal chatter smaller than this value
	double GetNoiseBand();								//   this should be acurately set
	
	double GetKp();										// * once autotune is complete, these functions contain the
	double GetKi();										//   computed tuning parameters.  
	double GetKd();										//
	
  private:
    void FinishUp();
	bool isMax, isMin;
	double *input, *output;
	double setpoint;
	double noiseBand;
	int controlType;
	bool running;
	unsigned long peak1, peak2, lastTime;
	int sampleTime;
	int nLookBack;
	int peakType;
	double lastInputs[101];
    double peaks[10];
	int peakCount;
	bool justchanged;
	bool justevaled;
	double absMax, absMin;
	double oStep;
	double outputStart;
	double Ku, Pu;
	
};
#endif

