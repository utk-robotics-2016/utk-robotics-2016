# Python modules
import time
import logging

# Local modules
from head.spine.core import get_spine
from head.spine.arm import get_arm
from head.spine.block_picking import BlockPicker
from head.spine.loader import Loader
from head.spine.Vec3d import Vec3d

fmt = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
# logging.basicConfig(format=fmt, level=logging.DEBUG, datefmt='%I:%M:%S')
logging.basicConfig(format=fmt, level=logging.INFO, datefmt='%I:%M:%S')
logger = logging.getLogger(__name__)

def findCenterOfBiggestMass(mask):
    contours, hierarchy = cv2.findContours(mask, 1, 2)
    biggestArea = -1
    biggestIndex = -1
    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if area > biggestArea:
            biggestArea = area
            biggestIndex = i
    M = cv2.moments(contours[biggestIndex])
    if M['m00'] != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        return (cx, cy)
    return (-1, -1)
	
# function to get position of cart
def get_color(color, hsv):
    mask = cv2.inRange(hsv, color[0], color[1])
    c = findCenterOfBiggestMass(mask)  #considering just returning the value of findCenterOfBiggestMass
    return c
	
def get_rail_zone_order():
	camera = cv2.VideoCapture(0)
	retval, img = camera.read()
    print(retval)
    cv2.imwrite("/home/kevin/tmp.jpg", img)
    camera.release()
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	red = [np.array([160, 128, 0]), np.array([180, 255, 255])]
	green = [np.array([70, 128, 0]), np.array([100, 255, 120])]
	blue = [np.array([100, 128, 100]), np.array([105, 255, 150])]
	yellow = [np.array([20, 150, 220]), np.array([30, 255, 255])]
    cr = ('red', get_color(red, hsv))
    cb = ('blue', get_color(blue, hsv))
    cg = ('green', get_color(green, hsv))
    cy = ('yellow', get_color(yellow, hsv))
    bins = [cr, cb, cg, cy]
    bins = sorted(bins, key=lambda color: color[1][0])
    # if there's an error, the coords will be (-1, -1) and the missing bin will be sorted into bins[0] 
    width = img.shape[1]    # get the width of the img to calculate the midpoint
    avg = np.mean([bins[1][0], bins[2][0], bins[3][0]])
    if (avg > width/2): # hard coding in the bin locations, I'm sure there's a better way
        bin_colors = [bins[1][0], bins[2][0], bins[3][0], bins[0][0]]
    else:
        bin_colors = [bins[0][0], bins[1][0], bins[2][0], bins[3][0]]
    return bin_colors

with get_spine() as s:
    with get_arm(s) as arm:
        class Robot:

            def __init__(self):
                self.ldr = Loader(s)
                self.bp = BlockPicker(s, arm)

                # set a threshold for white vs black values from the QTR sensor
                self.qtr_threshold = 800

                # Determine which course layout
                if s.read_switches()['course_mirror'] == 1:
                    # tunnel on left
                    self.course = 'B'
                    # dir_mod stands for direction modifier
                    self.dir_mod = 1
                else:
                    # tunnel on right
                    self.course = 'A'
                    self.dir_mod = -1
                logging.info("Using course id '%s' and dir_mod '%d'." % (self.course, self.dir_mod))

            def move_pid(self, speed, dir, angle):
                s.move_pid(speed, self.dir_mod * dir, self.dir_mod * angle)

            # moves with respect to the course layout
            def move(self, speed, dir, angle):
                s.move(speed, self.dir_mod * dir, self.dir_mod * angle)

            # rotate the orientation of the robot by 180 degrees
            def rotate_180(self):
                trapezoid(s.move_pid, (0, 0, 0), (0, 0, 1), (0, 0, 0), 1.74, rampuptime=.7, rampdowntime=1)

            # rotate the orientation of the robot by 90 degrees
            def rotate_90(self, dir):
                if dir == 'right':
                    angle = 0.5
                elif dir == 'left':
                    angle = -0.5
                else:
                    raise ValueError

                trapezoid(s.move_pid, (0, 0, 0), (0, 0, angle), (0, 0, 0), 1.74, rampuptime=.7, rampdowntime=1)

            def move_to_corner(self):
                trapezoid(self.move_pid, (0, 0, 0), (1, 0, 0), (1, 0, 0), 3.8)
                self.move(0.9, -10, 0)
                time.sleep(4)
                s.stop()

                # move back a smidgen
                self.move_pid(.75, 180, 0)
                time.sleep(.1)
                self.move(1, 90, 0)
                time.sleep(1)

            def strafe_until_line_abs(self, color, dir, sensor='auto'):
                # determine movement and sensor
                if dir == 'left':
                    angle = 90
                elif dir == 'right':
                    angle = -90
                else:
                    raise ValueError

                if sensor == 'auto':
                    if self.course == 'B':
                        sensor = 'left'
                    else:
                        sensor = 'right'

                    if self.course == 'A':
                        sensor = 'right'
                    else:
                        sensor = 'left'

                logging.info("moving %s with sensor %s" % (dir, sensor))

                # start moving
                s.move_pid(0.6, angle, 0)

                # read the line sensor and stop when desired color is detected
                if color == 'black':
                    while s.read_line_sensors()[sensor] < self.qtr_threshold:
                        time.sleep(0.01)
                elif color == 'white':
                    while s.read_line_sensors()[sensor] > self.qtr_threshold:
                        time.sleep(0.01)
                else:
                    raise ValueError
                # This function does not stop the movement after returning!

            def strafe_until_line(self, color, dir, sensor):
                # flip stuff for course A
                if self.course == 'A':
                    logging.info("Flipping command for A req: dir %s, sensor %s" % (dir, sensor))
                    if dir == 'left':
                        dir = 'right'
                    elif dir == 'right':
                        dir = 'left'

                    if sensor == 'left':
                        sensor = 'right'
                    elif sensor == 'right':
                        sensor = 'left'

                # call the actual strafe function
                self.strafe_until_line_abs(color, dir, sensor)

            def wait_until_arm_limit_pressed(self):
                logging.info("Waiting for arm limit press.")
                while not s.read_arm_limit():
                    pass

            def move_to_rail_zone(self, currzone, destzone, method='deadreckon'):
                if method == 'manual':
                    raw_input('Move me to zone %d' % (destzone))
                elif method == 'deadreckon':
                    if currzone == 3 and destzone == 0:
                        # Bump up against barge
                        s.move_for(5, 0.8, 0, 0.08)
                        # Bump against railroad
                        s.move_for(1, 0.6, -70, 0)
                        # Move away from railroad
                        s.move_for(1, 0.6, 70, 0)
                    elif currzone != -1:
                        trapezoid(self.move_pid, (0, 180, 0), (0.5, 180, 0), (0, 180, 0), 2.8)
                        s.stop()
                else:
                    raise ValueError

            def detect_blocks(self, level):
                # logger.info(arm.detect_blocks('top'))
                # '''
                blocks = []
                if level == 'bottom':
                    # Far right
                    blocks.append([{'color': 'blue', 'type': 'full'}])
                    blocks.append([{'color': 'red', 'type': 'full'}])
                    blocks.append([{'color': 'yellow', 'type': 'full'}])
                    blocks.append([{'color': 'green', 'type': 'full'}])
                    blocks.append([{'color': 'red', 'type': 'full'}])
                    blocks.append([{'color': 'blue', 'type': 'full'}])
                    blocks.append([{'color': 'green', 'type': 'full'}])
                    blocks.append([{'color': 'green', 'type': 'full'}])
                    # Far left
                elif level == 'top':
                    # Far right
                    blocks.append([{'color': 'green', 'type': 'full'}])
                    blocks.append([{'color': 'yellow', 'type': 'full'}])
                    blocks.append([{'color': 'yellow', 'type': 'full'}])
                    blocks.append([{'color': 'blue', 'type': 'full'}])
                    blocks.append([{'color': 'blue', 'type': 'full'}])
                    blocks.append([{'color': 'red', 'type': 'full'}])
                    blocks.append([{'color': 'yellow', 'type': 'full'}])
                    blocks.append([{'color': 'red', 'type': 'full'}])
                    # Far left
                else:
                    raise ValueError
                # '''
                return blocks

            def get_rail_zone_color(self, zid):
                colors = get_rail_zone_order()
                return colors[zid]

            def unload_rail(self):
                lastzid = -1
                # for level in ['top', 'bottom']:
                for level in ['top']:
                    blocks = self.detect_blocks(level)
                    for b in blocks:
                        assert b[0]['type'] == 'full'
                    for zid in range(4):
                        self.move_to_rail_zone(lastzid, zid)
                        color = self.get_rail_zone_color(zid)
                        indices = []
                        for i, b in enumerate(blocks):
                            if b[0]['color'] == color:
                                indices.append(i)
                        logging.info('%s blocks at %s.' % (color, indices))
                        for i in indices:
                            self.bp.pick_block(i, level, 'full')
                            side = {'B': 'right', 'A': 'left'}[self.course]
                            self.bp.drop_block(rail=True, side=side)
                        lastzid = zid

            def arm_to_vertical(self):
                # ...Vec3d(left/right, forward, height), radians, something)
                
                # moves vertical
                arm.move_to(Vec3d(11, -4, 10), 0, 180)
                # if it is on course A, turn 180
                if self.course == 'A':
                    arm.move_to(Vec3d(-11, -4, 10), 1.04, 180)
                    #time.sleep(0.5)
                    # arm.move_to(Vec3d(-11, -4, 10), 1.04, 180)


            def start(self):
                self.arm_to_vertical()
                # waits until button pressed, then reset
                # self.wait_until_arm_limit_pressed()
                bins = get_rail_zone_order()
                time.sleep(0.5)
                print(bins)
                arm.move_to(Vec3d(-11, -4, 10), 0, 180)
                arm.move_to(Vec3d(11, -4, 10), 0, 180)

        bot = Robot()

        bot.wait_until_arm_limit_pressed()
        time.sleep(0.5)
        bot.start()
        
