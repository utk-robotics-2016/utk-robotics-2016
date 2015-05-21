from Vec3d import Vec3d
from math import atan2, pi, degrees, sqrt

shoulderToElbow = 4.75*2.54
elbowToWrist = 5.00*2.54
shoulderPos = Vec3d(0, -5, 5)

def fwdkin(rot):
    humerus = Vec3d(0, 0, shoulderToElbow)
    forearm = Vec3d(0, elbowToWrist, 0)
    baseTheta = rot[0]
    shoulderTheta = rot[1]
    elbowTheta = rot[2]
    pos = humerus.rotated_around_x(-degrees(shoulderTheta))
    pos += forearm.rotated_around_x(-degrees(elbowTheta + shoulderTheta))
    pos.rotate_around_z(-degrees(baseTheta))
    pos += shoulderPos
    return pos

def revkin(pos):
    npos = pos - shoulderPos
    # Atan2 parameters are in the reverse order from Mathematica
    baseTheta = -(atan2(npos[1], npos[0]) - pi/2);
    npos = npos.rotated_around_z(degrees(baseTheta))
    y = npos[1]
    z = npos[2]

    shoulderTheta = atan2(
        (1*(-(elbowToWrist**2*shoulderToElbow*y**2) +
           shoulderToElbow**3*y**2 + shoulderToElbow*y**4 +
           shoulderToElbow*y**2*z**2 -
           z*sqrt(-(shoulderToElbow**2*y**2*(elbowToWrist**4 +
                (-shoulderToElbow**2 + y**2 + z**2)**2 -
                2*elbowToWrist**2*(shoulderToElbow**2 + y**2 +
                  z**2))))))/(shoulderToElbow**2*y*
          (y**2 + z**2)),
        (1*(-(elbowToWrist**2*shoulderToElbow*z) +
           shoulderToElbow**3*z + shoulderToElbow*y**2*z +
           shoulderToElbow*z**3 +
           sqrt(-(shoulderToElbow**2*y**2*(elbowToWrist**4 +
               (-shoulderToElbow**2 + y**2 + z**2)**2 -
               2*elbowToWrist**2*(shoulderToElbow**2 + y**2 +
                 z**2))))))/(shoulderToElbow**2*(y**2 + z**2)))
    elbowTheta = atan2(
        (elbowToWrist**2 + shoulderToElbow**2 - y**2 - z**2)/
         (elbowToWrist*shoulderToElbow),
        sqrt(-(shoulderToElbow**2*y**2*(elbowToWrist**4 +
             (-shoulderToElbow**2 + y**2 + z**2)**2 -
             2*elbowToWrist**2*(shoulderToElbow**2 + y**2 +
               z**2))))/(elbowToWrist*shoulderToElbow**2*y))

    return Vec3d(baseTheta, shoulderTheta, elbowTheta)

#print fwdkin(Vec3d(.5, 0, -1))
#print revkin(Vec3d(3.28974, 1.02183, 27.7517))
