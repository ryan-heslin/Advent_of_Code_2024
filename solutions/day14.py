import re
from functools import reduce
from itertools import product
from operator import mul
from utils.utils import split_lines, count_dict, list_map

pattern = """###############################
#                             #
#                             #
#                             #
#                             #
#              #              #
#             ###             #
#            #####            #
#           #######           #
#          #########          #
#            #####            #
#           #######           #
#          #########          #
#         ###########         #
#        #############        #
#          #########          #
#         ###########         #
#        #############        #
#       ###############       #
#      #################      #
#        #############        #
#       ###############       #
#      #################      #
#     ###################     #
#    #####################    #
#             ###             #
#             ###             #
#             ###             #
#                             #
#                             #
#                             #
#                             #
###############################"""
TOP = STUMP = None

for line in pattern.splitlines():
    if re.match(r"^#\s{4}#+\s{4}#$", line):
        TOP = re.compile("^.*(" + line + ").*$")
    elif re.match(r"^#\s+#{3}\s+#$", line):
        STUMP = line

assert TOP is not None and STUMP is not None

def parse(line):
    nums = re.findall(r"-?\d+", line)
    return dict(zip(("xpos", "ypos", "xdel", "ydel"), map(int, nums)))


def display(graph, xmax, ymax):
    return "\n".join(
        "".join("#" if graph[complex(col, row)] else " " for col in range(xmax))
        for row in range(ymax)
    )


# Sigh....


def is_ascending(l):
    # https://stackoverflow.com/questions/34684461/check-if-a-list-contains-incrementing-elements-starting-from-zero
    return l == list(range(l[0], len(l)))


def find_tree(data, xmax, ymax):
    graph = {complex(x, y): 0 for x, y in product(range(xmax), range(ymax))}
    for pair in data:
        graph[complex(pair["xpos"], pair["ypos"])] += 1

    iteration = 0
    # TODO: check for horizontal and vertical bars of the correct length?
    while iteration < 11000:
        for i, pair in enumerate(data):
            xpos = pair["xpos"]
            ypos = pair["ypos"]
            graph[complex(xpos, ypos)] -= 1
            xpos += pair["xdel"]
            ypos += pair["ydel"]
            xpos %= xmax
            ypos %= ymax
            data[i]["xpos"] = xpos
            data[i]["ypos"] = ypos
            graph[complex(xpos, ypos)] += 1

        iteration += 1
        # if iteration == 7603:
        #     breakpoint()
        text = display(graph, xmax, ymax).splitlines()
        for i, line in enumerate(text):
            m = re.match(TOP, line)
            if m:
                span = m.span(1)
                if (i < len(text) - 3) and (
                    text[i + 1][span[0] : span[1]]
                    == text[i + 2][span[0] : span[1]]
                    == text[i + 3][span[0]: span[1]]
                    == STUMP
            ):
                    return iteration


def count(data, xlim, ylim, n):
    # Using conventional coordinates for once
    positions = count_dict()
    # In TRBL order
    quadrants = dict(zip(range(4), [0] * 4))
    quadrants[-1] = 0
    xmid = xlim // 2
    ymid = ylim // 2

    for pair in data:
        xpos = pair["xpos"]
        ypos = pair["ypos"]
        for _ in range(n):
            xpos += pair["xdel"]
            ypos += pair["ydel"]
            xpos %= xlim
            ypos %= ylim
        right = xpos > xmid
        lower = ypos > ymid
        middle = (xpos == xmid) or ypos == ymid
        if middle:
            quadrant = -1
        elif right:
            quadrant = int(lower)
        else:
            quadrant = 3 - lower

        quadrants[quadrant] += 1
        positions[complex(xpos, ypos)] += 1

    quadrants.pop(-1)
    return reduce(mul, quadrants.values())


data = split_lines("inputs/day14.txt")
parsed = list_map(data, parse)
xmax = 101
ymax = 103
part1 = count(parsed, xmax, ymax, 100)
print(part1)
part2 = find_tree(parsed, xmax, ymax)
print(part2)
