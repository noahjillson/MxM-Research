c_map = {'a': {'b', 'e'}, 'b': {'a', 'c'}, 'c': {'b', 'd'}, 'd': {'c', 'e'}, 'e': {'d', 'a'}}
o_map = {'a': 0, 'c': 1, 'b': 2, 'd': 3, 'e': 4}

check = "acbc" 

"""
Algorithm: 

Start with the word. Automatically append the last leter to LL
    Now check the word - 1 for the adjacent letters to the last letter in the previous iteration
"""

def last_letters_recursion(w):
    if len(w) == 1:
        return set(w)
    return last_letters_recursion(w[0:-1]) \
                .intersection(c_map[w[-1]]) \
                .union(set(w[-1]))

print(last_letters_recursion(check))