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
