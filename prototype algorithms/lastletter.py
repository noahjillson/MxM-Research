c_map = {'a': {'b', 'e'}, 'b': {'a', 'c'}, 'c': {'b', 'd'}, 'd': {'c', 'e'}, 'e': {'d', 'a'}}
o_map = {'a': 0, 'c': 1, 'b': 2, 'd': 3, 'e': 4}

check = "acbd" 

"""
Algorithm: 

Start with a word W in shortlex.
If the last letter of w (W without the written last letter) can be something that commutes with 
the last written letter of W, then it can be a last letter. 
Last letter checks for this and also notes that the written last letter of W can also be a last letter.
"""

def last_letters_recursion(w):
    if len(w) == 1:
        return set(w)
    return last_letters_recursion(w[0:-1])      \
                .intersection(c_map[w[-1]])     \
                .add(w[-1])

print(last_letters_recursion(check))