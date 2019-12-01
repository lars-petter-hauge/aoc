import unittest
import numpy as np


def parse_input(input):
    def spilt(x):
        x = x.split(',')
        return int(x[0]),int(x[1])

    result = [spilt(l) for l in input]
    return result
 
def read_input(fname):
    with open(fname) as f:
        input = f.readlines()
    return input


def euclidean_dist(a,b,c,d,):
    return abs(a-c)+abs(b-d)

def closest_point(i,j, coordinates):
    dist = 999999
    closest = 9999
    for k, (x,y) in enumerate(coordinates):
        new_dist = euclidean_dist(x,y,i,j)
        if new_dist<=dist:
            closest = k+1
            dist = new_dist
    return closest

def in_range(i, j, coordinates, threshold):
    dist=0
    for x,y in coordinates:
        dist += euclidean_dist(x,y,i,j)
    if dist >= threshold:
        return 0
    return 1

def populate_grid(coordinates, mini=None, maxi=None, minj=None, maxj=None, threshold=None):
    if not isinstance(mini, int):
        mini = mini or min([x for x,y in coordinates]) 
    if not isinstance(maxi, int):
        maxi = maxi or max([x for x,y in coordinates]) 
    if not isinstance(minj, int):
        minj = minj or min([y for x,y in coordinates]) 
    if not isinstance(maxj, int):
        maxj = maxj or max([y for x,y in coordinates]) 

    grid = np.zeros(shape=(maxi,maxj))
    for i in range(mini, maxi):
        for j in range(minj, maxj):
            if threshold:
                grid[i,j] = in_range(i, j, coordinates, threshold)
            else:
                grid[i,j] = closest_point(i, j, coordinates)
    return grid

def part_two(coordinates, threshold=None):
    grid = populate_grid(coordinates, threshold=threshold)
    return grid.sum()

def part_one(coordinates):
    grid_one = populate_grid(coordinates)
    grid_two = populate_grid(coordinates, mini=0, minj=0, maxi=400, maxj=400)

    unique_one, counts_one = np.unique(grid_one, return_counts=True)
    counter_one = dict(zip(unique_one, counts_one))

    unique_two, counts_two = np.unique(grid_two, return_counts=True)
    counter_two = dict(zip(unique_two, counts_two))

    check = {}
    for key, val in counter_one.items():
        if val == counter_two.get(key,0):
            check[key]=val

    max_key = max(check, key=check.get)
    return check[max_key]

class Test(unittest.TestCase):
    def test(self):
        coordinates =  [(1, 1),
                        (1, 6),
                        (8, 3),
                        (3, 4),
                        (5, 5),
                        (8, 9)]
        
        region = part_two(coordinates, threshold=32)
        assert  region == 16

if __name__ =='__main__':
    #unittest.main()
    input=read_input('day6input')
    parsed = parse_input(input)
    print(part_two(parsed, threshold=10000)) 
