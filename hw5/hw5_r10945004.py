# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 16:33:40 2022

@author: dicky1031
"""
import numpy as np

def NTTm(N,M):
    # Foward
    # Find the possible alpha between 2 ~ M
    a = []
    for alpha in range(2,M-1+1):
        a.append(alpha)
        for k in range(1,N+1):
            temp = alpha**k%M
            if (temp == 1) & (k!= N) or (temp != 1) & (k == N):
                print(f"pop {alpha}")
                a.pop(a.index(alpha))
                break
    # Use smallest alpha to make a mod table a^1, a^2 .... , a^N
    table = []
    for k in range(1,N+1):
        table.append(a[0]**k%M)
    
    # Calculate NTT, if kn of a^kn is big we can use mod table to avoid big computation
    NTT_matrix = np.empty([N,N])   
    for k in range(N):
        for n in range(N):
            power = k*n
            if power == 0 or power == N:       
                NTT_matrix[k,n] = 1
            elif power > 0 and power < N:
                NTT_matrix[k,n] = table[power - 1]
            else:
                power = power % N
                NTT_matrix[k,n] = table[power - 1]
                
    # Inverse
    # Use smallest alpha to find smallest inverse_alpha
    inverse_a = 1
    while(True):
        if a[0]*inverse_a%M == 1:
            break
        inverse_a += 1
    
    # find smallest inverse_N
    inverse_N = 1
    while(True):
        if N*inverse_N%M == 1:
            break
        inverse_N += 1
        
    # Use smallest inverse_alpha to make a mod table a^-1, a^-2 .... , a^-N
    inverse_table = []
    for k in range(1,N+1):
        inverse_table.append(inverse_a**k%M)
        
    # Calculate inverse_NTT, if kn of a^kn is big we can use mod table to avoid big computation   
    inverse_NTT_matrix = np.empty([N,N])   
    for k in range(N):
        for n in range(N):
            power = k*n
            if power == 0 or power == N:       
                inverse_NTT_matrix[k,n] = 1
            elif power > 0 and power < N:
                inverse_NTT_matrix[k,n] = inverse_table[power - 1]
            else:
                power = power % N
                inverse_NTT_matrix[k,n] = inverse_table[power - 1]
                
    inverse_NTT_matrix = inverse_NTT_matrix*inverse_N%M # remember inv_mat need mutiplied by N^-1
    
    return NTT_matrix, inverse_NTT_matrix

if __name__ == "__main__" :
    N = 6
    M = 7
    [A,B] = NTTm(N, M)
    
        
    
    