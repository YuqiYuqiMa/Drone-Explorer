import matplotlib.pyplot as plt
import glob
import re
import numpy as np

path = '/home/hahnara/Documents/School/research/dronekit-python/mission/random/*.txt'
files = glob.glob(path)

xlegend = "Lambda"
plt.figure(1)
plt.title('Random Total Events for Lambda Start')
plt.xlabel(xlegend)
plt.ylabel('Total Events Caught')
x = []  # lambda (start[0], duration[1])
y = []  # number of events (total[2], missed[4], different[3])

for name in files:
    with open(name) as data_file:
            lines = data_file.readlines()
            data_str = lines[2]
            y_val = int(re.search(r'\d+', data_str).group())
            y.append(y_val)

            data_str = lines[0]
            x_val = float(re.search(r'\d+\.\d+', data_str).group())
            x.append(x_val)
print(x, y)
idx = np.argsort(x)
x = np.array(x)[idx]
y = np.array(y)[idx]
plt.plot(x, y)

plt.figure(2)
plt.title('Random # of Diff Events for Lambda Start')
plt.xlabel(xlegend)
plt.ylabel('# of Different Events')
x = []  # lambda (start[0], duration[1])
y = []  # number of events (total[2], missed[4], different[3])

for name in files:
        with open(name) as data_file:
                lines = data_file.readlines()
                data_str = lines[3]
                y_val = int(re.search(r'\d+', data_str).group())
                y.append(y_val)

                data_str = lines[0]
                x_val = float(re.search(r'\d+\.\d+', data_str).group())
                x.append(x_val)

idx = np.argsort(x)
x = np.array(x)[idx]
y = np.array(y)[idx]
plt.plot(x, y)

plt.figure(3)
plt.title('Random # of Missed Events for Lambda Start')
plt.xlabel(xlegend)
plt.ylabel('# of Different Events')
x = []  # lambda (start[0], duration[1])
y = []  # number of events (total[2], missed[4], different[3])

for name in files:
        with open(name) as data_file:
                lines = data_file.readlines()
                data_str = lines[4]
                y_val = int(re.search(r'\d+', data_str).group())
                y.append(y_val)

                data_str = lines[0]
                x_val = float(re.search(r'\d+\.\d+', data_str).group())
                x.append(x_val)

idx = np.argsort(x)
x = np.array(x)[idx]
y = np.array(y)[idx]
plt.plot(x, y)

plt.figure(4)
plt.title('Random Total Events for Lambda Duration')
plt.xlabel(xlegend)
plt.ylabel('Total Events Caught')
x = []  # lambda (start[0], duration[1])
y = []  # number of events (total[2], missed[4], different[3])

for name in files:
        with open(name) as data_file:
                lines = data_file.readlines()
                data_str = lines[2]
                y_val = int(re.search(r'\d+', data_str).group())
                y.append(y_val)

                data_str = lines[1]
                x_val = float(re.search(r'\d+\.\d+', data_str).group())
                x.append(x_val)
print(x, y)
idx = np.argsort(x)
x = np.array(x)[idx]
y = np.array(y)[idx]
plt.plot(x, y)

plt.figure(5)
plt.title('Random # of Diff Events for Lambda Duration')
plt.xlabel(xlegend)
plt.ylabel('# of Different Events')
x = []  # lambda (start[0], duration[1])
y = []  # number of events (total[2], missed[4], different[3])

for name in files:
        with open(name) as data_file:
                lines = data_file.readlines()
                data_str = lines[3]
                y_val = int(re.search(r'\d+', data_str).group())
                y.append(y_val)

                data_str = lines[1]
                x_val = float(re.search(r'\d+\.\d+', data_str).group())
                x.append(x_val)

idx = np.argsort(x)
x = np.array(x)[idx]
y = np.array(y)[idx]
plt.plot(x, y)

plt.figure(6)
plt.title('Random # of Missed Events for Lambda Duration')
plt.xlabel(xlegend)
plt.ylabel('# of Different Events')
x = []  # lambda (start[0], duration[1])
y = []  # number of events (total[2], missed[4], different[3])

for name in files:
        with open(name) as data_file:
                lines = data_file.readlines()
                data_str = lines[4]
                y_val = int(re.search(r'\d+', data_str).group())
                y.append(y_val)

                data_str = lines[1]
                x_val = float(re.search(r'\d+\.\d+', data_str).group())
                x.append(x_val)

idx = np.argsort(x)
x = np.array(x)[idx]
y = np.array(y)[idx]
plt.plot(x, y)
plt.show()