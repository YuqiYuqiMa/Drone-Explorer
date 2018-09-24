# ======================================================================
# FILE:        Avgtime.py
#
# DESCRIPTION: This file compute tthe average time for roomba
#
# ======================================================================


try:
    f1 = open("time.txt", "r")
except IOError:
    print "Cannot open time.txt"
else:
    ts = f1.readlines()
    f1.close()
    s = 0
    for t in ts:
        if t != "\n" and t != "" and t != " ":
            s += float(t.strip())
    avg = s/len(ts)

    try:
        f2 = open("time.txt", "w")
    except IOError:
        print "Cannot open time.txt"
    else:
        f2.write(str(avg))
        f2.close()
