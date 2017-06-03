#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 01:11:14 2017

@author: quien
"""

import numpy as np;
import matplotlib.pyplot as plt;
import matplotlib.image as img;

def evalpoly(p,z):
    return np.dot(p,np.power(z,range(p.shape[0])));

def durand_kerner(p,max_iter,tol):
    Z = np.power(0.7+0.4j,np.arange(p.shape[0]-1));
    for t in range(max_iter):
        W = np.zeros(p.shape[0]-1,dtype=complex)
        for k in range(Z.shape[0]):
           aux = 1.0;
           for l in range(Z.shape[0]):
               if k != l:
                   aux *= Z[k]-Z[l];
           W[k] = evalpoly(p,Z[k])/aux;
        Z -= W;
        if np.linalg.norm(W)<tol:
            break;
    for i in range(Z.shape[0]):
        c = 1;
        z = Z[i];
        for j in range(i+1,Z.shape[0]):
            if np.abs(Z[j]-Z[i])<tol:
                c += 1;
                z += Z[j];
        if c > 1:
            z /= c;
            for j in range(i+1,Z.shape[0]):
                if np.abs(Z[j]-Z[i])<tol:
                    Z[j] = z;
            Z[i] = z;
    return Z;

def gen_p(N,L):
    l = L.reshape((L.shape[0],1));
    o = np.ones(l.shape);
    x = l;
    for n in range(1,N):
        x = np.kron(x,o);
        l = np.kron(o,l);
        x = np.c_[x,l];
    return x;

l = 20;
L = np.arange(-l,l+1);

A = np.zeros((1024,1024));
for n in range(1,4):
    for p in gen_p(n,L):
        Z = durand_kerner(np.r_[p,1.0],1000,1e-10);
        print p,Z;
        for z in Z:
            x = np.real(z);
            y = np.imag(z);
            a = int((x+5.0)*(A.shape[1])/10.0)
            b = int((5.0-y)*(A.shape[0])/10.0)
            for aa in range(-2,+3):
                for bb in range(-2,+3):
                    if 0 <= a+aa < A.shape[1] and 0 <= b+bb < A.shape[0]:
                        A[b+bb][a+aa] += np.exp(-0.01*(aa**2+bb**2));
X = np.log(A+1e-4);
img.imsave("look_at_that.png",X,cmap='jet');