TEST_INPUT = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""


def load_input(fname):
    with open(fname) as fh:
        return [l.strip() for l in fh.readlines()]


def populate_dir(linenr, lines, name):

    content = {"name": name, "size": 0, "dirs": [], "files": []}
    expected_dirs = []
    while linenr < len(lines):
        line = lines[linenr]
        linenr += 1
        if "cd .." in line:
            assert expected_dirs == [directory["name"] for directory in content["dirs"]]
            return linenr, content
        elif "cd " in line:
            name = line.split()[2]
            linenr, dir_content = populate_dir(linenr, lines, name)
            content["dirs"].append({"size": dir_content["size"], **dir_content})
            content["size"] += dir_content["size"]
        elif line[0].isnumeric():
            size, fname = line.split()
            size = int(size)
            content["files"].append((fname, size))
            content["size"] += size
        elif line[:3] == "dir":
            expected_dirs.append(line[4:])
        elif "ls" in line:
            pass
        else:
            raise NotImplementedError(f"Not implemented {line}")
    return linenr, content


def count_dirs_smaller_than(content, size):
    dirs_to_report = []
    total_size = 0
    if content["size"] < size:
        dirs_to_report.append(content["name"])
        total_size += content["size"]
    for directory in content["dirs"]:
        possibles, sub_size = count_dirs_smaller_than(directory, size)
        total_size += sub_size
        if possibles:
            dirs_to_report.extend(possibles)
    return dirs_to_report, total_size


def smallest_dir(content, min_size):
    best_size = 9999999999999
    for directory in content["dirs"]:
        sub_size = smallest_dir(directory, min_size)
        if sub_size > min_size and sub_size < best_size:
            best_size = sub_size
    if content["size"] < best_size:
        return content["size"]
    else:
        return best_size


linenr, content = populate_dir(0, TEST_INPUT.split("\n")[1:], name="/")
dirs, total_size = count_dirs_smaller_than(content, 100000)

total_space = 70000000
required_space = 30000000
space_to_delete = abs(total_space - content["size"] - required_space)
print(smallest_dir(content, space_to_delete))

linenr, content = populate_dir(0, load_input("input.txt"), name="/")
dirs, total_size = count_dirs_smaller_than(content, 100000)

total_space = 70000000
required_space = 30000000
space_to_delete = abs(total_space - content["size"] - required_space)
print(smallest_dir(content, space_to_delete))
