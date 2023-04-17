from _collections_abc import Sequence, Iterable


class WordGenerator:
    def __init__(self, commutation_dict: dict[str: list], order_dict: dict[str: int]):
        self.c_map = commutation_dict
        self.o_map = order_dict

    def word(self, word):
        return Word(word, self.c_map, self.o_map)


class Word(Sequence):
    def __init__(self, word, commutation_dict: dict[str: list], order_dict: dict[str: int]):
        if word is list:
            self.word_as_list = word
        elif isinstance(word, Iterable):
            self.word_as_list = list(word)
        else:
            raise TypeError("argument 'word' is not iterable")
        self.c_map = commutation_dict
        self.o_map = order_dict
        self.alphabet = set().union(letter for letter in order_dict)
        #super.__init__()

    def __getitem__(self, item):
        return self.word_as_list[item]

    def __len__(self):
        return len(self.word_as_list)

    def __str__(self):
        return ''.join(str(a) for a in self.word_as_list)

    def __last_letter_recursive(self, w_list) -> set:
        if len(w_list) <= 1:
            return set(w_list)

        return self.__last_letter_recursive(w_list[:-1]) \
            .intersection(self.c_map[w_list[-1]])          \
            .union(set(w_list[-1]))

    def last_letters(self) -> set:
        return self.__last_letter_recursive(self.word_as_list)

    def __neighborhood(self, letter: str) -> set:
        return set(self.c_map[letter])

    def __forbidden_letters_recursive(self, w_list) -> set:
        if len(w_list) == 1:
            return set(
                filter(lambda x: self.o_map[x] < self.o_map[w_list[0]], self.__neighborhood(w_list[0]))
            ).union(set(w_list[0]))

        return self.__forbidden_letters_recursive(w_list[-1])\
            .union(self.__forbidden_letters_recursive(w_list[:-1]))\
            .intersection(self.__neighborhood(w_list[-1]))

    def forbidden_letters(self) -> set:
        return self.__forbidden_letters_recursive(self.word_as_list)

    def legal_next_letters(self) -> set:
        return self.alphabet.copy().difference(self.forbidden_letters())
