import lastletter


def fsm():
    E = set()
    V = set()

    letters = {'a', 'b', 'c', 'd', 'e'}
    for l in letters:
        adjacent_letters = c_map[l]
        intermediary_letters = []
        for al in adjacent_letters:
            intermediary_letters.extend(c_map[al].copy().difference(set(l)))
            print(l + " -" + al + "-> " + al+l)
        for il in intermediary_letters:
            print(l + " -" + il + "-> " + il+l)
            for x in c_map[il].copy().intersection(c_map[l]):
                print(l + il + " -" + x + "-> " + x+l)


c_map = {'a': {'b', 'e'}, 'b': {'a', 'c'}, 'c': {'b', 'd'}, 'd': {'e', 'c'}, 'e': {'a', 'd'}, '': {'a', 'b', 'c', 'd', 'e'}}
fsm()
