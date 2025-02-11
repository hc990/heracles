'''
Created on 2012/2/6

@author: ishida
'''
import networkx as nx  
from math import  sqrt  
import heapq     
from functools import partial  
from numpy import zeros, random , exp, diag, array
from scipy.linalg import *  
from scipy.cluster.vq import *  
import pylab   
import cPickle as pickle
import os
import tempfile
import matplotlib.pyplot as plt


def poweig(A, x0, maxiter=100, ztol=1.0e-5, mode=0, teststeps=1):
    """
    Performs iterative power method for dominant eigenvalue.
     A  - input matrix.
     x0 - initial estimate vector.
     maxiter - maximum iterations
     ztol - zero comparison.
     mode:
       0 - divide by last nonzero element.
       1 - unitize.
    Return value:
     eigenvalue, eigenvector
    """
    m = len(A)
    xi = x0[:] 
 
    for n in range(maxiter):
       # matrix vector multiplication.
       xim1 = xi[:]
       for i in range(m):
           xi[i] = 0.0
           for j in range(m):
             xi[i] += A[i][j] * xim1[j]
       print n, xi
       if mode == 0:
          vlen = sqrt(sum([xi[k] ** 2 for k in range(m)]))
          xi = [xi[k] / vlen for k in range(m)]
       elif mode == 1:
          for k in range(m - 1, -1, -1):
             c = abs(xi[k])
             if c > 1.0e-5:
                xi = [xi[k] / c for k in range(m)]
                break
       # early termination test.
       if n % teststeps == 0:
          S = sum([xi[k] - xim1[k] for k in range(m)])
          if abs(S) < ztol:
             break
       print n, xi
    # Compute Rayleigh quotient.
    numer = sum([xi[k] * xim1[k] for k in range(m)])
    denom = sum([xim1[k] ** 2 for k in range(m)])
    xlambda = numer / denom
    return xlambda, array([xi])

H = nx.read_gml('karate.gml', encoding='UTF-8', relabel=False)
M = nx.to_numpy_matrix(H)
W = array(M)  
D = diag([reduce(lambda x, y:x + y, Wi) for Wi in W])
L = D - W

x0 = array([1.0 for i in xrange(len(L))])
evals1, evcts2 = eig(L, D)  
print '=====' + str(evals1)
evals = []
evcts = []
for i in range(3):  
   eval, evct = poweig(L, x0, maxiter=10 - i, mode=0)  
   evals.append(eval)
   for j in evct:
       evcts.append(j)
       
print '-----' + str(evals)       
array_evcts = array(evcts).transpose()


#vals = dict (zip(abs(evals1), evcts2.transpose()))    
#keys = vals.keys()  
#keys.sort()  
#Y = array ([vals[k] for k in keys[:3]]).transpose()  


res, idx = kmeans2(array_evcts, 3, minit='points')
nx.write_gml(H, 'aa.gml')
nx.draw(H, node_color=idx)
plt.savefig("karate.png")
plt.show()



