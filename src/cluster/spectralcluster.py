'''
Created on 2012/2/1

@author: ishida
'''
#!/usr/bin/python  
# copyright (c) 2008 Feng Zhu, Yong Sun  
import heapq  
from functools import partial  
from numpy import zeros, random , exp, diag, array
from scipy.linalg import *  
from scipy.cluster.vq import *  
import pylab   
import cPickle as pickle
import os
import tempfile
 
def line_samples ():  
    vecs = random.rand(120, 2)  
    vecs [:, 0] *= 3  
    vecs [0:40, 1] = 1  
    vecs [40:80, 1] = 2  
    vecs [80:120, 1] = 3  
    return vecs



  
def gaussian_simfunc (v1, v2, sigma=1):  
    tee = (-norm(v1 - v2) ** 2) / (2 * (sigma ** 2))  
    return exp (tee)  


def construct_W (vecs, simfunc=gaussian_simfunc):  
    n = len (vecs)  
    W = zeros ((n, n))  
    for i in xrange(n):  
        for j in xrange(i, n):  
            W[i, j] = W[j, i] = simfunc (vecs[i], vecs[j])  
    return W

  
def knn (W, k, mutual=False):  
    n = W.shape[0]  
    assert (k > 0 and k < (n - 1))  
    for i in xrange(n):  
        thr = heapq.nlargest(k + 1, W[i])[-1]  
        for j in xrange(n):  
            if W[i, j] < thr:  
                W[i, j] = -W[i, j]  
    for i in xrange(n):  
        for j in xrange(i, n):  
            if W[i, j] + W[j, i] < 0:  
                W[i, j] = W[j, i] = 0  
            elif W[i, j] + W[j, i] == 0:  
                W[i, j] = W[j, i] = 0 if mutual else abs(W[i, j])  
#vecs = line_samples()  
with open('cluster.pkl.txt') as inf:
        samples = pickle.load(inf)
N = 0
fd, temp_file_name = tempfile.mkstemp()
os.close(fd)
f = open(temp_file_name, 'wt') 
try:
    f.write(str(samples))
finally:
    f.close() 
for smp in samples:
        N += len(smp[0])    
                
vecs = zeros((N, 2))
idxfrm = 0
for i in range(len(samples)):
    idxto = idxfrm + len(samples[i][0])
    vecs[idxfrm:idxto, 0] = samples[i][0]
    vecs[idxfrm:idxto, 1] = samples[i][1]
    idxfrm = idxto
        
W = construct_W (vecs, simfunc=partial(gaussian_simfunc, sigma=2))  
knn (W, 10)  
D = diag([reduce(lambda x, y:x + y, Wi) for Wi in W])  
L = D - W  
evals, evcts = eig(L, D)  
vals = dict (zip(evals, evcts.transpose()))  
keys = vals.keys()  
keys.sort()  
Y = array ([vals[k] for k in keys[:3]]).transpose()  
res, idx = kmeans2(Y, 3, minit='points')  
colors = [(1, 2, 3)[i] for i in idx]  
pylab.scatter(vecs[:, 0], vecs[:, 1], c=colors)  
pylab.show()  
