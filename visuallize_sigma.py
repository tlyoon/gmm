import numpy as np
import matplotlib.pyplot as plt


fn = 'sigma.csv'
print('fn:',fn)
file1 = open(fn, 'r')
Lines = file1.readlines()
Lines=Lines[2:]
#print(Lines)
count = 0
ygmt={}
yexp={}
wl={}
for line in Lines:
#    print("Line{}: {}".format(count, line.strip()))
   # print(count, line.strip())
    wl[count]=float(line.strip().split()[0])
    Cextgmt=float(line.strip().split()[1])
    Cextexp=float(line.strip().split()[2])
    ygmt[count]=Cextgmt
    yexp[count]=Cextexp
    count += 1
file1.close()
ygmt=[ i for i in ygmt.values() ]
yexp=[ i for i in yexp.values() ]
wl=[ i for i in wl.values() ]


fig = plt.figure()
ax1 = fig.add_subplot(111)

ygmt=[ i for i in ygmt ]
yexp=[ i for i in yexp ]
sigma=np.sqrt(np.sum([ (ygmt[i]-yexp[i])**2 for i in range(len(ygmt))])/len(ygmt))
sigma=round(sigma, 8)
sigma=str(sigma)
ax1.plot(wl[:], ygmt[:], marker="s", label='gmt')
ax1.plot(wl[:],yexp[:],marker="o", label='exp')
plt.legend(loc='upper right');
plt.title('Normalized Cext vs. wavelength (nm).' + "\n" + 'Sigma='+sigma)
plt.savefig('sigma.png')



