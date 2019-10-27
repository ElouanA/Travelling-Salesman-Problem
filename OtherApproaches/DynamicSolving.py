import random
import numpy as np
import itertools
import time
import matplotlib.pyplot as plt
import math

"""This code is the implementation of a Dynamic (iterative) Programming Algorithm to solve the Travelling Salesman Problem.
It give the exact best route (shortest distance) but it only works in reasonable time up to about 15 nodes.
As a matter of fact the complexity of this algorithm is approxmatively O(n²*2^n)"""

#The function to call to run the algorithm, it return the list of indexes of nodes in target list in order of appearence in the best route
def DynamicApproach(targetList):
  distanceMatrix = [[this.length(x) for this in targetList] for x in targetList]
  A = {(frozenset([0, idx+1]), idx+1): (dist, [0,idx+1]) for idx,dist in enumerate(distanceMatrix[0][1:])}
  for m in range(2, len(targetList)):
    B = {}
    for Subset in [frozenset(C) | {0} for C in itertools.combinations(range(1, len(targetList)), m)]:
      for j in Subset - {0}:
        B[(Subset, j)] = min( [(A[(Subset-{j},k)][0] + distanceMatrix[k][j], A[(Subset-{j},k)][1] + [j]) for k in Subset if k != 0 and k!=j])  
    A = B
  indexListRoute = min([(A[d][0] + distanceMatrix[0][d[1]], A[d][1]) for d in iter(A)])
  distance=0
  for i in range (len(indexListRoute[1])-1):
    distance+=distanceMatrix[indexListRoute[1][i]][indexListRoute[1][i+1]]
  distance+=distanceMatrix[indexListRoute[1][-1]][indexListRoute[1][0]]
  return indexListRoute[1], distance

def translateResultFromIndexListToTargetList(indexListRoute,targetList):
    targetListRoute=[]
    for i in indexListRoute:
        targetListRoute.append(targetList[i])
    return(targetListRoute)
        
#Define target class
class Target:
  #Initialize target object
  def __init__(self,index,x,y,priority):
    self.index=index
    self.x = x
    self.y = y
    self.priority = priority
  #Define oriented distance between self and target
  def length(self,target):
    euclidianDis = np.sqrt((self.x-target.x)**2+(self.y-target.y)**2)
    if self.priority!= None:
        priorityDis = self.priority/target.priority
    else: 
        priorityDis=0
    totalDis = euclidianDis-priorityDis
    return(totalDis)
  #Override represent function to get better insight when using print function on target objet
  def __repr__(self):
      return('(' + str(self.index) + ')')

#Initialize parameters for this algorithm
targetListSize=10

#Initialize target List
targetList=[]
for i in range (0,targetListSize):
  targetList.append(Target(i,100*random.random(),100*random.random(),100*random.random()))
  
###   MAIN  ###
result, distance = DynamicApproach(targetList)
print(result)
print(distance)
targetListRoute=translateResultFromIndexListToTargetList(result,targetList)

def addStartingTarget(targetListRoute,distance,startingPoint):
    bestDistance=math.inf
    for i in range(0,len(targetListRoute)-1):
        tempDistance=distance - targetListRoute[i].length(targetListRoute[i+1])
        tempDistance+= startingPoint.length(targetListRoute[i+1])
        if tempDistance<bestDistance: 
            print('yes')
            bestDistance=tempDistance
            indexToInsert=i+1
    tempDistance=distance - targetListRoute[-1].length(targetListRoute[0])
    tempDistance+= startingPoint.length(targetListRoute[0])
    if tempDistance<bestDistance: 
       print('yes')
       bestDistance=tempDistance
       indexToInsert=0
    targetListRoute=targetListRoute[indexToInsert:]+targetListRoute[:indexToInsert]
    targetListRoute.insert(0,startingPoint)
    return(targetListRoute)

startingPoint=Target('start',100*random.random(),100*random.random(),None)

new=addStartingTarget(targetListRoute,distance,startingPoint)
print(new)
#Plotting the results

x=[]
y=[]
colors=[]
sizes=[]
for target in new:
    x.append(target.x)
    y.append(target.y)
    if target.priority != None:
        colors.append(target.priority)
        sizes.append(10*target.priority)
    else: 
        colors.append(0)
        sizes.append(1)

for i in range(0,len(new)-1):
    plt.plot([new[i].x,new[i+1].x],[[new[i].y],[new[i+1].y]])
plt.scatter(x, y, c=colors, s=sizes, alpha=0.5,cmap='magma')
for i in range (0,len(new)):
    plt.annotate(new[i].index, (x[i],y[i]))
plt.colorbar()


        

