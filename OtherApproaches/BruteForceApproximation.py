import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt
import math

class Target:

    def __init__(self,index,x,y,priority):
        self.index=index
        self.x = x
        self.y = y
        self.priority = priority

    def distance(self,target):
        euclidianDis = np.sqrt((self.x-target.x)**2+(self.y-target.y)**2)
        if self.priority!= None:
            priorityDis = self.priority/target.priority
        else: 
            priorityDis=0
        totalDis = euclidianDis-priorityDis
        return(totalDis) 
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
        
    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return(str(self.index))

    

class Link: 

    def __init__(self,previousNode,nextNode):
        self.previousNode=previousNode
        self.nextNode=nextNode
        self.length=previousNode.distance(nextNode)

    def __repr__(self):
        return("(" + str(self.previousNode.index)+ ',' + str(self.nextNode.index)+")")
  
targetListSize=10
targetList=[]
for i in range (0,targetListSize):
  targetList.append(Target(i,100*random.random(),100*random.random(),100*random.random()))

def defineListLinks(targetList):
  listLinks=[]
  for previousTarget in targetList:
    for nextTarget in targetList:
      if previousTarget != nextTarget:
        listLinks.append(Link(previousTarget,nextTarget))
  return(listLinks)
  
def joinChains(listUsefullLinks):
    delta = 1
    while delta > 0 :
        oldLength=len(listUsefullLinks)
        for chain1 in listUsefullLinks:
            for chain2 in listUsefullLinks:
                if chain1 != chain2:
                    if chain1[-1].nextNode == chain2[0].previousNode:
                        chain=chain1+chain2
                        listUsefullLinks.remove(chain1)
                        listUsefullLinks.remove(chain2)
                        listUsefullLinks.append(chain)    
        delta=oldLength - len(listUsefullLinks)
    return(listUsefullLinks)

def isClosingChain(link, listUsefullLink): 
    result=False
    for chain in listUsefullLink: 
        if link.nextNode == chain[0].previousNode and link.previousNode == chain[-1].nextNode:
                result=True
    return(result)        
    
def bruteForceAlgorithm(targetList):
    listLinks=defineListLinks(targetList)
    listChains=[]
    #Start by removing all links that point to starting target
    indexToPop=[]
    for i in range (0,len(listLinks)):
        if (listLinks[i].nextNode == targetList[0]):
            indexToPop.append(i)
    indexToPop.sort(reverse=True)
    for i in range (0,len(indexToPop)):
        listLinks.pop(indexToPop[i])
      
    while len(listLinks) > 0:
        minimalDistance=math.inf
        for i in range (0, len(listLinks)):
            if minimalDistance>listLinks[i].length and not isClosingChain(listLinks[i],listChains):
                minimalDistanceLink=listLinks[i]
                minimalDistance=listLinks[i].length
                minimalDistanceLinkIndex=i
        listChains.append([listLinks[minimalDistanceLinkIndex]])
        indexToPop=[]
        for i in range (0,len(listLinks)):
            if (listLinks[i].previousNode == minimalDistanceLink.previousNode) or (listLinks[i].nextNode == minimalDistanceLink.nextNode): 
                indexToPop.append(i)
        indexToPop.sort(reverse=True)
        for i in range (0,len(indexToPop)):
            listLinks.pop(indexToPop[i])
        print(listChains)
        listChains=joinChains(listChains)
        print(listChains)
    listUsefullLinks=listChains[0]

    totalDis=0
    for i in range (0,len(listUsefullLinks)):
        totalDis+=listUsefullLinks[i].length
    return(listUsefullLinks)

listUsefullLinks=bruteForceAlgorithm(targetList)
def checkNodes(listUsefullLinks):
  for i in range (0,len(listUsefullLinks)):
    spreviousprevious=0 
    snextprevious=0
    spreviousnext=0
    snextnext=0
    for j in range(0,len(listUsefullLinks)):
      if listUsefullLinks[i].previousNode==listUsefullLinks[j].previousNode:
        spreviousprevious+=1
      if listUsefullLinks[i].previousNode==listUsefullLinks[j].nextNode:
        spreviousnext+=1
      if listUsefullLinks[i].nextNode==listUsefullLinks[j].previousNode:
        snextprevious+=1
      if listUsefullLinks[i].nextNode==listUsefullLinks[j].nextNode:
        snextnext+=1
    if spreviousprevious!=1:
      return(False)
      break
    if spreviousnext!=1:
      return(False)
      break
    if snextprevious!=1:
      return(False)
      break
    if snextnext!=1:
      return(False)
      break
  return(True)
  
def translateResultFromLinkListToTargetList(listUsefullLinks):
    result=[]
    for i in range(0,len(listUsefullLinks)):
        result.append(listUsefullLinks[i].previousNode)
    result.append(listUsefullLinks[-1].nextNode) 
    totalDis=0
    for i in range (0,len(result)-1):
        totalDis+=result[i].distance(result[i+1])
    totalDis+=result[-1].distance(result[0])
    return(result,totalDis)

targetListRoute,distance=translateResultFromLinkListToTargetList(listUsefullLinks)
def addStartingTarget(targetListRoute,distance,startingPoint):
    bestDistance=math.inf
    for i in range(0,len(targetListRoute)-1):
        tempDistance=distance - targetListRoute[i].distance(targetListRoute[i+1])
        tempDistance+= startingPoint.distance(targetListRoute[i+1])
        if tempDistance<bestDistance: 
            print('yes')
            bestDistance=tempDistance
            indexToInsert=i+1
    tempDistance=distance - targetListRoute[-1].distance(targetListRoute[0])
    tempDistance+= startingPoint.distance(targetListRoute[0])
    if tempDistance<bestDistance: 
       print('yes')
       bestDistance=tempDistance
       indexToInsert=0
    targetListRoute=targetListRoute[indexToInsert:]+targetListRoute[:indexToInsert]
    targetListRoute.insert(0,startingPoint)
    return(targetListRoute)

startingPoint=Target('start',100*random.random(),100*random.random(),None)
targetListRoute=addStartingTarget(targetListRoute,distance,startingPoint)

print(targetListRoute)
x=[]
y=[]
colors=[]
sizes=[]
for target in targetListRoute:
    x.append(target.x)
    y.append(target.y)
    if target.priority != None:
        colors.append(target.priority)
        sizes.append(10*target.priority)
    else: 
        colors.append(0)
        sizes.append(1)
for i in range(0,len(targetListRoute)-1):
    plt.plot([targetListRoute[i].x,targetListRoute[i+1].x],[[targetListRoute[i].y],[targetListRoute[i+1].y]],color='grey')
plt.scatter(x, y, c=colors, s=sizes, alpha=0.5,
            cmap='magma')
for i,txt in enumerate(targetListRoute):
    plt.annotate(txt, (x[i],y[i]))
plt.colorbar()


