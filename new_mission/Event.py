# ======================================================================
# FILE:        Event.py
#
# DESCRIPTION: This file contains Event class, which will represent each
#               Event in the map
#
# ======================================================================

import Distribution
from collections import defaultdict
import random


class Event:
    event_id = 1

    def __init__(self, prob, lifetime, col, row):
        """
        The class has two parameters
        :param prob: The probability the the event will move
        :param lifetime: The exponential distribution of the life time of the event
        :param expo: The duration that the event will stay in the same place(sector)
        :param col: The column dimension of the map
        :param row: The row dimension of the map
        """
        self.col_dim = col
        self.row_dim = row
        self.probability = prob
        self.life_time_expo = lifetime
        self.die_time = 0
        self.finish_time = 0
        self.id = Event.event_id
        Event.event_id += 1
        self.travel_history = defaultdict(int)
        self.cur_c = -1
        self.cur_r = -1
        self.next_c = -1
        self.next_r = -1

    def update_sector(self, c, r):
        """
        This function updates the travel history of this event
        :param c: col coordinate
        :param r: row coordinate
        :return:
        """
        self.cur_c = c
        self.cur_r = r
        self.travel_history[(c, r)] += 1

    def update_next_sector(self):
        numbers = [i for i in range(1000)]
        stay = numbers[:int(self.probability*1000)]
        i = random.randint(0, 999)
        if i in stay:
            self.next_c, self.next_r = self.cur_c, self.cur_r
        else:
            goto_next = next_sector(self.cur_c, self.cur_r, self.col_dim, self.row_dim)
            self.next_c, self.next_r = goto_next[0], goto_next[1]

    def update_die_time(self, cur_time):
        """
        This function will update the death time as soon as an event set up
        :param cur_time: the current time
        :return:
        """
        self.die_time = cur_time + self.life_time_expo()

    def update_next_move_time(self, dur_time):
        """
        This function will update the next move time of the event
        :param dur_time: The duration time of the event
        :return:
        """
        self.finish_time += dur_time

    def get_id(self):
        return self.id


def next_sector(c, r, col_dim, row_dim):
    """
    This function will tell you which quadrant the sector is
    :param c: current column
    :param r: current row
    :param col_dim: Col num in the board
    :param row_dim: Row num in the board
    :return: The quadrant
    """
    left = (c - 1, r)
    right = (c + 1, r)
    up = (c, r + 1)
    down = (c, r - 1)

    if c == 0 and r == 0:
        available = [up, right]
        return available[random.randint(0,1)]
    elif c == 0 and r == row_dim:
        available = [down, right]
        return available[random.randint(0,1)]
    elif c == col_dim and r == 0:
        available = [left, up]
        return available[random.randint(0,1)]
    elif c == col_dim and r == row_dim:
        available = [left, down]
        return available[random.randint(0,1)]
    elif c == 0:
        available = [up, down, right]
        return available[random.randint(0,2)]
    elif c == col_dim:
        available = [left, up, down]
        return available[random.randint(0,2)]
    elif r == 0:
        available = [left, right, up]
        return available[random.randint(0,2)]
    elif r == row_dim:
        available = [left, right, down]
        return available[random.randint(0,2)]
    else:
        available = [left, right, up, down]
        return available[random.randint(0,3)]