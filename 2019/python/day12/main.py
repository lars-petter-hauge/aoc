import itertools

def apply_gravity(moons):
    for moon1, moon2 in itertools.combinations(moons,2):
        for axis in range(3):
            if moon1["position"][axis] < moon2["position"][axis]:
                moon1["velocity"][axis] += 1
                moon2["velocity"][axis] -= 1
            elif moon1["position"][axis] > moon2["position"][axis]:
                moon1["velocity"][axis] -= 1
                moon2["velocity"][axis] += 1

def update_position(moons):
    for moon in moons:
        for axis in range(3):
            moon["position"][axis] += moon["velocity"][axis]

def calculate_energy(moon):
    pot = [abs(x) for x in moon["position"]]
    kin = [abs(x) for x in moon["velocity"]]
    return sum(pot) * sum(kin)

def run(moons, steps):
    step = 0
    while step < steps:
        apply_gravity(moons)
        update_position(moons)
        step += 1
    return sum((calculate_energy(moon) for moon in moons))

def test():
    positions = [[-1, 0, 2], [2, -10, -7], [4, -8, 8], [3, 5, -1]]
    moons = [{"velocity": [0, 0, 0], "position": p} for p in positions]
    assert (run(moons,10), 179)

    positions = [[-8, -10, 0], [5, 5, 10], [2, -7, 3], [9, -8, -3]]
    moons = [{"velocity": [0, 0, 0], "position": p} for p in positions]
    assert (run(moons,100), 1940)

def main():
    positions = [[-10, -13, 7], [1, 2, 1], [-15, -3, 13], [3, 7, -4]]
    moons = [{"velocity": [0, 0, 0], "position": p} for p in positions]
    print(run(moons,1000))

test()
main()