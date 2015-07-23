# Python modules
import time
# Local modules
from head.spine import spine, optical_move
from head.find_lines import current_lines

# Change this port if not on LINUX
s = spine.Spine(spine.DEF_LINUX_PORT)
s.startup()

values = {}
averages = {}
#to_test = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 1]
to_test = range(0, 4000, 500)
n = 2
for t in to_test:
    values[t] = []
    averages[t] = []

for i in range(n):
    for t in to_test:
        lf = current_lines(True, False)
        x1 = lf.lines[0].intersect[0]
        optical_move.x_move(s, t, 'left')
        lf = current_lines(True, False)
        x2 = lf.lines[0].intersect[0]
        print t, (x2 - x1)
        values[t].append(x2 - x1)
        optical_move.x_move(s, t, 'right')
        #lf = current_lines()
        #pixelmove.correct_baseline_error(s, lf.dist_to_baseline, lf.baseline_theta)

for key, value in values.items():
    averages[key] = float(sum(value)) / len(value)
print values
print averages

s.close()
