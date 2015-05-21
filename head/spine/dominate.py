# Python modules
import time
# Third party modules
#import pyttsx
# Local modules
from head.spine import spine, pixelmove, zones
from head.find_lines import current_lines
from head.index_blocks import current_blocks

# Change this port if not on LINUX
s = spine.Spine(spine.DEF_LINUX_PORT)
s.startup()

# Text to speech
#engine = pyttsx.init()
#engine.say('starting run')
#engine.runAndWait()

def seconds_to_inches(seconds):
    return seconds*12.7

class Robot:
    def __init__(self):
        self.block_a = None
        self.block_b = None
        self.start_of_blocks = None
    
    def corner_up(self, drop_off):
        # Line up with corner
        lf = current_lines(drop_off, True)
        pixelmove.move_to_first_line(s, lf)
        pixelmove.correct_baseline_error(s, lf)
    
    def pick_up(self, bf, block):
        seconds_forward = 0.28 * pixelmove.move_to_x(s, bf.im_cols, block.moment)
        s.move_for(0.3, 0.4, 0, 0)
        s.move_for(0.3, 0.4, 180, 0)
        print 'Picked up:', block.color, block.get_type()
        return seconds_forward
        
    def drop_off_to(self, bf, zone):
        seconds_forward = 0.28 * pixelmove.move_to_x(s, bf.im_cols, zone.moment)
        s.move_for(0.3, 0.4, 0, 0)
        s.move_for(0.3, 0.4, 180, 0)
        print 'Dropped off:', zone.color
        return seconds_forward
        
    def pick_up_two(self):
        self.corner_up(False)
        
        assert self.block_a == None
        assert self.block_b == None
        
        # STATE VARIABLES
        finished = False
        # Used as rough estimate of how far along the line we've moved
        seconds_from_first = 0
        seconds_to_move = 3.3

        if self.start_of_blocks:
            print "Moving", self.start_of_blocks, "seconds right to save time."
            seconds_from_first += self.start_of_blocks
            s.move_for(self.start_of_blocks, .9, -90, 0)

        while seconds_from_first < seconds_to_move and not finished:
            # Update current position
            bf = current_blocks(False, True)
            pixelmove.correct_baseline_error(s, bf.lf)
    
            # Debug where we think we are and the blocks we see
            print str(seconds_from_first) + ':'
            for block in bf.blocks:
                print block.color, block.get_type(), block.height
    
            # See if we can pick up a block
            just_picked_up = False
            for block in bf.blocks:
                # If we are looking for the second block
                if self.block_a:
                    # Make sure it is the right type
                    if block.get_type() == self.block_a.get_type():
                        # Hopefully it's not the same color. Should not happen
                        if block.color != self.block_a.color:
                            #engine.say(block.color + ' ' + block.get_type() + ' oh yeah')
                            #engine.runAndWait()
                            seconds_from_first += self.pick_up(bf, block)
                            self.block_b = block
                            just_picked_up = True
                            # Break out of the for loop. Don't pick up any more blocks
                            finished = True
                            break
                # If we are looking for the first block
                else:
                    # Rule out empty slots and air blocks
                    if block.color != 'black' and block.get_type() != 'air':
                        #engine.say(block.color + ' ' + block.get_type() + ' oh yeah')
                        #engine.runAndWait()
                        seconds_from_first += self.pick_up(bf, block)
                        # So we know where to move up to next time around:
                        if seconds_from_first > 0:
                            self.start_of_blocks = seconds_from_first
                        self.block_a = block
                        just_picked_up = True
                        # Break so that we don't try to pick up another without rescanning
                        break

            # Continue on down the line if we didn't find anything
            if not just_picked_up:
                seconds_from_first += .7
                s.move_for(.7, .9, -90, 0)

        return seconds_to_inches(seconds_from_first), seconds_from_first

    # Very similar to pick_up_two()
    def drop_off(self):
        self.corner_up(True)
       
        # Make sure we have two blocks 
        assert self.block_a != None
        assert self.block_b != None
        
        # STATE VARIABLES
        finished = False
        # Used as rough estimate of how far along the line we've moved
        zone_a_at = None # This is if we see where our second drop should be
        seconds_from_first = 0
        seconds_to_move = 1.6

        while seconds_from_first < seconds_to_move and not finished:
            # Update current position
            bf = current_blocks(True, True)
            pixelmove.correct_baseline_error(s, bf.lf)
    
            # Debug where we think we are and the zones we see
            print str(seconds_from_first) + ':'
            for block in bf.blocks:
                print block.color, block.get_type(), block.height
    
            # See if we can drop off a block
            # We need to make sure to drop these off in order
            just_dropped_off = False
            # Treat blocks as zones
            for zone in bf.blocks:
                # If we need to place block B:
                if self.block_b:
                    # Make sure it is the right color
                    if zone.color == self.block_b.color:
                        seconds_from_first += self.drop_off_to(bf, zone)
                        self.block_b = None
                        just_dropped_off = True
                        # Break out of the for loop. Don't drop off any more blocks
                        break
                    elif zone.color == self.block_a.color:
                        if zone_a_at == None:
                            zone_a_at = seconds_from_first
                        else:
                            print "taking average of zone_a_at:", zone_a_at
                            zone_a_at += seconds_from_first
                            zone_a_at /= 2
                        print "Found zone A!!! Taking note at", zone_a_at, "seconds."
                # If we need to place block A
                else:
                    # Make sure it is the right color
                    if zone.color == self.block_a.color:
                        seconds_from_first += self.drop_off_to(bf, zone)
                        self.block_a = None
                        just_dropped_off = True
                        # Break out of the for loop. Don't drop off any more blocks
                        finished = True
                        break
            # Continue on down the line if we didn't find anything
            if not just_dropped_off:
                seconds_from_first += .7
                s.move_for(.7, .9, -90, 0)
            # If we already know where zone A is at
            elif (zone_a_at != None) and not finished:
                diff = seconds_from_first - zone_a_at
                if diff >= 0:
                    s.move_for(diff, .9, 90, 0)
                else: # Don't think this will happen, but if so:
                    s.move_for(abs(diff), .9, -90, 0)
                seconds_from_first = zone_a_at

        return seconds_to_inches(seconds_from_first)

    def game_time(self):
        return time.time() - self.start_time

    def start(self):
        self.start_time = time.time()
        # Move to row of blocks
        zones.to_zone(s, 0, 1)

        #engine.say('starting scan')
        #engine.runAndWait()

        # Main loop. Does not handle air. Should run 6 times.
        i = 6 # Run this loop 6 times:
        while i != 0:
            i -= 1

            print "Starting run %d. Game time is %f." % (6-i, self.game_time())

            # Scan right for two blocks
            inches_away, seconds_away = self.pick_up_two()
            print "I think I am", inches_away, "inches away."
            dest = None
            # Make sure we picked up blocks before trying to drop them off
            if self.block_a:
                if self.block_a.get_type() == 'sea':
                    dest = 3
                elif self.block_a.get_type() == 'rail':
                    dest = 4
                # Move to right placement zone
                zones.x_slide(s, inches_away, dest)
    
                # Drop off blocks
                inches_away = self.drop_off()
                # Block A is not "dropped off" yet
                self.block_a = None
    
                # Return to line of blocks
                zones.x_return(s, inches_away, dest, 1)
            # If we didn't actually pick up blocks, head back to start
            else:
                print "Ahh! Didn't find any blocks! Heading back to start."
                s.move_for(seconds_away, .9, 90, 0)
                # Just in case our time saver caused this problem
                self.start_of_blocks = None
                # Don't count this run as one of our 6 runs
                i += 1

        # AIR CODE GOES HERE
        
        print "WOOHOO!! We won the competition!!"
        print "Game time is %f." % self.game_time()

# Tare compass before every run
s.tare_compass()
bot = Robot()
bot.start()

s.close()
