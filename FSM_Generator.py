class FSMGenerator:
    def __init__(self, commutation_dict: dict[str: list], order_dict: dict[str: int]):
        """
        Initialize a Finite State Machine (FSM) Generator Object. Using the defining graph of a right-angled coxeter
        group, necessary short-lex, last-letter, and fiber-product machines can be created.

        :param commutation_dict: A dictionary representation of a defining graph. A letter (key) is associated with a list of letters (value) in the dictionary such that all letters in the list commute with the key
        :param order_dict: A dictionary representation of a total ordering on the letter in the defining graph. A letter (key) is associated with an index (value) that represents that letters relative position in the ordering.
        """
        self.c_map = commutation_dict
        self.o_map = order_dict

    def generate_short_lex_fsm_as_networkx(self):
        pass

    def generate_last_letter_fsm_as_networkx(self):
        pass

    def generate_fiber_product_fsm_as_networkx(self):
        pass

    def generate_short_lex_fsm_as_adj(self):
        pass

    def generate_last_letter_fsm_as_adj(self):
        pass

    def generate_fiber_product_fsm_as_adj(self):
        pass

    def visualize_fsm(self):
        pass
