from utils.utils import split_lines
from collections import defaultdict

def mix_prune(secret, val):
    return (secret ^ val) % 16777216

def update_secret(secret):
    secret = mix_prune(secret, secret * 64)
    secret = mix_prune(secret, secret // 32)
    return mix_prune(secret, secret * 2048)


def check_prices(secret, mapping):
    prev = [None  ] * 4 # + [secret %10]
    seen =  set()
    current = secret
    # OR 2001?
    for _ in range(2000):
        #breakpoint()
        prev.pop(0)
        new = update_secret(current)
        price = new % 10
        difference = price - (current % 10)
        prev.append(difference)
        current = new
        key = tuple(prev)
        if key not in seen:
            mapping[key] += price
            seen.add(key)
    return current

def maximize_bananas(numbers):
    banana_record = defaultdict(lambda: 0)
    part1 = sum(check_prices(s, banana_record) for s in numbers)
    part2 = max(v  for k, v in banana_record.items() if None not in k )
    print(banana_record)
    return part1, part2


numbers = list(map(int, split_lines("inputs/day22.txt")))
part1, part2 = maximize_bananas(numbers)
print(part1)
print(part2)
