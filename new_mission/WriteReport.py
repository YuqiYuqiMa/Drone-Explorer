from __future__ import division
import sys


def generate_and_empty_average_file(filename):
    record = open(filename, "r")
    total = 0
    counter = 0
    for line in record.readlines():
        if line != "":
            total += float(line)
            counter += 1
    record.close()
    record2 = open(filename, "w")
    record2.close()
    return total / counter


def get_from_fix():
    try:
        f = open("fix_paras.txt", "r")
    except IOError:
        print ("Cannot open fix_paras.txt")
    else:
        paras = f.read().split('\n')
        f.close()
        row = paras[0].split()[0]
        col = paras[0].split()[1]
        return row, col


def time_info(t1, t2):
    """
    This function will write the time result for each experiment
    :param t1: the starting time
    :param t2: the finishing time
    """
    file_name = "time.txt"
    report = open(file_name, 'a')
    report.write("\n" + str(t2-t1) + "\n")
    report.close()


def generate_prob_file(prob,dur_lambda,arr_l,arr_num,die_l,var,random,row,col,catch_rate1,catch_rate2,delimiter=","):
    """
    write a report about the original board
    :param info: the information returned needed
    :param delimiter: the delimiter of the data. Comma by default
    """

    file_name = var + "_var.csv"

    report = open(file_name, "a")
    # report.write("dim_column,dim_row,duration_lambda,probability,"
    #              "arrival_lambda,eventlife_lambda,arrival_num,"
    #              "catch_rate,catch_rate_include_same,random\n")
    report.write(str(col) + delimiter +
                 str(row) + delimiter +
                 str(dur_lambda) + delimiter +
                 str(prob) + delimiter +
                 str(arr_l) + delimiter +
                 str(die_l) + delimiter +
                 str(arr_num) + delimiter +
                 str(catch_rate1) + delimiter +
                 str(catch_rate2) + delimiter +
                 str(random) + "\n")

    report.close()


def stats(total_events, total_caught_events,filename):
    report = open(filename, "a")
    rate = float(total_caught_events/total_events)
    report.write(str(float(rate)) + '\n')
    report.close()


if __name__ == "__main__":
    try:
        prob = sys.argv[1]
        dur_lambda = sys.argv[2]
        arr_l = sys.argv[3]
        arr_num = sys.argv[4]
        die_l = sys.argv[5]
        var = sys.argv[-2]
        random = sys.argv[-1]
        row, col = get_from_fix()
        catch_rate1 = generate_and_empty_average_file("catch_rate.txt")
        catch_rate2 = generate_and_empty_average_file("catch_rate_include_same.txt")

        generate_prob_file(prob, dur_lambda, arr_l, arr_num, die_l,var, random, row, col, catch_rate1,catch_rate2)

    except IndexError:
        print ("Some error")
