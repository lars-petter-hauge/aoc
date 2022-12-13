import itertools
from typing import DefaultDict
import numpy as np
from collections import Counter


def load_data(path):
    with open(path) as fh:
        lines = fh.readlines()

    name = None
    tile = np.zeros((10, 10))
    results = {}
    rowcount = 0
    for line in lines:
        if line.startswith("Tile"):
            name = line[5:9]
            continue

        if line == "\n":
            results[name] = tile
            tile = np.zeros((10, 10))
            rowcount = 0
            continue

        line = line.strip("\n")
        row = [1 if c == "#" else 0 for c in line]
        tile[rowcount] = row
        rowcount += 1
    results[name] = tile

    return results


def tile_side_match(tile_one, tile_two):
    if all(tile_one[0] == tile_two[-1]):
        return "N"
    if all(tile_one[-1] == tile_two[0]):
        return "S"
    if all(tile_one[:, :1] == tile_two[:, -1:]):
        return "W"
    if all(tile_one[:, -1:] == tile_two[:, :1]):
        return "E"
    return False


def inverse_rot(rot, func_name):
    INVERSE_ROT = {
        0: 0,
        1: 3,
        2: 2,
        3: 1,
    }
    if func_name == "<lambda>":
        return INVERSE_ROT[rot]
    else:
        return rot


def opposite_side(side_name):
    INVERSE_ROT = {
        "W": "E",
        "E": "W",
        "N": "S",
        "S": "N",
    }
    return INVERSE_ROT[side_name]


def connected_tiles(tiles):
    """Returns a dict of tile names and their respective connection

    Each connected tile to the key tile will be added in the list of connection
    including how the connected tile must be manipulated (rotated and/or flipped)
    in order for the borders to allign
    """
    sides_matching = DefaultDict(list)
    for name_one, name_two in itertools.combinations(tiles.keys(), 2):
        tile_one = tiles[name_one]
        tile_two = tiles[name_two]

        for rotation, flip_func in itertools.product(
            [0, 1, 2, 3], [lambda x: x, np.flipud, np.fliplr]
        ):
            side_match = tile_side_match(
                tile_one, flip_func(np.rot90(tile_two, rotation))
            )

            if side_match:
                # Add to both tiles, with direction on how to manipulate the other
                # tile in order for them to align
                sides_matching[name_one].append(
                    (name_two, side_match, rotation, flip_func.__name__)
                )
                old_side_match = side_match
                side_match = tile_side_match(
                    tile_two,
                    flip_func(
                        np.rot90(tile_one, inverse_rot(rotation, flip_func.__name__))
                    ),
                )
                if side_match != opposite_side(old_side_match):
                    a = 2
                sides_matching[name_two].append(
                    (
                        name_one,
                        opposite_side(side_match),
                        inverse_rot(rotation, flip_func.__name__),
                        flip_func.__name__,
                    )
                )
                # Two tiles can be connected in multiple ways of manipulation - we only need a single
                break

    return sides_matching


def edge_tiles(matches):
    counter = Counter({k: len(v) for k, v in matches.items()})
    corner_tiles = [k for k, v in counter.items() if v == 2]
    border_tiles = [k for k, v in counter.items() if v == 3]
    return corner_tiles, border_tiles


def arrange_tiles(connected_tiles, tiles):
    tile_map = [[]]
    row = 0
    corner_tiles, _ = edge_tiles(connected_tiles)

    current_tile = corner_tiles[0]
    placed = {current_tile}
    tile_map[row].append(current_tile)
    direction = "E"
    # Direction of placement is:
    # >----->---->--\/
    # \/----<----<---<
    # >----->---->
    while len(placed) < len(tiles.keys()):
        possible_tiles = connected_tiles[current_tile]
        try:
            selected_tile = [
                [t, rot, flip]
                for t, side, rot, flip in possible_tiles
                if side.startswith(direction)
            ][0]
        except IndexError:
            raise ValueError(
                f"Did not find a valid tile to {current_tile} for the list of candidates: {possible_tiles}"
                f" - looked in {direction} direction. Placed {len(placed)} tiles"
            )
        tile_map[row].append(selected_tile[0])
        direction = None


def main(path):
    tiles = load_data(path)
    conn_tiles = connected_tiles(tiles)
    arrange_tiles(conn_tiles, tiles)


def run_test_input(path, value):
    tiles = load_data(path)
    conn_tiles = connected_tiles(tiles)
    corner_tiles, _ = edge_tiles(conn_tiles)
    assert np.prod([int(name) for name in corner_tiles]) == value


run_test_input("test_input.txt", 20899048083289)
run_test_input("input.txt", 68781323018729)
main("test_input.txt")
