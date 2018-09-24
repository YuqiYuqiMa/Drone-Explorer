# ======================================================================
# FILE:        Policy.py
#
# DESCRIPTION: Contains policies drone will fly including: random, roomba
#
# ======================================================================

from random import randrange, random
from dronekit import connect, VehicleMode, LocationGlobalRelative
from collections import defaultdict


class Policy():
    def __init__(self, board, start, end, col_dim, row_dim):
        self.board = board
        self.start = start
        self.end = end
        self.cur = (0, 0)
        self.switch = 0
        self.__colDimension = col_dim
        self.__rowDimension = row_dim
        self.cord_map = change_to_map(board,row_dim * col_dim)

    def random(self):
        """
        This method provides drone to fly randomly
        :reutrn: the tuple of col, row, and wpl
        """
        l = self._check_neighbor()
        i = l[randrange(0,len(l))]
        lat = self.board[i][0]
        lon = self.board[i][1]
        c = self.board[i][2]
        r = self.board[i][3]
        self.cur = (c,r)
        wpl = LocationGlobalRelative(lat, lon, 10)
        return (c, r, wpl)

    def roomba(self):
        """
        This method provides drone to fly inorder
        :return: the tuple of col, row, and wpl
        """
        temp = (0, 0, 0)
        if self.start[0] == self.end[0]:
            temp = self._horizontal()
        elif self.start[1] == self.end[1]:
            temp = self._vertical()
        if self.switch == 1:
            self.switch = 0
            return self._horizontal()
        elif self.switch == 2:
            self.switch = 0
            return self._vertical()
        return temp

    def _find_dir(self, a, b):
        if (a < b):
            return 1
        else:
            return -1

    def _horizontal(self):
        """
        returns lat & long
        if at the end: go to vertical (start a new cycle)
        if at the end of some row: turn to the next upper/lower row (depends on dir)
        if at row 0, 2: ------->
        if at row 1, 3: <-------
        """
        c = self.cur[0]
        r = self.cur[1]
        print(c, r)
        d = self._find_dir(self.start[1], self.end[1])
        if c == self.end[0] and r == self.end[1]:
            self.start = (self.end[0], self.end[1])
            self.end = (self.__colDimension - 1 - self.start[0], self.end[1])
            self.switch = 2
            return
        if (r % 2 == 0 and c == self.__colDimension - 1) or (r % 2 == 1 and c == 0):
            self.cur = (c, r + d)
            return self.__getboardinfo__(c, r + d)
        if r % 2 == 1:
            self.cur = (c - 1, r)
            return self.__getboardinfo__(c - 1, r)
        if r % 2 == 0:
            self.cur = (c + 1, r)
            return self.__getboardinfo__(c + 1, r)
        else:
            print("nothing\n")

    def _vertical(self):
        """
        returns lat & long
        if at the end: go to horizontal (start a new cycle)
        if at the end of some col: turn to the next left/right col (depends on dir)
        if at col 0, 2: go down
        if at col 1, 3: go up
        """
        c = self.cur[0]
        r = self.cur[1]
        d = self._find_dir(self.start[0], self.end[0])
        if c == self.end[0] and r == self.end[1]:
            self.start = (self.end[0], self.end[1])
            self.end = (self.end[0], self.__rowDimension - 1 - self.start[1])
            self.switch = 1
            return
        if (c % 2 == 1 and r == self.__rowDimension - 1) or (c % 2 == 0 and r == 0):
            self.cur = (c + d, r)
            return self.__getboardinfo__(c + d, r)
        if c % 2 == 0:
            self.cur = (c, r - 1)
            return self.__getboardinfo__(c, r - 1)
        if c % 2 == 1:
            self.cur = (c, r + 1)
            return self.__getboardinfo__(c, r + 1)
        else:
            print("nothing")

    def _check_neighbor(self):
        """
        This function checks and return all the neighbors
        :return: list of the valid neighbors(index) that the current position has
        """
        result = []
        c = self.cur[0]
        r = self.cur[1]
        cords = set(self.cord_map.keys())
        up = (c,r+1)
        down = (c, r-1)
        left = (c-1, r)
        right = (c+1, r)
        if up in cords:
            result.append(self.cord_map[up])
        if down in cords:
            result.append(self.cord_map[down])
        if left in cords:
            result.append(self.cord_map[left])
        if right in cords:
            result.append(self.cord_map[right])
        return result


    def __getboardinfo__(self, c, r):
        """
        For returning the wpl, we need to get information of the longtitude and latitude,
        so we need to return the board(sector) information
        :param c: the coloum of the board; r: the row of the board
        :return: the longtitude and latitude of the sector
        """
        for elem in self.board:
            if elem[2] == c and elem[3] == r:
                lat = elem[0]
                lon = elem[1]
                wpl = LocationGlobalRelative(lat, lon, 2)
                return c, r, wpl


def change_to_coordinate(index):
    """
    Given the index i, returns its corresponding coordinates
    :param index: the index of the list
    :return: the related coordinates
    """
    x = index / 10
    if x % 2 == 0:
        y = index % 10
    else:
        y = 9 - index % 10
        return (int(x),int(y))


def change_to_map(board,l):
    """
    Given the board, return a dictionary
    :param board: the board to be transferred
    :return: the dictionary, key: (c,r), val: index
    """
    result = defaultdict(int)
    for i in range(l):
        c = board[i][2]
        r = board[i][3]
        result[(c,r)] = i
    return result
