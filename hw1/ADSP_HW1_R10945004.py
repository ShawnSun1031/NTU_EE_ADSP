# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 14:12:46 2022

@author: dicky1031
"""

import numpy as np
import math 
import matplotlib.pyplot as plt


N = 17;
fs = 6000;
pass_band = [i/fs for i in range(1,1200)]
transition_band = [i/fs for i in range(1200,1500)]
pass_band_2 = [i/fs for i in range(1501,3000)]
# W_F = 1; W_F = 0.6;
delta = 0.0001; 

k = int((N-1)/2)
F1 = np.linspace(0.0,1200/fs,int((k+2)/2))
F2 = np.linspace(1500/fs, 3000/fs,int((k+2)/2))
F0 = np.array([0, 0.05, 0.1, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5])

max_err = [10];

while True:
    A = np.zeros([k+2,k+2])
    hd = np.zeros(k+2)
    for m in range(0,k+2):
        for n in range(0,k+1):
            A[m,n] = math.cos(2*math.pi*n*F0[m])
        if F0[m] <= 1350/fs:
            A[m,n+1] = 1/1*float((-1)**m)
            hd[m] = 1
        else:
            A[m,n+1] = (1/0.6)*float((-1)**m)
            hd[m] = 0
            
    Ainv = np.linalg.inv(A)
    s = Ainv.dot(hd)
    
    F = np.linspace(0,0.5,1000)
    R = np.zeros([F.shape[0]])
    hd = np.zeros([F.shape[0]])
    w = np.zeros([F.shape[0]])
    for f in range(0,F.shape[0]):
        temp = 0;
        for n in range(0,k+1):
            temp += s[n]*math.cos(2*math.pi*n*F[f])
        R[f] = temp
        if F[f] <= 1350/fs:
            hd[f] = 1
        else:
            hd[f] = 0
        if F[f] <= 1200/fs:
            w[f] = 1
        elif F[f] >= 1500/fs:
            w[f] = 0.6
        else:
            w[f] = 0
    
    
    err = (R - hd)*w
    extrem_F = [];
    extrem_R = [];
    boundary_F = [];
    boundary_R = [];
    
    for i in range(0,F.shape[0]):
        if i == 0:
            if (err[i] > 0) & (err[i] > err[i+1]):
                boundary_F.append(F[i])
                boundary_R.append(abs(err[i]))
            elif (err[i] < 0) & (err[i] <= err[i+1]):
                boundary_F.append(F[i])
                boundary_R.append(abs(err[i]))
        elif i == (F.shape[0]-1):
            if (err[i] > err[i-1]) & (err[i] > 0):
                boundary_F.append(F[i])
                boundary_R.append(abs(err[i]))
            elif (err[i] < err[i-1]) & (err[i] < 0):
                boundary_F.append(F[i])
                boundary_R.append(abs(err[i]))
        else:
            if (err[i]>err[i+1]) & (err[i]>err[i-1]):
                extrem_F.append(F[i])
                extrem_R.append(err[i])
            elif (err[i]<err[i+1]) & (err[i]<err[i-1]):
                extrem_F.append(F[i])
                extrem_R.append(err[i])
    
    while(len(extrem_R) < (k+2)):
        tempR = max(boundary_R)
        for i in range(0,len(boundary_R)):
            if tempR == boundary_R[i]:
                idx = i
        boundary_R.remove(tempR)
        extrem_R.append(tempR)
        tempF = boundary_F[idx]
        boundary_F.remove(tempF)
        extrem_F.append(tempF)
        
        
    (extrem_F,extrem_R) = (list(t) for t in zip(*sorted(zip(extrem_F, extrem_R))))
        
    
    F0 = np.array(extrem_F)
    
    plt.plot(F,R,F,hd)
    plt.show()
    
    plt.plot(F,err,extrem_F,extrem_R,'o')
    plt.show()

    
    
    
    max_err.append(max(abs(err)));
    if (((max_err[-2]-max_err[-1]) < delta) & ((max_err[-2]-max_err[-1])>0)):
        break


err = (R - hd)*w
extrem_F = [];
extrem_R = [];
boundary_F = [];
boundary_R = [];

for i in range(0,F.shape[0]):
    if i == 0:
        if (err[i] > 0) & (err[i] > err[i+1]):
            boundary_F.append(F[i])
            boundary_R.append(abs(R[i]))
        elif (err[i] < 0) & (err[i] <= err[i+1]):
            boundary_F.append(F[i])
            boundary_R.append(abs(R[i]))
    elif i == (F.shape[0]-1):
        if (err[i] > err[i-1]) & (err[i] > 0):
            boundary_F.append(F[i])
            boundary_R.append(abs(R[i]))
        elif (err[i] < err[i-1]) & (err[i] < 0):
            boundary_F.append(F[i])
            boundary_R.append(abs(R[i]))
    else:
        if (err[i]>err[i+1]) & (err[i]>err[i-1]):
            extrem_F.append(F[i])
            extrem_R.append(R[i])
        elif (err[i]<err[i+1]) & (err[i]<err[i-1]):
            extrem_F.append(F[i])
            extrem_R.append(R[i])

while(len(extrem_R) < (k+2)):
    tempR = max(boundary_R)
    for i in range(0,len(boundary_R)):
        if tempR == boundary_R[i]:
            idx = i
    boundary_R.remove(tempR)
    extrem_R.append(tempR)
    tempF = boundary_F[idx]
    boundary_F.remove(tempF)
    extrem_F.append(tempF)
    
(extrem_F,extrem_R) = (list(t) for t in zip(*sorted(zip(extrem_F, extrem_R))))
    

F0 = np.array(extrem_F)
plt.plot(F,R,F,hd,extrem_F,extrem_R,'o')
plt.xlabel('F')
plt.legend(['H(F)','H_d(F)'])
plt.title('frequency response')
plt.show()

plt.plot(F,err)
plt.show()

print('  iteration |   error')
for i in range(1,len(max_err)):
    print(f'\t{i}_th    |   {max_err[i]:.4f}')
    
h_n = np.zeros([N])
y = np.zeros([N])
for i in range(0,s.shape[0]-1):
    h_n[k-i] = s[i];
    h_n[k+i] = s[i];

plt.plot(h_n,color='lightgrey')
plt.plot(n,y,color='black')
n = np.linspace(0,16,17)
plt.bar(n,h_n,width=0.2,color='lightgrey')
plt.scatter(n,h_n,color='lightgrey')
plt.xlabel('n')
plt.ylabel('h[n]')
plt.title(' impulse response h[n]')
plt.show()
