from _collections_abc import Sequence


class Word(Sequence):
    def __init__(self, word_as_list: list, commutation_dict: dict[str: list]):
        self.word_as_list = word_as_list
        self.c_map = commutation_dict
        super.__init__()

    def __getitem__(self, item):
        return self.word_as_list[item]

    def __len__(self):
        return len(self.word_as_list)

    def __str__(self):
        return ''.join(str(a) for a in self.word_as_list)

    def get_last_letters(self):
        return self.__get_last_letter_recursive(self.word_as_list)

    def __get_last_letter_recursive(self, w_list):
        if len(w_list) <= 1:
            return set(w_list)

        return self.__get_last_letter_recursive(w_list[:-1]) \
            .intersection(self.c_map[w_list[-1]])          \
            .union(set(w_list[-1]))
