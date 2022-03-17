import numpy as np
import matplotlib.pyplot as plt

##### treat gmt ##############
fn = 'gmt.dat'
print('fn:',fn)
file1 = open(fn, 'r')
Lines = file1.readlines()
Lines=Lines[2:]
#print(Lines)
count = 0
gmt={}
# Strips the newline character
for line in Lines:
#    print("Line{}: {}".format(count, line.strip()))
   # print(count, line.strip())
    wl=float(line.strip().split()[0])
    Cext=float(line.strip().split()[1])
    gmt[count]=wl,Cext
    #print(gmt[count][1])
#    data[count] = [ float(data[count][1].split()[0]), float(data[count][1].split()[1]) ]
    count += 1
file1.close()
Nconst=np.sum([ float(i[1]) for i in gmt.values() ])

#### to handle nonconvergence in gmt.dat  ####
#print('[ gmt[0][i] for i in range(len(gmt)) ]:',[ int(gmt[i][1]) for i in range(len(gmt)) ])
if 99999 in [ gmt[i][1] for i in range(len(gmt)) ]:
    print('non-convergence encountered in ' + fn + '. It is not to be normalized:')	
    Nconst=1
    print('Nconst:',Nconst)
    gmt=[ (i[0],float(i[1])/Nconst ) for i in gmt.values() ]
    normalize=np.sum([ float(i[1] ) for i in gmt ] )
    print('sum of Cext is not normalised:',normalize)
else:	
    gmt=[ (i[0],float(i[1])/Nconst ) for i in gmt.values() ]
    print(fn+' normalized:')	
    print('Nconst:',Nconst)
    normalize=np.sum([ float(i[1] ) for i in gmt ] )
    print('sum of Cext is normalised, normalize:',normalize)

#print('gmt:',gmt)
print('')
##### end of treat gmt ##############



##### treat'experimental.dat' ##############

fn = 'experimental.dat'
print('fn:',fn)
file1 = open(fn, 'r')
Lines = file1.readlines()
Lines=Lines[2:]
#print(Lines)
count = 0
exp={}
# Strips the newline character
for line in Lines:
#    print("Line{}: {}".format(count, line.strip()))
   # print(count, line.strip())
    wl=float(line.strip().split()[0])
    Cext=float(line.strip().split()[1])
    exp[count]=wl,Cext
#    data[count] = [ float(data[count][1].split()[0]), float(data[count][1].split()[1]) ]
    count += 1
file1.close()
Nconst=np.sum([ float(i[1]) for i in exp.values() ])
print('Nconst:',Nconst)
exp=[ (i[0],float(i[1])/Nconst ) for i in exp.values() ]
print(fn+' normalized:')
#print('exp:',exp)
normalize=np.sum([ float(i[1] ) for i in exp ] )
print('Sum of Cext is normalised:',normalize)
#print('')
##### end of treat'experimental.dat' ##############



#fig = plt.figure()
#ax1 = fig.add_subplot(111)
print('')
x=[ i[0] for i in gmt ]
ygmt=[ i[1] for i in gmt ]
yexp=[ i[1] for i in exp ]
sigma=np.sqrt(np.sum([ (ygmt[i]-yexp[i])**2 for i in range(len(ygmt))])/len(ygmt))
sigma=round(sigma, 8)
sigma=str(sigma)
#ax1.plot(x[:], ygmt[:], marker="s", label='gmt')
#ax1.plot(x[:],yexp[:],marker="o", label='exp')
#plt.legend(loc='upper right');
#plt.title('Normalized Cext vs. wavelength (nm).' + "\n" + 'Sigma='+sigma)
#plt.show()
#plt.savefig('sigma.png')

f = open("results.tmp", "w")
f.write(sigma)
f.close()
print('sigma:',sigma)

#import csv
with open('sigma.csv', 'w', newline='') as f:
    string='wavelength(nm)    Cext(gmt)    Cext(exp)' + "\n"
 #       writer.writerows(string)
    f.write(string)
    #writer = csv.writer(f)
    for i in range(len(x)):
        string=str(x[i]) + ' ' + str(ygmt[i]) + ' ' + str(yexp[i]) + "\n"
 #       writer.writerows(string)
        f.write(string)




