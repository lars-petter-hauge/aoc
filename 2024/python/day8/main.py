import sys

TEST_INPUT = "2333133121414131402"

with open(sys.argv[1]) as fh:
    content = fh.read()

def somename(content):
    some = len(content)//2
    for i in reversed(range(0,len(content), 2)):
        for _ in range(int(content[i])):
            yield some
        some -= 1

def solve(content):
    reversed_content = list(somename(content))
    is_block = True
    result = []

    for idx, dig in enumerate(content):
        dig = int(dig)
        if is_block:
            for _ in range(dig):
                if len(reversed_content)==0:
                    break
                result.append(str(idx//2))
                reversed_content.pop()
            is_block = False
        else:
            for _ in range(dig):
                if len(reversed_content)==0:
                    break
                result.append(str(reversed_content.pop(0)))
            is_block = True


    return result
result = solve(TEST_INPUT)
print("".join(result))
print(sum([int(c)*idx for idx, c in enumerate(result)]))
a=2
result = solve(content.strip())
print(sum([int(c)*idx for idx, c in enumerate(result)]))
