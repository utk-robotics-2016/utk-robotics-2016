def correct_baseline_error(s, lf):
    dist = lf.dist_to_baseline
    theta = lf.baseline_theta
    scale = float(320) /lf.im_cols
    print dist, theta
    IDEAL = 60 # Pixels from bottom
    dist_from_ideal = dist-IDEAL
    dist_from_ideal *= scale
    turn_time_small = -0.265+0.2036*abs(theta)
    turn_time_large = 0.220+0.0404*abs(theta)
    turn_time = min(turn_time_small, turn_time_large)
    fw_time = 0.0715+0.0084071*abs(dist_from_ideal)
    if theta < -2:
        s.move_for(turn_time, 0, 0, .3)
    elif theta > 2:
        s.move_for(turn_time, 0, 0, -.3)
    if dist_from_ideal < 0:
        s.move_for(fw_time, .4, 180, 0)
    elif dist_from_ideal > 0:
        s.move_for(fw_time, .4, 0, 0)

def x_strafe(s, actual_x, ideal_x, scale):
    diff = ideal_x - actual_x
    diff *= scale
    strafe_time = 0.0537+0.01698*abs(diff)
    mult = 1
    if diff < 0: # to right
        s.move_for(strafe_time, .4, -90, 0)
        mult = 1
    elif diff > 0: # to left
        s.move_for(strafe_time, .4, 90, 0)
        mult = -1
    return strafe_time * mult

def move_to_first_line(s, linefinder):
    scale = float(320) / linefinder.im_cols
    actual_x = linefinder.lines[0].intersect[0]
    ideal_x = linefinder.im_cols / 2
    x_strafe(s, actual_x, ideal_x, scale)
   
def move_to_last_line(s, linefinder):
    scale = float(320) / linefinder.im_cols
    actual_x = linefinder.lines[-1].intersect[0]
    ideal_x = linefinder.im_cols / 2
    x_strafe(s, actual_x, ideal_x, scale)

def move_to_x(s, im_cols, dest):
    scale = float(320) / im_cols
    ideal_x = im_cols / 2
    return x_strafe(s, dest, ideal_x, scale)
