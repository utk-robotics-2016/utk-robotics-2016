# This script causes the robot to stop moving; useful if the script
# crashed mid-move

import spine

# Change this port if not on LINUX
s = spine.Spine(spine.DEF_LINUX_PORT)
s.startup()

s.move(0, 0, 0)
s.retract_rail(0)
s.close()
