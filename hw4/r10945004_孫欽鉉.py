# -*- coding: utf-8 -*-
"""
Created on Wed May 11 17:24:02 2022

@author: dicky1031
"""
import cv2 
import numpy as np
import matplotlib.pyplot as plt

#%% SSIM function
def SSIM(A,B,c1,c2):
    mua = np.mean(A)
    mub = np.mean(B)
    vx = np.mean((A-mua)**2)
    vy = np.mean((B-mub)**2)
    vxy = np.mean((A-mua)*(B-mub))
    L = 255
    
    return ((2*mua*mub + (c1*L)**2)*(2*vxy+(c2*L)**2))/((mua**2 + mub**2 + (c1*L)**2)*(vx + vy + (c2*L)**2))

#%% Input setting 
A = cv2.imread("1.png", cv2.IMREAD_GRAYSCALE)
B = cv2.imread("3.png", cv2.IMREAD_GRAYSCALE)
c1 = 1/255**0.5
c2 = 1/255**0.5

ssim = SSIM(A,B,c1,c2)
plt.figure()
plt.suptitle(f"SSIM : {ssim:.4f}\n c1={c1:.4f} c2={c2:.4f}")
plt.subplot(1,2,1)
plt.axis('off')
plt.imshow(A, cmap="gray")
plt.subplot(1,2,2)
plt.axis('off')
plt.imshow(B, cmap="gray")

    
    

