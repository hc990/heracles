'''
Created on 2012/2/6

@author: ishida
'''
import networkx as nx
import matplotlib.pyplot as plt
G = nx.Graph()

H = nx.read_gml('dolphins.gml')
nx.draw(H)  

plt.show()  
