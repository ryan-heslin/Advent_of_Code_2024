def parse(digits):
    # id, length
    result = []
    for i, digit in enumerate(digits):
        digit = int(digit)
        mem_id = i // 2 if i % 2 == 0 else None
        if digit > 0:
            result.append([mem_id, digit])

    return result


def block_compact(memory):
    #breakpoint()
    current_block_index = len(memory) - 1

    while current_block_index > 0:
        current_block = memory[current_block_index]
        # Trailing free space
        if current_block[0] is None:
            if current_block_index == len(memory) - 1:
                memory.pop()
            current_block_index -= 1
        else:
            block_id, block_size = current_block
            for  candidate_space in range(current_block_index):
                # No space found
                memory_block = memory[candidate_space]
                # Not a free space
                if memory_block[0] is not None:
                    continue
                memory_size = memory_block[1]
                if not (memory_size < block_size):
                    #breakpoint()
                    # Exactly enough space
                    memory[current_block_index][0] = None
                    if memory_size == block_size:
                        memory[candidate_space][0] = block_id
                    # More space than needed
                    elif memory_size > block_size:
                        # Index unchanged since new block pushes up 1
                        memory[candidate_space] = [block_id, block_size]
                        memory.insert(
                            candidate_space + 1, [None, memory_size - block_size]
                        )
                    break
            else:
                current_block_index -= 1 

    return memory


def compact(memory):
    current_space = 1

    while current_space < len(memory):
        if memory[current_space][0] is not None:
            current_space += 1
            continue
        rightmost = memory[-1]
        # Trim empty space
        if rightmost[0] is None:
            memory.pop()
        else:
            data_size = rightmost[1]
            space_size = memory[current_space][1]
            if data_size >= space_size:
                memory[current_space][0] = rightmost[0]
                # Not enough space for whole block, so fill and move to next space
                if data_size > space_size:
                    rightmost[1] -= space_size
                # Exactly enough space
                else:
                    memory.pop()
                current_space += 2
            # More than enough space
            else:
                memory[current_space] = [rightmost[0], data_size]

                space_size -= data_size
                current_space += 1
                memory.insert(current_space, [None, space_size])
                memory.pop()
    return memory


def collapse(memory):
    i = 0
    while i < len(memory) - 1:
        if memory[i + 1][0] == memory[i][0]:
            memory[i][1] += memory[i + 1][1]
            memory.pop(i + 1)
        i += 1
    return memory


def checksum(memory):
    s = 0
    index = 0
    for block in memory:
        mem_id, size = block
        if mem_id is not None:
            s += sum(i * mem_id for i in range(index, index + size))
        index += size
    return s


with open("inputs/day9.txt") as f:
    number = f.read().rstrip("\n")

storage = parse(number)
compacted = collapse(compact(storage))
part1 = checksum(compacted)
print(part1)
compacted = collapse(block_compact(parse(number)))
part2 = checksum(compacted)
print(part2)
