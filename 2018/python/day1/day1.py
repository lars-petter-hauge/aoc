from itertools import cycle
 
def parse_data(data):
    parsed = [int(x.split()[0]) for x in data]
    return parsed

def read_input(fname):
    with open(fname) as f:
        data=f.readlines()
    parsed = parse_data(data)
    return parsed

def evaluate(input_list, start, frequency_list):
    for element in cycle(data):
        if start not in frequency_list:
            frequency_list.add(start)
        else:
            print("frequency {} found twice".format(start))
            break
        start += element
    return start

def main(data):
    evaluate(data,0, set())

if __name__ == '__main__':
    data = read_input('day1input')
    main(data)
