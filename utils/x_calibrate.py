# Local modules
from head.spine import spine
from head.find_lines import current_lines

# Change this port if not on LINUX
s = spine.Spine(spine.DEF_LINUX_PORT)
s.startup()

values = {}
averages = {}
to_test = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 1]
n = 2
for t in to_test:
    values[t] = []
    averages[t] = []

for i in range(n):
    for t in to_test:
        lf = current_lines()
        x1 = lf.lines[0].intersect[0]
        s.move_for(t, .4, 90, 0)
        lf = current_lines()
        x2 = lf.lines[0].intersect[0]
        print t, (x2 - x1)
        values[t].append(x2 - x1)
        s.move_for(t, .4, -90, 0)
        # lf = current_lines()
        # pixelmove.correct_baseline_error(s, lf.dist_to_baseline, lf.baseline_theta)

for key, value in values.items():
    averages[key] = float(sum(value)) / len(value)
print values
print averages

s.close()
