# ======================================================================
# FILE:        Parameters.py
#
# DESCRIPTION: get parameters from user
#
# ======================================================================


class Parameters:
    def __init__(self):
        self.row = ""
        self.col = ""
        self.rule = ""
        self.buf = []
        self.dur = []
        self.policy = ""
        self.end = ""
        self.rd = ""

    def get_input(self):
        """
        This method get all the input from the user
        """
        self.row = raw_input("Board row dimension: ")
        while not _check_int(self.row):
            print "Please enter valid number"
            self.row = raw_input("Board row dimension: ")

        self.col = raw_input("Board col dimension: ")
        while not _check_int(self.col):
            print "Please enter valid number"
            self.col = raw_input("Board col dimension: ")

        self.rule = raw_input("Distribution to generate events (random/expo): ")
        while self.rule != "random" and self.rule != "expo":
            print "Please enter valid distribution"
            self.rule = raw_input("Distribution to generate events (random/expo): ")

        buffer = raw_input("List of distribution coefficients for event buffer time for testing: ")
        self.buf = buffer.split()
        while not _check_list_digit(self.buf):
            print "Please enter valid list of coefficients"
            buffer = raw_input("List of distribution coefficients for event buffer time for testing: ")
            self.buf = buffer.split()

        duration = raw_input("List of distribution coefficients for event duration time for testing: ")
        self.dur = duration.split()
        while not _check_list_digit(self.dur) or len(self.dur) != len(self.buf):
            print "Please enter valid list of coefficients and make sure it has the same quantity of coefficients as buffer"
            duration = raw_input("List of distribution coefficients for event duration time for testing: ")
            self.dur = duration.split()

        self.policy = raw_input("How you'd like to fly the drone? (random/roomba): ")
        while self.policy != "roomba" and self.policy != "random":
            print "Please enter valid policy"
            self.policy = raw_input("How you'd like to fly the drone? (random/roomba): ")

        self.end = raw_input("How you'd like to determine when to stop the drone? certain (time/movement): ")
        while self.end != "time" and self.end != "movement":
            print "Please enter valid ending"
            self.end = raw_input("How you'd like to determine when to stop the drone? certain (time/movement): ")

        self.rd = raw_input("How many rounds would you like to stop the drone? \n (time:seconds/movement:steps(int)): ")
        if self.end == "movement":
            while not _check_int(self.rd):
                print "Please enter valid integer for movement"
                self.rd = raw_input("How many rounds would you like to stop the drone? \n (time:seconds/movement:steps(int)): ")
        else:
            while not self.rd.isdigit():
                print "Please enter valid integer for movement"
                self.rd = raw_input("How many rounds would you like to stop the drone? \n (time:seconds/movement:steps(int)): ")

    def run(self):
        """
        This function writes all the parameters to two files, and the order is:
        paras.txt:
            row col
            rule
            policy
            end
            round
        lambdas.txt:
            buf/dur pairs
        """
        self.get_input()
        f = open("paras.txt", "w+")
        f.write(self.row + " " + self.col + "\n")
        f.write(self.rule + "\n")
        f.write(self.policy + "\n")
        f.write(self.end + "\n")
        f.write(self.rd)
        f.close()

        f = open("lambdas.txt", "w+")
        f.write(self._get_lambda_pairs())
        f.close()

    def _get_lambda_pairs(self):
        result = ""
        for x, y in zip(self.dur, self.buf):
            result += y + " " + x + "\n"
        return result


def _check_int(i):
    """
    This function checks the input string is an integer or not
    :param i: the input string to be checked
    :return: true if i is an integer, false otherwise
    """
    try:
        int(i)
        return True
    except ValueError:
        return False


def _check_float(i):
    """
    This function checks the input string is a float number or not
    :param i: the input string to be checked
    :return: true if i is a float number, false otherwise
    """
    try:
        float(i)
    except ValueError:
        return False
    return True


def _check_list_digit(l):
    """
    This function ensures the items in the list are all digits
    :param l: the list to be checked
    :return: true when items are all digits, false when there's one item is not digit
    """
    for item in l:
        if not _check_float(item):
            return False
    return True


Parameters().run()