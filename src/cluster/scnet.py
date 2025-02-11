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
from scipy.cluster.vq import kmeans2
import pylab 
import linecache
import cPickle as pickle
import os
import re   
import tempfile
 
  
def gaussian_simfunc (v1, v2, sigma=1):  
    tee = (-norm(v1 - v2) ** 2) / (2 * (sigma ** 2))  
    return exp (tee)  


def construct_W (links, simfunc=gaussian_simfunc):
    W = zeros ((xn, yn))  
    for i in xrange(xn):  
        for j in xrange(i, yn): 
            if links[i][j] == 1:  
                W[i, j] = 1 
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
#with open('cluster.pkl.txt') as inf:
#        samples = pickle.load(inf)
#N = 0
#fd, temp_file_name = tempfile.mkstemp()
#os.close(fd)
#f = open(temp_file_name, 'wt') 
#try:
#    f.write(str(samples))
#finally:
#    f.close() 
#for smp in samples:
#        N += len(smp[0])    
#                
#vecs = zeros((N, 2))
#idxfrm = 0
#for i in range(len(samples)):
#    idxto = idxfrm + len(samples[i][0])
#    vecs[idxfrm:idxto, 0] = samples[i][0]
#    vecs[idxfrm:idxto, 1] = samples[i][1]
#    idxfrm = idxto
links = {}
pattern = r'\W'
pairs = []
for text in linecache.getlines('wiki-Vote.txt')[4:]:  
     values = []       
     for value in re.split(pattern, text.rstrip()):
         values.append(value)  
     if links.has_key(int(values[0])):
         links[int(values[0])].append(int(values[1]))
     else:
         links[int(values[0])] = [int(values[1])]
     pair = [int(values[0]), int(values[1])]   
     pairs.append(pair)

vecs = array(pairs)
       
tmptoset = []
for key in links.keys(): 
   tmptoset = list(set(tmptoset) | set(links[key]))
xn = len(links.keys())
yn = len(tmptoset)
maxx = max(links.keys())
maxy = max(tmptoset) 

W = zeros ((xn, xn))    
for i in xrange(xn):
    for j in links[links.keys()[i]]:
            z = tmptoset.index(j,)
            W[i, z] = W[z, i] = 1 
        
#W = construct_W (links, simfunc=partial(gaussian_simfunc, sigma=2))  
#knn (W, 10)  
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
