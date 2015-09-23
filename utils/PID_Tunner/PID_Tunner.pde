import processing.serial.*;
import controlP5.*;

Serial myPort;
ControlP5 cp5;
Textfield[] PField = new Textfield[4];
Textfield[] IField = new Textfield[4];
Textfield[] DField = new Textfield[4];
Textfield[] SField = new Textfield[4];
Textfield SAllField;

float[] Setpoint = new float[4];
float[] Input = new float[4];
float[] Output = new float[4];

// graph stuff
int iLeft = 20, iWidth = 800, iTop = 20, iHeight = 300;
float iMin = -100.0, iMax = 100.0;
int oLeft = iLeft, oWidth = iWidth, oTop = iTop+iHeight+30, oHeight = iHeight;
float oMin = -255.0, oMax = 255.0;

// time stuff
int windowspan =10000;
float displayFactor = 1000;
int refreshRate = 100;
int nextRefresh;

//Graph Data
int arrayLength = windowspan / refreshRate;
int[][] InputData = new int[4][arrayLength];
int[][] SetpointData = new int[4][arrayLength];
int[][] OutputData = new int[4][arrayLength];
int nPoints = 0;
float pointWidth = iWidth/float(arrayLength-2);

int motorNum = 2;

void setup()
{
  frameRate(30);
  size(900,800);
  String[] portList = Serial.list();
  for(int i = 0; i < portList.length; i++)
    println(portList[i]);
  myPort = new Serial(this, Serial.list()[7], 115200);                
  myPort.bufferUntil('\n');
  
  cp5 = new ControlP5(this);
  
  for(int i = 0; i < 4; i++)
  {
    Input[i] = 0.0;
    Setpoint[i] = 0.0;
    Output[i] = 0.0;
    
    
    cp5.addTextlabel("Motor"+(i+1)+"_label")
      .setPosition(oLeft+50,oTop+oHeight+24+20*i)
      .setColor(0)
      .setValue("Motor "+(i+1)+"- ");
    
    cp5.addTextlabel("P"+(i+1)+"_label")
      .setPosition(oLeft+105,oTop+oHeight+24+20*i)
      .setColor(0)
      .setValue("P: ");
    
    
    PField[i] = cp5.addTextfield("P"+(i+1))
     .setPosition(oLeft+120,oTop+oHeight+20+20*i)
     .setSize(45,16)
     .setColorBackground(color(255,255,255))
     .setColor(0)
     .setValue(".1")
     ;
     
     cp5.addTextlabel("I"+(i+1)+"_label")
      .setPosition(oLeft+170,oTop+oHeight+24+20*i)
      .setColor(0)
      .setValue("I: ");
     
     IField[i] = cp5.addTextfield("I"+(i+1))
     .setPosition(oLeft+185,oTop+oHeight+20+20*i)
     .setSize(45,16)
     .setColorBackground(color(255,255,255))
     .setColor(0)
     .setValue("0");
     ;
     
     cp5.addTextlabel("D"+(i+1)+"_label")
      .setPosition(oLeft+235,oTop+oHeight+24+20*i)
      .setColor(0)
      .setValue("D: ");
     
     DField[i] = cp5.addTextfield("D"+(i+1))
     .setPosition(oLeft+250,oTop+oHeight+20+20*i)
     .setSize(45,16)
     .setColorBackground(color(255,255,255))
     .setColor(0)
     .setValue("0");
     ;
     
     cp5.addButton("Set_PID"+(i+1))
     .setValue(2)
     .setPosition(oLeft+300,oTop+oHeight+20+20*i)
     .setSize(50,16)
     ;
     
     cp5.addTextlabel("Setpoint"+(i+1)+"_label")
      .setPosition(oLeft+355,oTop+oHeight+24+20*i)
      .setColor(0)
      .setValue("Setpoint: ");
     
     SField[i] = cp5.addTextfield("Setpoint"+(i+1))
     .setPosition(oLeft+400,oTop+oHeight+20+20*i)
     .setSize(45,16)
     .setColorBackground(color(255,255,255))
     .setColor(0)
     .setValue("0");
     ;
     
     cp5.addButton("Set_Setpoint"+(i+1))
     .setValue(2)
     .setPosition(oLeft+450,oTop+oHeight+20+20*i)
     .setSize(75,16)
     ;
     
     
  }
  
  cp5.addTextlabel("Setpoint_label")
      .setPosition(oLeft+555,oTop+oHeight+74)
      .setColor(0)
      .setValue("Setpoint: ");
  
  SAllField = cp5.addTextfield("Setpoint")
     .setPosition(oLeft+600,oTop+oHeight+70)
     .setSize(45,16)
     .setColorBackground(color(255,255,255))
     .setColor(0)
     .setValue("0");
     ;
  
  cp5.addButton("Set_All_Setpoint")
     .setValue(2)
     .setPosition(oLeft+650,oTop+oHeight+70)
     .setSize(80,16)
     ;
  
     nextRefresh = millis();
}

void draw()
{
  
  background(100);
  stroke(0);
  rect(iLeft,iTop,iWidth,iHeight);
  rect(oLeft,oTop,oWidth,oHeight);
  rect(oLeft,oTop+oHeight+15,oWidth,88);
  
  text("PID Input / Setpoint",iLeft+10,iTop-5);
  text("PID Output",oLeft+10,oTop-5);
  
  // Horizontal Lines
  int horzCount = 16;
  for(int i=0;i<=horzCount;i++)
  {
    line(iLeft,iTop+i*iHeight/horzCount,iLeft+iWidth,iTop+i*iHeight/horzCount);
    text(str(int(iMax - (iMax-iMin)*i/horzCount)),iLeft+iWidth+5,iTop+i*iHeight/horzCount+4);
    
    line(oLeft,oTop+i*oHeight/horzCount,oLeft+oWidth,oTop+i*oHeight/horzCount);
    text(str(int(oMax - (oMax-oMin)*i/horzCount)),oLeft+oWidth+5,oTop+i*oHeight/horzCount+4);
  }
  
  // Vertical lines and TimeStamps
  int vertCount = 20;
  int elapsedTime = millis();
  int interval = iWidth/vertCount;
  int shift = elapsedTime*iWidth/windowspan;
  shift %= interval;
  int iTimeInterval = windowspan/vertCount;
  float firstDisplay = float(iTimeInterval*(elapsedTime/iTimeInterval))/displayFactor;
  float timeInterval = float(iTimeInterval)/displayFactor;
  for(int i=0; i<vertCount;i++)
  {
    int x = iLeft+iWidth-shift-i*iWidth/vertCount;
    line(x,iTop,x,iTop+iHeight);
    line(x,oTop,x,oTop+oHeight);
    
    float t = firstDisplay-(float)i*timeInterval;
    if(t>0) 
    {
      text(str(t),x,oTop+oHeight+10);
      text(str(t),x,iTop+iHeight+10);
    }
  }
  if(elapsedTime >= nextRefresh)
  {
    nextRefresh += refreshRate;
    for(int j = 0; j < 4; j++)
    {
      for(int i=nPoints-1;i>0;i--)
      {
        InputData[j][i]=InputData[j][i-1];
        SetpointData[j][i]=SetpointData[j][i-1];
        OutputData[j][i]=OutputData[j][i-1];
      }
    }
    if(nPoints < arrayLength) nPoints++;
  }
  for(int j = 0; j < 4; j++)
  {
  InputData[j][0] = int(iTop+iHeight-iHeight*(Input[j]-iMin)/(iMax-iMin));
  stroke(64*(j+1),0,0);
  // Max and Min are swapped because 0,0 is in the top left
  int inputMax = InputData[j][0], inputMin = InputData[j][0];
  for(int i=0;i<nPoints-2;i++)
  {
    int x1 = int(iLeft+iWidth-(i+1)*pointWidth);
    int x2 = int(iLeft+iWidth-i*pointWidth);
    int y1 = InputData[j][i+1];
    int y2 = InputData[j][i];
    line(x1,y1,x2,y2);
    
    // Actually the minimum peak
    if(InputData[j][i] > inputMax)
      inputMax = InputData[j][i];
      
    // Actually the maximum peak
    if(InputData[j][i] < inputMin)
      inputMin = InputData[j][i];
  }
  
  stroke(64*(j+1),64*(j+1),0);
  line(iLeft,inputMax,iLeft+iWidth,inputMax);
  text(str(-1*int(float(inputMax - iTop)/float(iHeight) * (iMax-iMin) + iMin)),iLeft+iWidth+30,inputMax+4);
  stroke(64*(j+1),0,64*(j+1));
  line(iLeft,inputMin,iLeft+iWidth,inputMin);
  text(str(-1*int(float(inputMin - iTop)/float(iHeight) *(iMax-iMin) + iMin)),iLeft+iWidth+45,inputMin+4);

  
  SetpointData[j][0] = int(iTop+iHeight-iHeight*(Setpoint[j]-iMin)/(iMax-iMin));
  stroke(0,64*(j+1),0);
  for(int i=0;i<nPoints-2;i++)
  {
    int x1 = int(iLeft+iWidth-(i+1)*pointWidth);
    int x2 = int(iLeft+iWidth-i*pointWidth);
    int y1 = SetpointData[j][i+1];
    int y2 = SetpointData[j][i];
    line(x1,y1,x2,y2);
  }
  
  OutputData[j][0] = int(oTop+oHeight-oHeight*(Output[j]-oMin)/(oMax-oMin));
  stroke(0,0,64*(j+1));
  for(int i=0;i<nPoints-2;i++)
  {
    int x1 = int(oLeft+oWidth-(i+1)*pointWidth);
    int x2 = int(oLeft+oWidth-i*pointWidth);
    int y1 = OutputData[j][i+1];
    int y2 = OutputData[j][i];
    line(x1,y1,x2,y2);
  }
  }
  myPort.write("p\n");
}

public boolean isNumeric(String s) {  
    return s.matches("[-+]?\\d*\\.?\\d+");  
}  

void setPID1()
{
  if(isNumeric(PField[0].getText()) && isNumeric(IField[0].getText()) && isNumeric(DField[0].getText()))
  {
  println("P: "+PField[0].getText()+" I: "+IField[0].getText()+" D: "+DField[0].getText()+"\n");
  myPort.write("vp 1 "+PField[0].getText()+"  "+IField[0].getText()+" "+DField[0].getText()+"\n");
  }
}

void setPID2()
{
  if(isNumeric(PField[1].getText()) && isNumeric(IField[1].getText()) && isNumeric(DField[1].getText()))
  {
  println("P: "+PField[1].getText()+" I: "+IField[1].getText()+" D: "+DField[1].getText()+"\n");
  myPort.write("vp 2 "+PField[1].getText()+"  "+IField[1].getText()+" "+DField[1].getText()+"\n");
  }
}

void setPID3()
{
  if(isNumeric(PField[2].getText()) && isNumeric(IField[2].getText()) && isNumeric(DField[2].getText()))
  {
  println("P: "+PField[2].getText()+" I: "+IField[2].getText()+" D: "+DField[2].getText()+"\n");
  myPort.write("vp 3 "+PField[2].getText()+"  "+IField[2].getText()+" "+DField[2].getText()+"\n");
  }
}

void setPID4()
{
  if(isNumeric(PField[3].getText()) && isNumeric(IField[3].getText()) && isNumeric(DField[3].getText()))
  {
  println("P: "+PField[3].getText()+" I: "+IField[3].getText()+" D: "+DField[3].getText()+"\n");
  myPort.write("vp 4 "+PField[3].getText()+"  "+IField[3].getText()+" "+DField[3].getText()+"\n");
  }
}

void Set_Setpoint1()
{
  if(isNumeric(SField[0].getText()))
    myPort.write("vss 1 "+SField[0].getText()+"\n");
}

void Set_Setpoint2()
{
  if(isNumeric(SField[1].getText()))
    myPort.write("vss 2 "+SField[1].getText()+"\n");
}

void Set_Setpoint3()
{
  if(isNumeric(SField[2].getText()))
    myPort.write("vss 3 "+SField[2].getText()+"\n");
}

void Set_Setpoint4()
{
  if(isNumeric(SField[3].getText()))
    myPort.write("vss 4 "+SField[3].getText()+"\n");
}

void Set_All_Setpoint()
{
  if(isNumeric(SAllField.getText()))
  {
    for(int i = 0; i < 4; i++)
      SField[i].setValue(SAllField.getText());
    myPort.write("vs "+SAllField.getText()+" "+SAllField.getText()+" "+SAllField.getText()+" "+SAllField.getText()+"\n");
  }
}

void serialEvent(Serial myPort)
{
  String read = myPort.readStringUntil('\n');
  if(read == "ok")
    return;
  print(str(millis())+ " "+read);
  String[] s = split(read, " ");
  
  if (s.length == 12)
  {
    for(int i = 0; i < 4; i++)
    {
      Setpoint[i] = float(s[i+4]);           // * pull the information
      Input[i] = float(s[i]);              //   we need out of the
      Output[i] = float(s[i+8]);             //   string and put it
    }
  }
}