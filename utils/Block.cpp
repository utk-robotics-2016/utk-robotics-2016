#include "Block.h"

// Set default values
Block::Block()
{
    setType("default");
    setColor(Scalar(0,0,0));
}

Block::Block(string name, Scalar min, Scalar max, Scalar color)
{
    setType(name);
    setHSVmin(min);
    setHSVmax(max);
    setColor(color);
}

Block::~Block()
{
}

int Block::getXPos()
{
    return xPos;
}

void Block::setXPos(int x)
{
    xPos = x;
}

int Block::getYPos()
{
    return yPos;
}

void Block::setYPos(int y)
{
    yPos = y;
}

Scalar Block::getHSVmin()
{
    return HSVmin;
}

Scalar Block::getHSVmax()
{
    return HSVmax;
}

void Block::setHSVmin(Scalar min)
{
    HSVmin = min;
}

void Block::setHSVmax(Scalar max)
{
    HSVmax = max;
}
