'''
Created on 2012/1/10

@author: ishida
'''


import os
import linecache
import re  
import tempfile
import random


class Cluster(object):
    '''
    defind the class
    1.cluster method
    2.dinstance method    
    '''
    def __init__(self, function, distance): 
        '''
        Constructor
        '''  
        self.function = function
        self.distance = distance
        
def odistance(toNodeIds1, toNodeIds2):
    same = 0
    for toNodeId in toNodeIds1:
        if toNodeIds2.index(toNodeId,) >= 0:
                  same += 1
        all = len(toNodeIds1) + len(toNodeIds2)
        distance = same / all
        return distance
       
def kmeans(rows, distance, k=4):     
        ranges = [(min([row[i] for row in rows]), max([row[i] for row in rows]))
                for i in range(len(rows[0]))]
        
        clusters = [[random.random()*(ranges[i][1] - ranges[i][0]) + ranges[i][0] 
                   for i in range(len(rows[0]))] for j in range(k)]
        
        lastmatches = None
        for t in range(100):
            print  'Iteration %d' % t
            bestmatches = [[]for i in range(k)]
             
            for j in range(len(rows)):
                 row = rows[j]
                 bestmatch = 0
                 for i in range(k):
                     d = distance(clusters[i], row)
                     if d < distance(clusters[bestmatch], row):bestmatch = i
                 bestmatches[bestmatch].append(j)
 
            if bestmatches == lastmatches:break
            else:lastmatches = bestmatches
                     
            for i in range(k):
               avgs = [0.0] * len(rows[0])
               if len(bestmatches[i]) > 0:
                 for rowid in bestmatches[i]:
                     for m in range(len(rows[rowid])):
                         avgs[m] += rows[rowid][m]
                 for j in range(len(avgs)):
                     avgs[j] /= len(bestmatches[i])
                 clusters[i] = avgs
    
        return bestmatches

'''
data structor : one disc
the first one for 
the second one for 
the third one for 

'''
#def kmeans2(discs, distance, k=4):    
#        discs = {'0':[1, 2, 3, 4, 5], '2':[4, 5, 6, 8]}
#        keys = [key for key in discs.keys()]
#        values = [value for value in discs.values()]
#        ranges = [(min(value), max(value))  for value in values]
#        clusters = [[random.random()*(ranges[i][1] - ranges[i][0]) + ranges[i][0] 
#                   for i in range(len(rows[0]))] for j in range(k)]
        
#        lastmatches = None
#        for t in range(100):
#            print  'Iteration %d' % t
#            bestmatches = [[]for i in range(k)]
#             
#            for j in range(len(rows)):
#                 row = rows[j]
#                 bestmatch = 0
#                 for i in range(k):
#                     d = distance(clusters[i], row)
#                     if d < distance(clusters[bestmatch], row):bestmatch = i
#                 bestmatches[bestmatch].append(j)
# 
#            if bestmatches == lastmatches:break
#            else:lastmatches = bestmatches
#                     
#            for i in range(k):
#               avgs = [0.0] * len(rows[0])
#               if len(bestmatches[i]) > 0:
#                 for rowid in bestmatches[i]:
#                     for m in range(len(rows[rowid])):
#                         avgs[m] += rows[rowid][m]
#                 for j in range(len(avgs)):
#                     avgs[j] /= len(bestmatches[i])
#                 clusters[i] = avgs
#    
#        return bestmatches

pattern = r'\W'
        
def getLinks(file):
    if os.path.exists(file):
        links = {}
        for text in linecache.getlines(file)[4:]:         
            values = []
            for value in re.split(pattern, text.rstrip()):
               values.append(value)
            if links.has_key(values[0]):
                links[values[0]].append(int(values[1]))
            else:
                links[values[0]] = [int(values[1])]
        return links   

        
#def rank(self, links):
#        pr = 0.15
#        pageranks = []
#        print len(links)
#        for link in links:
#           linkingcount = len(link.get(link[0]))
#           pagerank = pageranks[link[0]]
#           if pagerank == None:pagerank = 1.0
#           pr = pr + 0.85 * (pagerank / linkingcount)
#        return pr

#def main():  
#   links = getLinks('soc-Epinions1.txt')
#   kmeans2({}, '')
   
#if __name__ == '__main__':
#    main()
