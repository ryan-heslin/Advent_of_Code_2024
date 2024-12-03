import re

# input = split_lines("inputs/day3.txt")
# input = "".join(inpput)
with open("inputs/day3.txt") as f:
    input = f.read().replace("\n", "")
part1 = part2 = 0

matches = re.findall(r"(do)\(\)|(don't)\(\)|mul\((\d+),(\d+)\)", input)
do = True

for m in matches:
    if m[0] == "do":
        do = True
    elif m[1] == "don't":
        do = False
    else:
        val = int(m[2]) * int(m[3])
        part1 += val
        if do:
            part2 += val

print(part1)
print(part2)
