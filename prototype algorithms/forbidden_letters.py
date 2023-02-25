from typing import List

def neighborhood(p: int) -> set[str]:
    """Return the 1.5 radius neighborhood around point p (just p and all its adjacent vertices)"""
    nbhd = set(torus_c_map[p])
    # nbhd.append(p)
    return nbhd

def forbidden_letters(w: str) -> set[str]:
    """
    Find the forbidden letters for a word w.s

    Params:
    :w str: The input word.
    :return: The list of forbidden letters that can follow w.
    """

    if len(w) == 1:
        # If the word length is 1, then the last letters are just the adjacent letters than come before that letter
        return set(filter(lambda x: torus_o_map[x] <= torus_o_map[w], neighborhood(w)))
    else:
        # F(wl) = F(l) union (F(w) intersection N_l)
        return forbidden_letters(w[-1]).union(forbidden_letters(w[:-1]).intersection(neighborhood(w[-1])))
    
def name_to_char(letter: str) -> str:
    if letter[0] == 'a':
        return chr(96 + int(letter[1]))
    elif letter[0] == 'b':
        return chr(64 + int(letter[0]))
    else:
        return str(int(letter(0)))

torus_o_map = {
                'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6,
                'A': 7, 'B': 8, 'C': 9, 'D': 10, 'E': 11, 'F': 12, 'G': 13,
                '1': 14, '2': 15, '3': 16, '4': 17, '5': 18, '6': 19, '7': 20
}

torus_c_map = {
                'a': {'b', 'g', 'D', 'E', '4', '5'}, 'b': {'a', 'c', 'E', 'F', '5', '6'},
                'c': {'b', 'd', 'F', 'G', '6', '7'}, 'd': {'c', 'e', 'A', 'G', '1', '7'}, 
                'e': {'d', 'f', 'A', 'B', '1', '2'}, 'f': {'e', 'g', 'B', 'C', '2', '3'},  
                'g': {'a', 'f', 'C', 'D', '3', '4'},  
                'A': {'d', 'e', 'B', 'G', '4', '5'}, 'B': {'e', 'f', 'A', 'C', '5', '6'},
                'C': {'f', 'g', 'B', 'D', '6', '7'}, 'D': {'a', 'g', 'C', 'E', '1', '7'},
                'E': {'a', 'b', 'D', 'F', '1', '2'}, 'F': {'b', 'c', 'E', 'G', '2', '3'},  
                'G': {'c', 'd', 'A', 'F', '3', '4'},  
                '1': {'d', 'e', 'D', 'E', '2', '7'}, '2': {'e', 'f', 'E', 'F', '1', '3'},
                '3': {'f', 'g', 'F', 'G', '2', '4'}, '4': {'a', 'g', 'A', 'G', '3', '5'},
                '5': {'a', 'b', 'A', 'B', '4', '6'}, '6': {'b', 'c', 'B', 'C', '5', '7'},  
                '7': {'c', 'd', 'C', 'D', '1', '6'}
}

test_word = '7E' #B5 A6

print(forbidden_letters(test_word).union(test_word[-1])) # union the last letter