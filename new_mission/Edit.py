# ======================================================================
# FILE:        Edit.py
#
# DESCRIPTION: Edit the para.txt
#
# ======================================================================

para = open("fix_paras.txt", "r")
lines = para.readlines()
col_row = lines[0]
para.close()

t = open("time.txt", "r")
time = t.readline()
t.close()

pw = open("fix_paras.txt", "w")
pw.write(col_row)
pw.write("random\n")
pw.write("time\n")
pw.write(time)
pw.close()
