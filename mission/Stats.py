# ======================================================================
# FILE:        Stats.py
#
# DESCRIPTION: This file compute and analyze the result that drone
#              collected
#
# ======================================================================


from time import gmtime, strftime, time
import Board


def board_stats(info, delimiter=","):
    """
    write a report about the original board
    :param info: the information returned by the board
    :param delimiter: the delimiter of the data. Comma by default
    """
    GLO = time()
    file_name = "Board_" + str(GLO) + ".csv"
    col = info[0]
    row = info[1]
    board = info[2]
    total_buf_avg = info[3]
    total_dur_avg = info[4]

    report = open(file_name, "w")
    report.write("dim_column,dim_row,buffer_seconds,duration_seconds,buffer_lambda,duration_lambda\n")
    report.write(str(col) + delimiter +
                 str(row) + delimiter +
                 str(cal_second(float(Board.lambdas[0]))) + delimiter +
                 str(cal_second(float(Board.lambdas[1]))) + delimiter +
                 Board.lambdas[0] + delimiter +
                 Board.lambdas[1] + "\n")

    report.write("column,row,max_id,"
                 "average_buffer_time,average_duration_time,"
                 "total_board_avg_buf,total_board_avg_dur\n")
    for r in range(row):
        for c in range(col):
            report.write(str(c) + delimiter +
                         str(r) + delimiter +
                         str(board[c][r].id) + delimiter +
                         str(board[c][r].buf/board[c][r].id) + delimiter +
                         str(board[c][r].dur/board[c][r].id) + delimiter +
                         str(total_buf_avg) + delimiter +
                         str(total_dur_avg) + "\n")

    report.close()


def drone_stats(info, delimiter=","):
    """
    write a report about the real time information that drone collects
    :param info: the information catched by drone
    :param delimiter: the delimiter of the data. Comma by default
    """
    GLO = time()
    file_name = "Drone_RealTime_" + str(GLO) + ".csv"
    total_events = info[0]
    count_different = info[1]
    missed_events = info[2]
    total_missed_events = info[3]
    rowDim = info[4]
    colDim = info[5]
    times_hasEvent = info[6]
    total_visit = info[7]
    round = info[8]
    speed = info[9]
    random = 1 if info[10] == "random" else 0
    lam_Buf = Board.lambdas[0]
    lam_Dur = Board.lambdas[1]
    report = open(file_name, "w+")
    hyper_params = "dim_col,dim_row,round,drone_speed,sec_Buf,sec_Dur,lam_Buf,lam_Dur,random\n"
    report.write(hyper_params)
    hyper_params_vals = (str(colDim) + delimiter + str(rowDim) + delimiter + str(round) + delimiter + str(speed)
                         + delimiter + str(cal_second(lam_Buf)) + delimiter + str(cal_second(lam_Dur)) + delimiter
                         + str(lam_Buf) + delimiter + str(lam_Dur) + delimiter + str(random) + "\n")
    report.write(hyper_params_vals)
    coordinates = "col,row,time,event_id,mssd_evnts\n"
    report.write(coordinates)
    for row in range(rowDim):
        for col in range(colDim):
            msd = "0"
            if (col, row) in missed_events:
                msd = str(missed_events[(col, row)])
            if (col, row) in times_hasEvent.keys():
                for id in times_hasEvent[(col, row)].keys():
                    for t in times_hasEvent[(col, row)][id]:
                        line = (str(col) + delimiter + str(row) + delimiter + str(t) + delimiter + str(id) + delimiter
                                + msd + "\n")
                        report.write(line)
            else:
                coor = (str(col) + delimiter + str(row) + delimiter + "0" + delimiter + "0" + delimiter
                       + msd + delimiter + "\n")
                report.write(coor)
    report.close()


def drone_total_stats(info, delimiter=","):
    """
    write a report about the real time information that drone collects
    :param info: the information catched by drone
    :param delimiter: the delimiter of the data. Comma by default
    """
    GLO = time()
    file_name = "Drone_Total_" + str(GLO) + ".csv"
    total_events = info[0]
    count_different = info[1]
    total_missed_events = info[3]
    rowDim = info[4]
    colDim = info[5]
    total_visit = info[7]
    round = info[8]
    speed = info[9]
    count = info[10]
    random = 1 if info[10] == "random" else 0
    lam_Buf = Board.lambdas[0]
    lam_Dur = Board.lambdas[1]
    report = open(file_name, "w+")
    hyper_params = "dim_col,dim_row,round,drone_speed,sec_Buf,sec_Dur,lam_Buf,lam_Dur,random\n"
    report.write(hyper_params)
    hyper_params_vals = (str(colDim) + delimiter + str(rowDim) + delimiter + str(round) + delimiter + str(speed)
                         + delimiter + str(cal_second(lam_Buf)) + delimiter + str(cal_second(lam_Dur)) + delimiter
                         + str(lam_Buf) + delimiter + str(lam_Dur) + delimiter + str(random) + "\n")
    report.write(hyper_params_vals)
    coordinates = "ttl_evnts,ttl_diff_evnts,ttl_mssd_evnts,ttl_vistd_sctrs,ttl_evnt_generate\n"
    report.write(coordinates)
    line = (str(total_events) + delimiter + str(count_different) + delimiter
            + str(total_missed_events) + delimiter + str(total_visit) + delimiter + str(count) + "\n")
    report.write(line)
    report.close()


def time_info(t1, t2, delimiter=","):
    """
    This function will write the time result for each experiment
    :param t1: the starting time
    :param t2: the finishing time
    :param delimiter: the delimiter of the data. Comma by default
    """
    file_name = "time.txt"
    report = open(file_name, 'a')
    report.write("\n" + str(t2-t1) + "\n")
    report.close()


def cal_second(lam):
    """
    This function will transfer lambda into seconds
    :param lam: the lambda, type:float
    :return: the transferred seconds
    """
    return 1/float(lam)
