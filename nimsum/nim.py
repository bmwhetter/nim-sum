import json
from random import randint
import numpy as np


class NimPiles:
    """Class holding the information about a game of Nim
    """
    def __init__(self, piles_string):
        self.piles_dict = json.loads(piles_string) 

    def remove_stones(self, pile, stones):
        # take integers for piles and stones and apply move to dict
        pile_key = 'pile {}'.format(pile)
        self.piles_dict[pile_key] = self.piles_dict[pile_key] - stones

    def stringify_piles(self):
        return json.dumps(self.piles_dict)

    def game_over(self):
        total_stones = 0
        for _, stones in self.piles_dict.items():
            total_stones = total_stones + stones

        if total_stones == 0:
            return True
        else:
            return False  

    def gen_random_move(self):
        # find a pile with nonzero stones and take a random amount of stones
        num_piles = len(self.piles_dict)
        searching_nonzero_pile = True
        while searching_nonzero_pile:
            candidate = randint(1, num_piles)
            pile_key = 'pile {}'.format(candidate)
            stones = self.piles_dict[pile_key]
            if stones > 0:
                searching_nonzero_pile = False
        
        take = randint(1, stones)
        return (candidate, take)

    def nim_sum_zero(self):
        int_list = list(self.piles_dict.values())
        nim_sum = nim_sum_from_list(int_list)
        sum = 0 
        for i in nim_sum:
            sum = sum+i
        return sum == 0

    def gen_optimal_move(self):
        # loop through random moves until one of them gets a nim sum of 0
        # TODO find direct method of constructing the optimal move (sig digit?)
        searching = True
        while searching:
            mirror_game = NimPiles(self.stringify_piles())
            pile, stones = self.gen_random_move()
            mirror_game.remove_stones(pile, stones)
            if mirror_game.nim_sum_zero():
                searching = False
        
        return (pile, stones)


def nim_sum_from_list(int_list):
    # first express each number in reverse binary
    reverse_bin_list = [np.binary_repr(i)[::-1] for i in int_list]
    # find length of longest binary and set up list to hold sum
    nim_length = 0 
    for i in reverse_bin_list:
        l = len(i)
        if l > nim_length:
            nim_length = l
    bin_sum = [0]*nim_length
    # now sum digits
    for i in reverse_bin_list:
        index = 0
        for d in i:
            bin_sum[index] = bin_sum[index] + int(d)
            index = index+1
    # last take sums mod 2
    return [i%2 for i in bin_sum]