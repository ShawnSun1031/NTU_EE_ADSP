# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 21:24:08 2022

@author: dicky1031
"""

import numpy as np
import matplotlib.pyplot as plt


k = 100
N = np.linspace(0,1,2*k+1)
"step 1"
H_d = []
for i in range(len(N)):
    if i/len(N) < 0.5 and i/len(N) > 0:
        H_d.append(-1j)
    elif i/len(N) > 0.5 and i/len(N) < 1:
        H_d.append(1j)
    else:
        H_d.append(0)
        
"transision band"
H_d[k] = -0.5j
H_d[k+1] = 0.5j
H_d[0] = -0.5j
H_d[-1] = 0.5j

H_d = np.array(H_d)
plt.plot(H_d.imag)
plt.show()


"step 2"
r1_n = np.fft.ifft(H_d)
plt.plot(r1_n)
plt.title('ifft')
plt.show()
"same as ifft function"
# r11_n = []
# for i in range(len(H_d)):
#     temp = 0
#     for m in range(len(H_d)):
#         temp += 1/len(N)*(H_d[m]*np.exp(2j*np.pi*m*i/len(N)))
#     r11_n.append(temp)
# plt.plot(r11_n)
# plt.show()

"step 3"
rn = np.concatenate((r1_n[k:], r1_n[0:k]))
plt.plot(rn.real)
plt.title('impulse response')
plt.xlabel('N')
plt.ylabel('amplitude')
plt.show()

"step 4"
F = np.linspace(0,1,10001)
RF = 0

for n in range(len(rn)):
    RF += rn[n]*np.exp(-2j*np.pi*F*(n-k-1))
RF = np.array(RF)

plt.plot(N,H_d.imag,'r--')
plt.plot(F,RF.imag)
plt.legend(['Hibert_d(F)','R(F)'])
plt.title('frequency response')
plt.xlabel('F')
plt.ylabel('amplitude')
plt.show()


