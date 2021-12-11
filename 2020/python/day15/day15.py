
def output(array, turn):

    i = len(array)
    number = array[-1]
    index = {val:i+1 for i, val in enumerate(array[:-1])}
    while i < turn:
        if number in index:
            new_number = i - index[number]
            index[number] = i
        else:
            index[number] = i
            new_number = 0
        number = new_number
        i += 1

    return number


if __name__ == "__main__":
    assert output([0,3,6], 4) == 0
    assert output([0,3,6], 5) == 3
    assert output([0,3,6], 6) == 3
    assert output([0,3,6], 7) == 1  
    assert output([0,3,6], 8) == 0
    assert output([0,3,6], 9) == 4
    assert output([1,3,2], 2020) == 1
    assert output([2,1,3], 2020) == 10
    assert output([2,3,1], 2020) == 78
    assert output([3,2,1], 2020) == 438
    assert output([3,1,2], 2020) == 1836
    print(output([13,0,10,12,1,5,8], 2020))
    print(output([13,0,10,12,1,5,8], 30000000))

