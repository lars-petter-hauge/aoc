import operator
import pyparsing as pp

def rec_string_evaluator(string):
    op = None
    total = 0
    i = 0
    for _ in range(len(string)):
        if i == len(string):
            # Can occur if the string ends in a ")"
            # In such a case sub sum has already been
            # included in the total and we are good to go!
            break
        symbol = string[i]
        if symbol == "*":
            op = operator.mul
            i += 1
            continue
        if symbol == "+":
            op = operator.add
            i += 1
            continue
        if symbol == "(":
            sub, idx = rec_string_evaluator(string[i+1:])
            if op is None:
                total = sub
            else:
                total = op(sub, total)
            i += idx + 1
            continue
        if symbol == ")":
            i += 1
            break

        number = int(symbol)
        if op is None:
            total = number
        else:
            total = op(number, total)
        i += 1

    return total, i

def rec_string_evaluator_add_presedence(string):
    op = None
    total = ""
    i = 0
    eval_mult = "+" not in string

    for _ in range(len(string)):
        if i == len(string):
            # Can occur if the string ends in a ")"
            # In such a case sub sum has already been
            # included in the total and we are good to go!
            break
        symbol = string[i]
        if symbol == "*":
            op = operator.mul
            i += 1
            continue
        if symbol == "+":
            op = operator.add
            i += 1
            continue
        if symbol == "(":
            sub, idx = rec_string_evaluator(string[i+1:])
            if op is None:
                total = sub
            else:
                total = op(sub, total)
            i += idx + 1
            continue
        if symbol == ")":
            i += 1
            break

        number = int(symbol)
        if op is None:
            total = number
        elif op is operator.add:
            total = op(number, total)
        elif op is operator.mul:
            if eval_mult:
                total = op(number, total)
            else:
                pass
        i += 1

    return total


def eval_paranthesis(st):
    total = ""
    if "(" not in st:
        return str(rec_string_evaluator_add_presedence(st))
    start = st.find("(")
    end = st.find(")")

    if "(" not in st[start+1:]:
        return str(rec_string_evaluator_add_presedence(st[start+1:end])) + st[end:]

    # Check if an opening bracket precedes the closing bracket.
    # if so we need to match that first.
    if st[start+1:].find("(") < st[start+1:].find(")"):
        idx = st[start+1:].find("(")
        total += eval_paranthesis(st[idx+1:])
    else:
        total += str(rec_string_evaluator_add_presedence(st[start+1:end]))
    total += eval_paranthesis(st[end:])

    return total

def load(fname):
    with open(fname) as fh:
        lines = fh.read()

    lines = lines.split("\n")
    lines = [l.replace(" ", "") for l in lines]
    return lines

def run(lines):
    total = 0
    for line in lines:
        total += rec_string_evaluator(line)[0]
    return total

if __name__ == "__main__":
    assert rec_string_evaluator("1 + 2 * 3 + 4 * 5 + 6".replace(" ", ""))[0] == 71
    assert rec_string_evaluator("1 + (2 * 3) + (4 * (5 + 6))".replace(" ", ""))[0] == 51
    assert rec_string_evaluator("2 * 3 + (4 * 5)".replace(" ", ""))[0] == 26
    assert rec_string_evaluator("5 + (8 * 3 + 9 + 3 * 4 * 3)".replace(" ", ""))[0] == 437
    assert rec_string_evaluator("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))".replace(" ", ""))[0] == 12240
    assert rec_string_evaluator("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2".replace(" ", ""))[0] == 13632

    #print(run(load("2020/python/day18/input.txt")))
    print(eval_paranthesis("1 + (2 * 3) + (4 * (5 + 6))".replace(" ", "")))
    assert rec_string_evaluator_add_presedence("1 + (2 * 3) + (4 * (5 + 6))".replace(" ", ""))[0] == 51
    assert rec_string_evaluator_add_presedence("2 * 3 + (4 * 5)".replace(" ", ""))[0] == 46
    assert rec_string_evaluator_add_presedence("5 + (8 * 3 + 9 + 3 * 4 * 3)".replace(" ", ""))[0] == 1445
    assert rec_string_evaluator_add_presedence("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))".replace(" ", ""))[0] == 669060
    assert rec_string_evaluator_add_presedence("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2".replace(" ", ""))[0] == 23340
