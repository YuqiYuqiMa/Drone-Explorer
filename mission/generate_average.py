import os
from collections import defaultdict

def write_report(root, dest, name):
    '''
    reads the files from a given directory and
    generate the average values of them
    then writes the average values in a direcctory
    located in the main folder (reports)
    '''
    files = os.listdir(root)
    count=[]
    for every in files:
        if every[0] !='.' and every.endswith('report.txt') == False:
            temp = os.path.join(root, every)
            count.append(os.path.join(root, every))
            
    lam_buffer = 0
    lam_dur = 0
    event = 0
    diff = 0
    missed = 0
    val = lambda: defaultdict(int)
    each_sec = defaultdict(val)
    total=0
    num = len(count)
    for each in count:
        gen = open(os.path.join(root, each), 'r').readlines()
        lam_buffer += float(gen[0].split(" ")[-1])
        lam_dur += float(gen[1].split(" ")[-1])
        event += int(gen[2].split(" ")[-1])
        diff += int(gen[3].split(" ")[-1])
        missed += int(gen[4].split(" ")[-1])
        for i in range(9):
            row = gen[6+i].strip()  #.split("\n")[0]
            #print(row)
            ele = row.split("\t")
            #for j in range(10):
            for k in ele:
                j = ele.index(k)
                #k = ele[j]
                if k != '0':
                    for h in k.split(";"):
                        if h != '':
                            t = h.split(",")
                                #if t[0] !='' and t[1] != '':
                            each_sec[(i, j)][int(t[0])] += int(t[1])

        total += int(gen[-1].split(" ")[-1])
    s = 'report_' + name + '.txt'
    link = os.path.join(dest, s)
    open(link, 'a')
    see = open(link, 'w+')
    see.write('Lambda Buffer: ' + str(lam_buffer/num) + '\n')
    see.write('Lambda Duration: ' + str(lam_dur/num)+ '\n')
    see.write('Average num event caught: '+ str(event/num)+ '\n')
    see.write('Average diff num event caught: ' + str(diff/num)+ '\n')
    see.write('Average missed event: '+str(missed/num)+ '\n')
    see.write('Average event for each sector: \n')
    for row in range(10):
        for col in range(10):
            if len(each_sec[(row, col)]) !=0:
                line = ''
                for i, j in each_sec[(row, col)].items():
                    see.write(str(i) + ','+str(j)+';')
                    #line+=str(i)+','+str(j)+';'
            #see.write('{:>12}'.format(line))
            see.write('\t\t')
        see.write('\n')
    see.write('Average sectors visited: ' + str(total/num) + '\n')

            
def generate(root):
    '''
    reads all the sub-folders under the main folder
    and pass them as parameters to function write_report()
    '''
    files = os.listdir(root)
    os.chdir(root)
    os.mkdir('reports')
    count = []
    index=0
    names = []
    for every in files:
        if every[0] !='.':
            names.append(every)
            temp = os.path.join(root, every)
            count.append(os.path.join(root, every))
    dest =temp = os.path.join(root, 'reports')
    for i in count:
        write_report(i, dest, names[index])
        index+=1
                
if __name__ =='__main__':
    generate('/Users/mayuqi/desktop/stats_05_10/roomba')
