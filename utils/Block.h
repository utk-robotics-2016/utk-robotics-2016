#include <string>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
using namespace std;
using namespace cv;

class Block
{
    public:
        Block();
        ~Block();

        Block(string name, Scalar min, Scalar max, Scalar color);

        int getXPos();
        void setXPos(int x);

        int getYPos();
        void setYPos(int y);

        Scalar getHSVmin();
        Scalar getHSVmax();
        
        void setHSVmin(Scalar min);
        void setHSVmax(Scalar max);

        string getType(){return type;}
        void setType(string t){type = t;}

        Scalar getColor(){return Color;}
        void setColor(Scalar c){Color=c;}

    private:
        int xPos, yPos;
        string type;
        Scalar HSVmin, HSVmax;
        Scalar Color;
};
