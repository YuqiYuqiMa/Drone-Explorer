# ======================================================================
# FILE:        Main.py
#
# DESCRIPTION: This file contains main function for the board running
#               in the background
#
# CHANGES MADE 04/08: inorder, graph
#
# CHANGES TO BE MADE: take out threading example
# ======================================================================

import Drone
import Policy
import Board
import WriteReport
from time import time


def get_paras():
    """
    This function returns a list of parameters
    :return: a list of parameters
    """
    try:
        f = open("fix_paras.txt", "r")
    except IOError:
        print ("Cannot open fix_paras.txt")
    else:
        paras = f.read().split('\n')
        f.close()
        return paras


if __name__ == "__main__":
    #Parameters.Parameters().run()
    paras = get_paras()
    row = int(paras[0].split()[0])
    col = int(paras[0].split()[1])
    wind_dir = int(paras[-1].split()[0])
    wind_speed = int(paras[-1].split()[1])

    board = Board.board
    policy = Policy.Policy(board, (0, 0), (0, row-1), col, row)
    drone = Drone.Drone(Board.board_info, policy, int(paras[1]), row, col, wind_speed, wind_dir)
    drone.run()
    t = drone.get_time()
    #WriteReport.time_info(t[0], t[1])
    total_events = drone.get_total_events()
    total_caught_events = drone.get_total_caught_event()
    total_caught_events_include_same = drone.get_total_caught_event_include_same()
    WriteReport.stats(total_events, total_caught_events, "catch_rate.txt")
    WriteReport.stats(total_events, total_caught_events_include_same, "catch_rate_include_same.txt")
