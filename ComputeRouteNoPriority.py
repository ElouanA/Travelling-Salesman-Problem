import numpy as np, random, matplotlib.pyplot as plt
import math
import time

start=time.time()
#On définit une fonction qui permet d'afficher une route et l'ensemble des cibles
def plotRoute(route):
    plt.figure()
    theta=[]
    phi=[]
    colors=[]
    sizes=[]
    for node in route:
        theta.append(node.theta)
        phi.append(node.phi)
        colors.append(0)
        sizes.append(100)
    for i in range(0,len(route)-1):
        plt.plot([route[i].theta,route[i+1].theta],[[route[i].phi],[route[i+1].phi]],color='grey') 
    plt.scatter(theta, phi, c=colors, s=sizes, alpha=0.5,
                cmap='magma')
    for i,txt in enumerate(route):
        plt.annotate(txt, (theta[i],phi[i]))
        
#On définit la classe d'objet node pour représenter les les cibles en tant que noeuds pour un problème de graphe
class Node:
    #Méthode de classe pour initialiser un objet de type Noeud
    def __init__(self,index,theta,phi):
        self.index=index
        self.theta = theta
        self.phi = phi
    #Méthode de classe pour calculer la distance angulaire entre deux noeuds
    def distance(self,node):
        return(np.sqrt((self.theta-node.theta)**2+(self.phi-node.phi)**2))
    #On override deux méthodes de classes pour pouvoir utiliser les opérateurs booléens == et != pour tester l'égalité de deux noeuds    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False   
    def __ne__(self, other):
        return not self.__eq__(other)
    #On override également la fonction de réprésentation pour pouvoir représenter simplement une cible par son champ index avec print
    def __repr__(self):
        return(str(self.index))

#On définit également la classe d'objet Link qui représente un lien entre deux noeuds
class Link: 
    #Méthode de classe pour initialiser un objet de type Link
    def __init__(self,previousNode,nextNode):
        self.previousNode=previousNode
        self.nextNode=nextNode
        self.length=previousNode.distance(nextNode)
    #On override la fonction de représentation pour pouvoir représenter facilement un lien avec les index des noeuds
    def __repr__(self):
        return("(" + str(self.previousNode.index)+ ',' + str(self.nextNode.index)+")")

#Cette fonction permet de définir la liste de tous les objets de type Link que l'on peut construire à partir de la liste des objets de type Node
def defineListLinks(nodeList):
  listLinks=[]
  for previousTarget in nodeList:
    for nextTarget in nodeList:
      if previousTarget != nextTarget:
        listLinks.append(Link(previousTarget,nextTarget))
  return(listLinks)
  
#Fonction intermédiaire utilisée dans l'algorithme "BruteForce"
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

#Fonction intermédiaire utilisée utilisée dans l'algorithme "BruteForce"
def isClosingChain(link, listUsefullLink): 
    result=False
    for chain in listUsefullLink: 
        if link.nextNode == chain[0].previousNode and link.previousNode == chain[-1].nextNode:
                result=True
    return(result)        
    
#Algorithme qui calcule une route optimale
def bruteForceAlgorithm(nodeList):
    listLinks=defineListLinks(nodeList)
    listChains=[]    
    while len(listLinks) > 0:
        minimalDistance=math.inf
        for i in range (0, len(listLinks)):
            if len(listLinks) != 1:
                if minimalDistance>listLinks[i].length and not isClosingChain(listLinks[i],listChains):
                    minimalDistanceLink=listLinks[i]
                    minimalDistance=listLinks[i].length
                    minimalDistanceLinkIndex=i
            else: 
                if minimalDistance>listLinks[i].length:
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
        listChains=joinChains(listChains)
    listUsefullLinks=listChains[0]
    totalDis=0
    for i in range (0,len(listUsefullLinks)):
        totalDis+=listUsefullLinks[i].length
    return(listUsefullLinks)

#Fonction qui permet de vérifier que chaque noeud est utilisé une et seulement une fois dans la route
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

#Cette fonction permet simplement de changer le format de la route calculée précédemment
def translateResultFromLinkListToTargetList(listUsefullLinks):
    result=[]
    for i in range(0,len(listUsefullLinks)):
        result.append(listUsefullLinks[i].previousNode)
    return(result)

#Cette fonction calcule l'efficience d'une route en calculant sa "distance" en terme de graphe, pour pouvoir ensuite comparer les routes
def cost(route):
    cost=0
    for i in range(0,len(route)-1):
        cost+=route[i].distance(route[i+1])
    cost+=route[-1].distance(route[0])
    return(cost)

#Cette fonction est un algorithme qui permet d'améliorer une route par permutation successives
def two_opt(route):
     best = route
     improved = True
     while improved:
          improved = False
          for i in range(1, len(route)-2):
               for j in range(i+1, len(route)):
                    if j-i == 1: continue
                    new_route = best[:]
                    new_route[i:j] = best[j-1:i-1:-1]
                    if cost(new_route) < cost(best):  
                         best = new_route
                         improved = True
     best= best[1:] + best[:1]
     improved = True
     while improved:
          improved = False
          for i in range(1, len(route)-2):
               for j in range(i+1, len(route)):
                    if j-i == 1: continue 
                    new_route = best[:]
                    new_route[i:j] = best[j-1:i-1:-1]
                    if cost(new_route) < cost(best): 
                         best = new_route
                         improved = True
          route = best
     return best                

#Cette fonction permet d'insérer le noeud de départ au bon endroit dans la route pour minimiser le coût de la route
def addStartingTarget(targetListRoute,startingPoint):
    distance=cost(targetListRoute)
    bestDistance=math.inf
    for i in range(0,len(targetListRoute)-1):
        tempDistance=distance - targetListRoute[i].distance(targetListRoute[i+1])
        tempDistance+= startingPoint.distance(targetListRoute[i+1])+targetListRoute[i].distance(startingPoint)
        if tempDistance<bestDistance: 
            bestDistance=tempDistance
            indexToInsert=i+1
    tempDistance=distance - targetListRoute[-1].distance(targetListRoute[0])
    tempDistance+= startingPoint.distance(targetListRoute[0])+targetListRoute[-1].distance(startingPoint)
    if tempDistance<bestDistance: 
       bestDistance=tempDistance
       indexToInsert=0
    targetListRoute=targetListRoute[indexToInsert:]+targetListRoute[:indexToInsert]
    targetListRoute.insert(0,startingPoint)
    return(targetListRoute)

#Cette fonction change l'ordre de la liste pour avoir la route qui commence bien par le noeud start  
def removeLinkFromStart(targetListRoute):
    if targetListRoute[0].distance(targetListRoute[-1])<targetListRoute[0].distance(targetListRoute[1]):
        copyNode=targetListRoute
        copyNode.reverse()
        temp=copyNode[-1]
        copyNode.pop(-1)
        copyNode.insert(0,temp)
        return(copyNode)
    else: 
        return(targetListRoute)

#---MAIN---#

#On définit la liste des noeuds générée aleatoirement selon une distribution          
targetListSize=35
targetList=[]
for i in range (0,targetListSize):
    targetList.append(Node(i,120*random.random()-60,120*random.random()-60))    

#On appelles la première partie de l'algorithme sur la liste de noeuds
listUsefullLinks=bruteForceAlgorithm(targetList)
targetListRoute=translateResultFromLinkListToTargetList(listUsefullLinks)

#On génère un point de départ
startingPoint=Node('start',120*random.random()-60,12*random.random()-6)

#puis on apelle la deuxième partie de l'algorithme pour améliorer la route 
targetListRoute=two_opt(targetListRoute)  
#On ajoute le noeud 'start'
targetListRoute=addStartingTarget(targetListRoute,startingPoint)
targetListRoute=removeLinkFromStart(targetListRoute)
#On affiche le résultat
plotRoute(targetListRoute)
end=time.time()
print(end-start)
print(targetListRoute)




