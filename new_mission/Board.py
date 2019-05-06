# ======================================================================
# FILE:        Board.py
#
# DESCRIPTION: Combine prev Board and Arena
#
# ======================================================================

import Distribution
from Event import Event
import random

glb_time = 1734927


class Board:
    class __Tile:
        start_time = 0
        finish_time = 0
        id = 0
        event_list = []
        num_of_events = 0
        time_with_events = 0

        # ===============================================================
        # =                         Constructor
        # ===============================================================

    def __init__(self, row, col, arrival_rate, arrival_num, prob, expo,
                 die_expo):  # , prob, expo):#dur_dis, buf_dis, row, col):
        """Initializes board with 10 x 10 dimensions
        :param arrival_rate: The expo distribution of the interval times a new event will come into the sector
        :param arrival_num: The number of events that will arrive into the board after some time
        :param prob: The probability that the event will stay in the same quadrant
        :param expo: The expo distribution of the event about the time it will stay in one sector
        :param die_expo: The expo distribution of the event about its lifetime
        """
        self.__getsEvent = False
        self.__agentX = 0
        self.__agentY = 0
        self.__agentdir = 0
        self.__eventqueue = []
        self.__total_events = 0
        self.__total_dur = 0
        self.arrival_rate = arrival_rate
        self.arrival_num = arrival_num
        self.prob = prob
        self.stay_expo = expo
        self.die_expo = die_expo
        self.next_add_event_time = 0

        self.__colDimension = col
        self.__rowDimension = row
        self.__board = [[self.__Tile() for j in range(self.__colDimension)] for i in range(self.__rowDimension)]
        self.__setUpEvent()

        # ===============================================================
        # =             Arena Generation Functions
        # ===============================================================

    def __setUpEvent(self):
        """
        initializes events
        :return: None
        """
        for _ in range(self.arrival_num):
            c = random.randint(0, self.__colDimension - 1)
            r = random.randint(0, self.__rowDimension - 1)
            new_event = Event(self.prob, self.die_expo, self.__colDimension - 1, self.__rowDimension - 1)
            new_event.update_sector(c, r)
            new_event.update_die_time(glb_time)
            new_event.update_next_sector()
            stay_time = self.stay_expo()
            new_event.update_next_move_time(glb_time + stay_time)
            copy = list(self.__board[c][r].event_list)
            copy.append(new_event)
            self.__board[c][r].event_list = copy
            self.__total_events += 1
            self.__board[c][r].num_of_events += 1
            self.__board[c][r].time_with_events += stay_time
            self.__total_dur += stay_time
            self.next_add_event_time = glb_time + self.arrival_rate()

    def get_board(self):
        """
        :return: one dimension of board, [(0,0),(0,1),(0,2),(1,2),(1,1),(1,0),....]
        """
        result = []
        for r in range(self.__rowDimension):
            if r % 2 == 0:
                for c in range(self.__colDimension):
                    result.append((c, r))
            else:
                for c in range(self.__colDimension - 1, -1, -1):
                    result.append((c, r))
        return result

    def get_stay_expo(self):
        return self.stay_expo

    def get_next_add_event_time(self):
        return self.next_add_event_time

    def get_arrival_num(self):
        return self.arrival_num

    def get_prob(self):
        return self.prob

    def get_die_expo(self):
        return self.die_expo

    def get_total_events(self):
        return self.__total_events

    def get_arrival_rate(self):
        return self.arrival_rate

    def get_real_board(self):
        return self.__board



try:
    f1 = open("fix_paras.txt", "r")
    f2 = open("boardinput.txt", "r")
except IOError:
    print ("Cannot open")
else:
    paras = f1.read().split('\n')
    indep_var = f2.read().split('\n')[0].split()
    f1.close()
    f2.close()

    row = int(paras[0].split()[0])
    col = int(paras[0].split()[1])

    prob = float(indep_var[0])
    dur_dist = Distribution.Distribution(float(indep_var[1]))
    arrival_rate = Distribution.Distribution(float(indep_var[2])) #expo
    arrival_num = int(indep_var[-2])
    die_rate = Distribution.Distribution(float(indep_var[-1])) #expo
    board_info = Board(row, col, arrival_rate.exponential, arrival_num,
                             prob, dur_dist.exponential, die_rate.exponential)
    board = board_info.get_board()
