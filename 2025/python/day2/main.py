import sys

TEST = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124"""


def id_valid(tag):
    tag = str(tag)
    a, b = tag[len(tag) // 2 :], tag[: len(tag) // 2]
    return a != b


def id_valid_part2(tag):
    tag = str(tag)
    for n in range(1, len(tag) // 2 + 1):
        if len(set([tag[i : i + n] for i in range(0, len(tag), n)])) == 1:
            return False
    return True


content = TEST
content = sys.stdin.read()
p1 = []
p2 = []
for tag_range in content.split(","):
    start, stop = tag_range.split("-")
    print(f"checking tag_range:{tag_range}, tags to check: {int(stop) - int(start)}")
    for number in range(int(start), int(stop) + 1):
        if not id_valid(number):
            p1.append(number)
        if not id_valid_part2(number):
            p2.append(number)


print(sum(p1))

print(sum(p2))
