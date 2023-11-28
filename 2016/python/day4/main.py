import pathlib

TEST_DATA = [
    "aaaaa-bbb-z-y-x-123[abxyz]",
    "a-b-c-d-e-f-g-h-987[abcde]",
    "not-a-real-room-404[oarel]",
    "totally-real-room-200[decoy]",
]


def load_content(fname):
    with open(fname) as fh:
        content = fh.readlines()
    return content


def parse_line(line):
    name_and_room, checksum = line.strip().split("[")
    checksum = checksum.strip("]")
    name = name_and_room[:-4]
    room = name_and_room[-3:]
    return name, room, checksum


def check_checksum(name, checksum):
    name = "".join(name.split("-"))
    keys = set(name)
    counter = {k: sum([1 for char in name if char == k]) for k in keys}
    counter = sorted(counter.items(), key=lambda x: (-x[1], x))
    check_sum_created = "".join([char for char, _ in counter[:5]])
    return check_sum_created == checksum


def test_parse():
    assert parse_line(TEST_DATA[0]) == ("aaaaa-bbb-z-y-x", "123", "abxyz")


def test_run():
    rooms = [parse_line(line) for line in TEST_DATA]
    assert [
        check_checksum(encryption, checksum) for encryption, _, checksum in rooms
    ] == [
        True,
        True,
        True,
        False,
    ]


if __name__ == "__main__":
    input_path = pathlib.Path(__file__).parent / "input.txt"
    lines = load_content(input_path)
    rooms = [parse_line(line) for line in lines]
    print(
        sum(
            [
                int(room)
                for encryption, room, checksum in rooms
                if check_checksum(encryption, checksum)
            ]
        )
    )
