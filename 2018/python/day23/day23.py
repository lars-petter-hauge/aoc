import unittest
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import itertools

def parse(lines):
    positions = []
    for line in lines:
        pos, rad = line.split()
        _, pos = pos.split('<')
        pos, _ = pos.split('>')
        coordinate = pos.split(',')
        coordinate = [int(x) for x in coordinate]
        _, rad = rad.split('=')
        rad = int(rad)
        positions.append((coordinate, rad))
    return positions

def remove_outlier(df_in, col_name):
    q1 = df_in[col_name].quantile(0.25)
    q3 = df_in[col_name].quantile(0.75)
    iqr = q3-q1 #Interquartile range
    fence_low  = q1-1.5*iqr
    fence_high = q3+1.5*iqr
    df_out = df_in.loc[(df_in[col_name] > fence_low) & (df_in[col_name] < fence_high)]
    return df_out

def read_data(fname):
    with open(fname) as f:
        result = f.readlines()
    return result

def distance(x, y):
    return abs(x[0]-y[0]) + abs(x[1]-y[1]) + abs(x[2]-y[2])

def inrange(pos_x, rad_x, pos_y):
    return rad_x >= distance(pos_x, pos_y)

def in_range(positions):
    positions_by_range = sorted([pos for pos in positions], key = lambda x: x[1], reverse = True)
    strongest_pos, strongest_rad = positions_by_range[0]
    bots_in_range = 0
    for pos, _ in positions_by_range:
        if inrange(strongest_pos, strongest_rad, pos):
            bots_in_range += 1
    return bots_in_range

def main():
    data = read_data('day23_input.txt')
    positions = parse(data)
    positions_two = [pos[0] + [pos[1]] for pos in positions]
    df = pd.DataFrame(positions_two)
    df.columns = ['x','y','z','rad']
    print(df.describe())
    #hist = df.hist(bins=10)
    ax = plt.axes(projection='3d')

    for col_name in ['x','y','z']:
        print("PRE: col: {} min: {}, max: {}".format(col_name, df[col_name].min(), df[col_name].max()))
        df = remove_outlier(df, col_name)
        print("POST: col: {} min: {}, max: {}".format(col_name, df[col_name].min(), df[col_name].max()))
        print(len(df))
    print(df.describe())
    x_range = df['x'].max()-df['x'].min()
    y_range = df['y'].max()-df['y'].min()
    z_range = df['z'].max()-df['z'].min()
    print("number of x elems: {:.2E}".format(x_range))
    print("number of y elems: {:.2E}".format(y_range))
    print("number of z elems: {:.2E}".format(z_range))
    print("number of elems: {:.2E}".format(x_range*y_range*z_range))
    #y_range = range(df['y'].min(), y_range+1)
    #z_range = range(df['z'].min(), z_range+1)
    #possible_coords = itertools.product(x_range, y_range, z_range)
    #print("length of possible coords: {}".format(len(possible_coords)))
    #ax.scatter3D(df['x'], df['y'], df['z'])
    #ax.scatter3D(df['x'], df['y'], df['z'], s=(df['rad']/df['rad'].mean())*10)
    ax.scatter3D(df['x'], df['y'], df['z'], c=df['rad'], cmap='Greens')
    #plt.hist(df['x'], bins=20)
    plt.show()
   #df.plot.hist(bins=10)
   # hist.show()
   #print(in_range(positions))

class Test(unittest.TestCase):
    def test(self):
        data = read_data('day23_testinput.txt')
        positions = parse(data)
        positions_two = [pos[0] + [pos[1]] for pos in positions]
        df = pd.DataFrame(positions_two)
        #df = df.transpose()
        df.columns = ['x','y','z','rad']
        print(df)
        print(df.describe())
        print(in_range(positions))
        assert in_range(positions) == 7


if __name__ == '__main__':
    #unittest.main()
    main()