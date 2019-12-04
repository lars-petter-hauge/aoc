from textwrap import wrap
from collections import Counter

def is_valid(password):
    if len(str(password)) != 6:
        return False
    password = [int(c) for c in str(password)]

    includes_doubles = False
    repeated = []
    previous = password[0]

    for digit in password[1:]:
        if digit < previous:
            return False
        if digit == previous:
            repeated.append(digit)
        previous = digit

    count = Counter(repeated)
    if any([True for _,v in count.items() if v==1]):
        includes_doubles = True

    if not includes_doubles:
        return False

    return True

def run():
    valid_digits = [numbah for numbah in range(402328, 864247+1) if is_valid(numbah)]
    print(len(valid_digits))

if __name__ == '__main__':
    assert is_valid(111123) == False
    assert is_valid(122345) == True
    assert is_valid(111111) == False
    assert is_valid(223450) == False
    assert is_valid(123789) == False
    assert is_valid(112233) == True
    assert is_valid(123444) == False
    assert is_valid(111122) == True

    run()