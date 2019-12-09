from collections import Counter
from itertools import chain
import matplotlib.pyplot as plt

def load_input(fname):
    with open(fname) as f:
        lines = f.readlines()
    return [int(c) for c in lines[0]]

def count_values(img_data, num_pixels):
    pos = 0
    layers = []
    
    while pos+num_pixels <= len(img_data):
        count = Counter()
        for i in range(num_pixels):
            count.update([img_data[pos+i]])
        pos += num_pixels
        layers.append(count)
    return layers

def part_1(img_data):
    layers = count_values(img_data, 25*6)
    minimum_layer = layers[0]
    for layer in layers[1:]:
        if layer[0]<minimum_layer[0]:
            minimum_layer = layer
    print(minimum_layer[1]*minimum_layer[2])

def pixel_value(pixel, img_data, pixel_size):
    values = []
    while pixel < len(img_data):
        value = img_data[pixel]
        if value != 2:
            return value
        pixel += pixel_size
    raise ValueError

def pos2ij(pos, width):
    row = pos//width
    col = pos - width * row
    return col, row

def translate_image(img_data, width, height):
    img = [[2]*width for _ in range(height)]

    for pos in range(width * height):
        i, j = pos2ij(pos, width)
        img[j][i] = pixel_value(pos, img_data, width*height)

    return img

def run():
    img_data = load_input('day8/input.txt')
    part_1(img_data)
    img_data = translate_image(img_data, 25, 6)
    fig = plt.figure()
    plt.imshow(img_data)
    plt.show()


def run_tests():
    img_data = [int(c) for c in '123456789012']
    layers = count_values(img_data, 3*2)
    img_data = translate_image([int(c) for c in '0222112222120000'], 2, 2)

    layer1 = "22022222"
    layer2 = "12122222"
    layer3 = "12122110"
    layer4 = "00212002"
    layer5 = "20120002"
    img_data = [[int(c) for c in l] for l in [layer1, layer2, layer3, layer4, layer5]]
    img_data = list(chain.from_iterable(img_data))
    img_data = translate_image(img_data, 4, 2)
    assert img_data[0] == [1, 0, 0, 1]
    assert img_data[1] == [0, 1, 1, 0]
    # output:
    # 1001
    # 0110

    # 5 layers

    # 2202
    # 2222

    # 1212
    # 2222

    # 1212
    # 2110

    # 0021
    # 2002

    # 2012
    # 0002

if __name__ == '__main__':
    run_tests()
    run()
