def load_content(fname):
    with open(fname) as fh:
        return [l.strip() for l in fh.readlines()]


def parse_content(lines):
    return [(l.split()[0], int(l.split()[1])) for l in lines]


def run_sub(instructions):
    aim, hor, ver = 0, 0, 0
    for (direction, length) in instructions:
        if direction == "forward":
            hor += length
            ver += length * aim
            continue
        if direction == "up":
            aim -= length
        elif direction == "down":
            aim += length
        else:
            raise NotImplementedError(f"Not implemented for direction {direction}")
    return hor, ver


content = load_content("input.txt")
instructiones = parse_content(content)
hor, ver = run_sub(instructiones)

print(hor * ver)
