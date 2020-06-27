import math
import pandas as pd
import numpy as np

class EOQ:
    def __init__(self,D,Co,I,Clist,Rlist):
        self.D = D
        self.Co = Co
        self.I = I
        self.Clist=Clist
        self.Rlist=Rlist

    def Q(self):
        self.D = D
        self.Co = Co
        self.I = I
        self.Clist = Clist
        self.Rlist = Rlist
        
        C = Clist
        R = Rlist

        Q = []
        for i in range(len(C)):
            Q.append(np.sqrt((2*D*Co)/(I*C[i])))
        
        Tc = []
        dic = {'Q':[0]*len(Q), 'R':[0]*len(Q)}
        for i in range(len(Q)):
            if i ==0:
                if Q[i] < R[i]:
                    n = (C[i]*D)+((D/Q[i])*Co)+(Q[i]*I*C[i]*0.5)
                    Tc.append(n)   
                else:  # Q = 1
                    n = (C[i]*D)+((D/1)*Co)+(1*I*C[i]*0.5)
                    Tc.append(n)
                    dic['R'][i] = n

            elif i==(len(Q)-1):
                if Q[i] >= R[-1]:
                    n = (C[i]*D)+((D/Q[i])*Co)+(Q[i]*I*C[i]*0.5)
                    Tc.append(n) 
                else:  # Q = Rlist[-1]
                    n = (C[i]*D)+((D/R[-1])*Co)+(R[-1]*I*C[i]*0.5)
                    Tc.append(n)
                    dic['R'][i] = n

            else:
                if R[i-1] <= Q[i] < R[i]:
                    n = (C[i]*D)+((D/Q[i])*Co)+(Q[i]*I*C[i]*0.5)
                    Tc.append(n)
                else:
                    n = (C[i]*D)+((D/R[i-1])*Co)+(R[i-1]*I*C[i]*0.5)
                    Tc.append(n)  
                    dic['R'][i] = n
        

        mini = min(Tc)
        count = Tc.count(mini)

        if Tc[count] in dic['R']:
            Qstr = Rlist[count-1]
        else:
            Qstr = Q[count]

        return mini,Qstr

########### Input ###########
D = float(input('Enter The Total Demand In A Period: '))
Co = float(input('Enter The Cost Of Each Order: '))
I = float(input('Enter Holding cost as a percentage of unit purchase cost (%): '))
# t = float(input('Enter The Duration Of Period (Days): '))
I = I/100

R = input('Enter The Range Of Discounts Respectively (eg. 1000,2000): ')
C = input('Enter The Unit Purchase Cost Respectively (eg. 5,4.8,4.75) ')

list1 = R.split(',')
Rlist = []

for i in list1:
    Rlist.append(int(i))


list2 = C.split(',')
Clist = []
for i in list2:
    Clist.append(float(i))


Rlist.sort()
Clist.sort(reverse=True)


EOQs = EOQ(D=D, Co=Co, I=I, Clist=Clist, Rlist=Rlist)


########### Making DataFrame ############
Q = EOQs.Q()
N = int(D)/Q[1]
t = 360/N

L = {'Effiecient Order Quantity':[Q[1]], 'Total Cost':[Q[0]], 'Number Of Orders':[N], 'Delay Between Orders':[t]}
Data = pd.DataFrame(data=L)
print(Data.to_string(index=False))
input('Press ANY key TO EXIT')
# print('Quantity: ' + str(Q))

