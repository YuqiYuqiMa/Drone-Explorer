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


class Arena():
    # Tile Structure
    class __Tile:
        start_time = 0
        finish_time = 0
        buf = 0
        dur = 0
        lat = 0
        long = 0
        id = 0

    # ===============================================================
    # =                         Constructor
    # ===============================================================

    def __init__(self, my_lat, my_lon, my_time, dur_dis, buf_dis, row, col):
        """Initializes board with 10 x 10 dimensions
        :param my_lat: the initial latitude
        :param my_lon: the initial longtitude
        :param my_time: current time
        :param buf_dis: buffer time beween events
        :param dur_dis: duration time of events
        """
        self.__getsEvent = False
        self.__agentX = 0
        self.__agentY = 0
        self.__agentdir = 0
        self.__eventqueue = []
        self.__total_events = 0
        self.__total_buf = 0
        self.__total_dur = 0
        # may update other features and parameters later
        self.__buf_dis = buf_dis
        self.__dur_dis = dur_dis

        self.__colDimension = col
        self.__rowDimension = row
        self.__time = my_time
        self.__board = [[self.__Tile() for j in range(self.__colDimension)] for i in range(self.__rowDimension)]
        self.__addLongLat(my_lat, my_lon)
        self.__addEventTimes()

    # ===============================================================
    # =             Arena Generation Functions
    # ===============================================================
    def __addEventTimes(self):
        """
        This method add event times when the board first crated
        :return: None
        """
        for r in range(self.__rowDimension):
            for c in range(self.__colDimension):
                buf_time = self.__buf_dis()
                self.__board[c][r].start_time = self.__time + buf_time
                self.__board[c][r].id += 1
                self.__total_events += 1
                self.__total_buf += buf_time
                self.__board[c][r].buf += buf_time
                dur_time = self.__dur_dis()
                self.__board[c][r].finish_time = self.__board[c][r].start_time + dur_time
                self.__total_dur += dur_time
                self.__board[c][r].dur += dur_time

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

    # ===============================================================
    # =             Arena Fetch Functions
    # ===============================================================
    def update_board(self):
        """
        This method keeps updating the board with new events
        :return: None
        """
        time_now = time.time()
        for r in range(self.__rowDimension):
            for c in range(self.__colDimension):
                if time_now > self.__board[c][r].finish_time:
                    buf_time = self.__buf_dis()
                    self.__board[c][r].start_time = self.__board[c][r].finish_time +buf_time
                    self.__board[c][r].id += 1
                    self.__total_buf += buf_time
                    self.__board[c][r].buf += buf_time
                    dur_time = self.__dur_dis()
                    self.__board[c][r].finish_time = self.__board[c][r].start_time + dur_time
                    self.__total_dur += dur_time
                    self.__board[c][r].dur += dur_time

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

    def get_event(self, c, r, t):
        """
        This method will return if the sector has event or not
        :param c: the column of the board
        :param r: the row of the board
        :param t: the current time
        :return: True if this sector at this time has event; false otherwise
        """
        if t > self.__board[c][r].start_time:
            return True
        return False

    def get_id(self, c, r, t):
        """
        The method gets the current event id
        :param c: the column of the board
        :param r: the row of the board
        :param t: the current time
        :return: the event id of current event; 0 if no event this time
        """
        if t > self.__board[c][r].start_time:
            return self.__board[c][r].id
        return 0

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

    def get_average_buf(self):
        """
        This method will calculate the average buffer time
        :return: the average buffer time
        """
        return self.__total_buf/self.__total_events

    def get_average_dur(self):
        """
        This method will calculate the average dutation time
        :return: the average duration time
        """
        return self.__total_dur/self.__total_events

    def get_board_info(self):
        """
        This function will return a tuple of information about the board
        :return: a tuple of information about the board
        """
        return self.__colDimension, self.__rowDimension, self.__board, self.get_average_buf(), self.get_average_dur()
