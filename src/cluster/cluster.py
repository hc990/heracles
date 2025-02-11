'''
Created on 2011/11/18

@author: ishida
'''
from math import sqrt
from PIL import Image, ImageDraw
import linecache
import re  
import random

def euclidean(v1, v2):
#       if not list:
        pSum = sum(pow(v1[i] - v2[i], 2) for i in range(len(v1)))   
        return 1 / (1 + (pSum))     

def tanamoto(v1, v2):
  c1, c2, shr = 0, 0, 0
  for i in range(len(v1)):
    if v1[i] != 0: c1 += 1 # in v1
    if v2[i] != 0: c2 += 1 # in v2
    if v1[i] != 0 and v2[i] != 0: shr += 1 # in both
  
  return 1.0 - (float(shr) / (c1 + c2 - shr)) 

def rotatematrix(data):
  newdata = []
  print '----->' + str(len(data[0]))
  print '-aa---->' + str(len(data))
  
  for i in range(len(data[0])):
    newrow = [data[j][i] for j in range(len(data))]
    newdata.append(newrow)
  return newdata

def pearson(v1, v2):
  sum1 = sum(v1)
  sum2 = sum(v2)
  
  # Sums of the squares
  sum1Sq = sum([pow(v, 2) for v in v1])
  sum2Sq = sum([pow(v, 2) for v in v2])    
  
  # Sum of the products
  pSum = sum([v1[i] * v2[i] for i in range(len(v1))])
  
  # Calculate r (Pearson score)
  num = pSum - (sum1 * sum2 / len(v1))
  den = sqrt((sum1Sq - pow(sum1, 2) / len(v1)) * (sum2Sq - pow(sum2, 2) / len(v1)))
  if den == 0: return 0

  return 1.0 - num / den
       
            
def drawdendrogram(clust, labels, jpeg='clusters.jpg'):
  # height and width
  h = getheight(clust) * 20
  w = 1200
  depth = getdepth(clust)

  # width is fixed, so scale distances accordingly
  scaling = float(w - 150) / depth

  # Create a new image with a white background
  img = Image.new('RGB', (w, h), (255, 255, 255))
  draw = ImageDraw.Draw(img)

  draw.line((0, h / 2, 10, h / 2), fill=(255, 0, 0))    

  # Draw the first node
  drawnode(draw, clust, 10, (h / 2), scaling, labels)
  img.save(jpeg, 'Png')

def drawnode(draw, clust, x, y, scaling, labels):
  if clust.id < 0:
    h1 = getheight(clust.left) * 20
    h2 = getheight(clust.right) * 20
    top = y - (h1 + h2) / 2
    bottom = y + (h1 + h2) / 2
    # Line length
    ll = clust.distance * scaling
    # Vertical line from this cluster to children    
    draw.line((x, top + h1 / 2, x, bottom - h2 / 2), fill=(255, 0, 0))    
    
    # Horizontal line to left item
    draw.line((x, top + h1 / 2, x + ll, top + h1 / 2), fill=(255, 0, 0))    

    # Horizontal line to right item
    draw.line((x, bottom - h2 / 2, x + ll, bottom - h2 / 2), fill=(255, 0, 0))        

    # Call the function to draw the left and right nodes    
    drawnode(draw, clust.left, x + ll, top + h1 / 2, scaling, labels)
    drawnode(draw, clust.right, x + ll, bottom - h2 / 2, scaling, labels)
  else:   
    # If this is an endpoint, draw the item label
    draw.text((x + 5, y - 7), labels[clust.id], (0, 0, 0))
    
    
def getheight(clust):
      # Is this an endpoint? Then the height is just 1
    if clust.left == None and clust.right == None: return 1
    
      # Otherwise the height is the same of the heights of
      # each branch
    return getheight(clust.left) + getheight(clust.right)

def getdepth(clust):
  # The distance of an endpoint is 0.0
      if clust.left == None and clust.right == None: return 0
    
      # The distance of a branch is the greater of its two sides
      # plus its own distance
      return max(getdepth(clust.left), getdepth(clust.right)) + clust.distance
        
def kcluster(rows, distance=tanamoto, k=4):     
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
  
       
def hcluster(rows, distance=pearson):
         distances = {}
         currentclustid = -1  
    # Clusters are initially just the rows
         clust = [bicluster(rows[i], id=i) for i in range(len(rows))]
         while len(clust) > 1:
            lowestpair = (0, 1)
            closest = distance(clust[0].vec, clust[1].vec)
    # loop through every pair looking for the smallest distance
            for i in range(len(clust)):  
              for j in range(i + 1, len(clust)):
        # distances is the cache of distance calculations
                if (clust[i].id, clust[j].id) not in distances: 
                   distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec, clust[j].vec)
                   
                d = distances[(clust[i].id, clust[j].id)]
                
                if d < closest:
                   closest = d
                   lowestpair = (i, j)
                   
            print closest
            print lowestpair
            
            
            mergevec = [(clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i]) / 2.0 
                                    for i in range(len(clust[0].vec))]
            newcluster = bicluster(mergevec, left=clust[lowestpair[0]],
                         right=clust[lowestpair[1]],
                         distance=closest, id=currentclustid)
            currentclustid -= 1
            del clust[lowestpair[1]]
            del clust[lowestpair[0]]
            clust.append(newcluster)
            print clust
         return clust[0]

def printclust(clust, labels=None, n=0):
  # indent to make a hierarchy layout
  for i in range(n): print ' ',
  if clust.id < 0:
    # negative id means that this is branch
    print '-'
  else:
    # positive id means that this is an endpoint
    if labels == None: print clust.id
    else: print labels[clust.id]

  # now print the right and left branches
  if clust.left != None: printclust(clust.left, labels=labels, n=n + 1)
  if clust.right != None: printclust(clust.right, labels=labels, n=n + 1)
  
class bicluster:
    
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance  
        
pattern = r'\W'
def readfile(file):
    links = {}
    data = []
    for text in linecache.getlines(file)[4:]:  
        values = []       
        for value in re.split(pattern, text.rstrip()):
            values.append(value)  
        if links.has_key(int(values[0])):
            links[int(values[0])].append(int(values[1]))
        else:
            links[int(values[0])] = [int(values[1])]
    tmptoset = []
    for key in links.keys(): 
        tmptoset = list(set(tmptoset) | set(links[key]))
        
    keys = links.keys()
    keys.sort()
    
    for i in keys:
        tmplist = []
        for j in tmptoset: 
            if j in links[i]:
                tmplist.append(1)
            else:
                tmplist.append(0)
        data.append(tmplist)
    return keys, data
            
def main(): 
    keys, data = readfile('wiki-Vote.txt')
    kclust = hcluster(data, distance=tanamoto)
    drawdendrogram(kclust, jpeg='hclust.png', labels=keys)
    hclust = kcluster(data, distance=tanamoto) 
    drawdendrogram(hclust, jpeg='kclust.png', labels=keys)
    
if __name__ == '__main__':
   main()
     
    
