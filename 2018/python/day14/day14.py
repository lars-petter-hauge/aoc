import unittest


def after_x_recipies(req_recipies):
    recipies = [3, 7]
    Alf = 0
    Elfie = 1
    while len(recipies) < req_recipies + 10:
        # print("Alf idx: {}, Elfie idx: {}, Alf score: {}, Elfie score: {}".format(Alf, Elfie, recipies[Alf], recipies[Elfie]))
        new_score = recipies[Alf] + recipies[Elfie]
        if len(str(new_score)) == 1:
            recipies.append(new_score)
        else:
            recipies.append(1)
            recipies.append(new_score % 10)
        Alf = (Alf + recipies[Alf] + 1) % len(recipies)
        Elfie = (Elfie + recipies[Elfie] + 1) % len(recipies)
    return recipies[req_recipies : req_recipies + 10]


def first_encounter(check_recipies):
    recipies = [3, 7]
    Alf = 0
    Elfie = 1
    while len(recipies) < 100000000:
        # print("Alf idx: {}, Elfie idx: {}, Alf score: {}, Elfie score: {}".format(Alf, Elfie, recipies[Alf], recipies[Elfie]))
        new_score = recipies[Alf] + recipies[Elfie]
        if len(str(new_score)) == 1:
            recipies.append(new_score)
        else:
            recipies.append(1)
            if recipies[-len(check_recipies) :] == check_recipies:
                return len(recipies) - len(check_recipies)
            recipies.append(new_score % 10)
        if recipies[-len(check_recipies) :] == check_recipies:
            return len(recipies) - len(check_recipies)
        Alf = (Alf + recipies[Alf] + 1) % len(recipies)
        Elfie = (Elfie + recipies[Elfie] + 1) % len(recipies)
    return 0


class Test(unittest.TestCase):
    def test(self):
        assert after_x_recipies(9) == [5, 1, 5, 8, 9, 1, 6, 7, 7, 9]
        assert after_x_recipies(5) == [0, 1, 2, 4, 5, 1, 5, 8, 9, 1]
        assert after_x_recipies(18) == [9, 2, 5, 1, 0, 7, 1, 0, 8, 5]
        assert after_x_recipies(2018) == [5, 9, 4, 1, 4, 2, 9, 8, 8, 2]

    def test2(self):
        assert first_encounter([5, 1, 5, 8, 9]) == 9
        assert first_encounter([0, 1, 2, 4, 5]) == 5
        assert first_encounter([9, 2, 5, 1, 0]) == 18
        assert first_encounter([5, 9, 4, 1, 4]) == 2018


if __name__ == "__main__":
    # unittest.main()

    # print("".join([str(x) for x in main(323081)]))
    print("After {} recipies".format(first_encounter([3, 2, 3, 0, 8, 1])))
