# ======================================================================
# FILE:        Arena.py
#
# DESCRIPTION: This file contains Arena class, which contains the map
#              that our agent(UAV) is going to explore
#
# ======================================================================

import time
import math
import random
from Event import Event


class Arena:
    # Tile Structure
    class __Tile:
        start_time = 0
        finish_time = 0
        # buf = 0
        # dur = 0
        lat = 0
        long = 0
        id = 0
        event_list = []
        num_of_events = 0
        time_with_events = 0

    # ===============================================================
    # =                         Constructor
    # ===============================================================

    def __init__(self, my_lat, my_lon, row, col, arrival_rate, arrival_num, prob, expo, die_expo):#, prob, expo):#dur_dis, buf_dis, row, col):
        """Initializes board with 10 x 10 dimensions
        :param my_lat: the initial latitude
        :param my_lon: the initial longitude
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
        # may update other features and parameters later
        #self.__buf_dis = buf_dis
        #self.__dur_dis = dur_dis

        self.__colDimension = col
        self.__rowDimension = row
        self.__board = [[self.__Tile() for j in range(self.__colDimension)] for i in range(self.__rowDimension)]
        self.__addLongLat(my_lat, my_lon)
        self.__addEventTimes()

    # ===============================================================
    # =             Arena Generation Functions
    # ===============================================================

    def __addLongLat(self, lat, lon):
        """
        This method assigns longitude and latitude to the board
        :param lat: the start latitude
        :param lon: the start longitude
        :return: None
        """
        dNorth = 0
        dEast = 0
        earth_radius = 6378137.0  # Radius of "spherical" earth
        self.__board[0][0].lat = lat
        self.__board[0][0].long = lon
        for c in range(1,self.__colDimension):
            dEast += 10
            dLat = dNorth / earth_radius
            dLon = dEast / (earth_radius * math.cos(math.pi * lat / 180))
            self.__board[c][0].lat = lat + (dLat * 180 / math.pi)
            self.__board[c][0].long = lon + (dLon * 180 / math.pi)
        dEast = 0
        for r in range(1,self.__rowDimension):
            dNorth += 10
            for c in range(0,self.__colDimension):
                dLat = dNorth / earth_radius
                dLon = dEast / (earth_radius * math.cos(math.pi * lat / 180))
                self.__board[c][r].lat = lat + (dLat * 180 / math.pi)
                self.__board[c][r].long = lon + (dLon * 180 / math.pi)
                dEast += 10
            dEast = 0

    def __setUpEvent(self):
        """
        initializes events
        :return: None
        """
        for _ in range(self.arrival_num):
            c = random.randint(0,self.__colDimension-1)
            r = random.randint(0,self.__rowDimension-1)
            new_event = Event(self.prob, self.die_expo, self.__colDimension-1, self.__rowDimension-1)
            new_event.update_sector(c, r)
            new_event.update_die_time(time.time())
            new_event.update_next_sector()
            stay_time = self.stay_expo()
            new_event.update_next_move_time(time.time() + stay_time)
            copy = list(self.__board[c][r].event_list)
            copy.append(new_event)
            self.__board[c][r].event_list = copy
            self.__total_events += 1
            self.__board[c][r].num_of_events += 1
            self.__board[c][r].time_with_events += stay_time
            self.__total_dur += stay_time
            self.next_add_event_time = time.time() + self.arrival_rate()

    def __addEventTimes(self):
        """
        This method add event times when the board first crated
        :return: None
        """
        self.__setUpEvent()

    # ===============================================================
    # =             Arena Fetch Functions
    # ===============================================================

    def update_board(self):   # !!!think and discuss about efficiency next time!!!
        """
        This method keeps updating the board with new events
        :return: None
        """
        time_now = time.time()
        for r in range(self.__rowDimension):
            for c in range(self.__colDimension):
                length = len(self.__board[c][r].event_list)
                count = 0
                while count < length:
                    event = self.__board[c][r].event_list[count]
                    if time_now >= event.die_time:  # event are going to die
                        self.__board[c][r].event_list.remove(event)
                        length -= 1
                    else:
                        if time_now > event.finish_time:  # event need to move
                            cur_c = event.next_c
                            cur_r = event.next_r
                            event.update_sector(cur_c, cur_r)
                            event.update_next_sector()
                            stay_time = self.stay_expo()
                            event.update_next_move_time(stay_time)
                            self.__board[c][r].event_list.remove(event)
                            length -= 1
                            self.__board[cur_c][cur_r].event_list.append(event)
                            self.__board[cur_c][cur_r].num_of_events += 1
                            self.__board[cur_c][cur_r].time_with_events += stay_time
                            self.__total_dur += stay_time
                        else:
                            count += 1

        if time_now >= self.next_add_event_time:
            self.__setUpEvent()

    def get_board(self, t):
        """
        This method get and print current board status(information)
        :param t: the current time
        :return: None, but will print this sector has event or not
        """
        for r in range(self.__rowDimension):
            for c in range(self.__colDimension):
                if t > self.__board[c][r].start_time:
                    print(self.__board[c][r].lat, self.__board[c][r].long, "HasEvent", self.__board[c][r].id)
                else:
                    print("NoEvent")

    def get_event(self, c, r):
        """
        This method will return if the list of events
        :param c: the column of the board
        :param r: the row of the board
        :return: True if there's event on the current sector, False otherwise
        """
        return self.__board[c][r].event_list

    def get_id(self, c, r):
        """
        The method gets the current event id
        :param c: the column of the board
        :param r: the row of the board
        :return: the a list of event id from the current sector
        """
        result = []
        for event in self.__board[c][r].event_list:
            result.append(event.id)
        return result

    def get_max_id(self, c, r):
        """
        The method gets the current max id from the current sector
        :param c: the column of the board
        :param r: the row of the board
        :return: the (current) max id of this sector
        """
        return self.__board[c][r].id

    def get_longlat(self):
        """
        :return: one dimension of board, [(0,0),(0,1),(0,2),(2,1),(1,1),(1,0),....]
        """
        result = []
        for r in range(self.__rowDimension):
            if r % 2 == 0:
                for c in range(self.__colDimension):
                    result.append((self.__board[c][r].lat, self.__board[c][r].long, c, r))
            else:
                for c in range(self.__colDimension - 1, -1, -1):
                    result.append((self.__board[c][r].lat, self.__board[c][r].long, c, r))
        return result

        # board_info = Arena(33.24532, 53.12354, time.time())

    def get_average_dur(self):
        """
        This method will calculate the average duration time
        :return: the average duration time
        """
        return self.__total_dur/self.__total_events

    def get_board_info(self):
        """
        This function will return a tuple of information about the board
        :return: a tuple of information about the board
        """
        return self.__colDimension, self.__rowDimension, self.__board, self.get_average_dur()

    def get_total_events(self):
        return self.__total_events