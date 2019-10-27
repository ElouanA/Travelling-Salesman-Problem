import random, matplotlib.pyplot as plt,math,itertools,time

#On définit les objets que nous allons manipuler pour utiliser nos algorithmes de plus court chemin
class Node:
    #Initialisation d'objet Node, ce sont les noeuds du graphe
    def __init__(self,index,theta,phi,priority):
        self.index = index
        self.theta = theta
        self.phi = phi
        self.priority=priority
    #On définit la distance orientée entre le noeud "self" et le noeud "node"
    def edgeDistance(self,node):
        travelTime = computeTravelTime(self.theta, self.phi,node.theta,node.phi)
        priorityRatio=node.priority/self.priority
        return(travelTime,priorityRatio) 
    def __repr__(self):
        return(str(self.index))

        
#On définit la classe d'objet fitness pour comparer les routes entre elles
class Fitness:
  #Initialisation d'objet de type Fitness, ce qui va nous permettre de comparer des routes
  def __init__(self,route):
    self.route = route #Une route est une permutation de la liste des noeuds nodeList précédée du noeud de départ startNode
    self.distance = math.inf
#Calcule et retourne la "distance" (en terme de graphe) qui dépend de la métrique alpha    
  def routeDistance(self,alpha): 
    if self.distance == math.inf:
      routeDistance = 0
      for i in range (0,len(self.route)-1):
        travelTime,priorityRatio=self.route[i].edgeDistance(self.route[i+1])
        routeDistance += alpha*travelTime + priorityRatio*(1-alpha)*(i+1)
      self.distance=routeDistance
    return(self.distance)
    
#Fonction qui calcule la vitesse nécéssaire pour le ralliement d'une cible en fonction de l'espacement angulaire
#Calculé à partir des données constructeur du Pan & Tilt 
def computeTravelTime(theta0,phi0,theta1,phi1):
    distance= max(abs(theta1-theta0),abs(phi1-phi0))
    if distance < 25: 
        return(1.286*(1-math.exp(-distance/12.75)))
    else: 
        return(0.75+0.0142*distance)
        
#Algorithme itératif
def BruteForceApproach(nodeList,startNode,ponderation):
    minimalDistance = math.inf
    for permutation in itertools.permutations(nodeList):
        route=[startNode]+list(permutation)
        currentRouteDistance = Fitness(route).routeDistance(ponderation)
        if  currentRouteDistance < minimalDistance:
            bestRoute=route
            minimalDistance=currentRouteDistance
    return(bestRoute)  
    
#Fonction qui affiche la route et les différentes cibles
def plotRoute(route):
    plt.figure()
    theta=[]
    phi=[]
    colors=[]
    sizes=[]
    for node in route:
        theta.append(node.theta)
        phi.append(node.phi)
        colors.append(node.priority)
        sizes.append(500)
    for i in range(0,len(route)-1):
        plt.plot([route[i].theta,route[i+1].theta],[[route[i].phi],[route[i+1].phi]],color='grey') 
    plt.scatter(theta, phi, c=colors, s=sizes, alpha=0.5,cmap='magma')
    for i,txt in enumerate(route):
        plt.annotate(txt, (theta[i],phi[i]))
    cbar=plt.colorbar()
    cbar.ax.set_ylabel("priority")
    plt.xlabel("theta")
    plt.ylabel("phi")
    
    plt.figure()
    theta=[]
    phi=[]
    colors=[]
    sizes=[]
    for node in route:
        theta.append(node.theta)
        phi.append(node.phi)
        colors.append(node.priority)
        sizes.append(500)
    #for i in range(0,len(route)-1):
        #plt.plot([route[i].theta,route[i+1].theta],[[route[i].phi],[route[i+1].phi]],color='grey') 
    plt.scatter(theta, phi, c=colors, s=sizes, alpha=0.5,cmap='magma')
    for i,txt in enumerate(route):
        plt.annotate(txt, (theta[i],phi[i]))
    cbar=plt.colorbar()
    cbar.ax.set_ylabel("priority")
    plt.xlabel("theta")
    plt.ylabel("phi")

#Fonction intermédiaire utilisée dans l'algorithme heuristique suivant
def twoSwap(route,i,j):
    copyRoute=route[:]
    for k in range(i,j+1):
        copyRoute[k]=route[i+j-k]
    return(copyRoute)

#Algorithme heuristique   
def two_opt(route,ponderation):
     best=route[:]
     iteration = True
     while iteration:
         iteration = False
         bestCost=Fitness(best).routeDistance(ponderation)
         for i in range(1,len(route)):
             for j in range(i,len(route)):
                 current=twoSwap(best,i,j)
                 if Fitness(current).routeDistance(ponderation)<bestCost:
                     best=current[:]
                     iteration=True
     return(best)
       
#Algorithme du plus proche voisin en terme de priorité     
def greedyApproachNearestNeighbourPriority(nodeList,startNode):
    route=[]
    currentTarget=startNode
    while len(nodeList) > 0:
        route.append(currentTarget)
        minimalDistance = math.inf
        if currentTarget != startNode: 
           nodeList.remove(currentTarget)
        for i in range(0,len(nodeList)):
            travelTime,priorityRatio=currentTarget.edgeDistance(nodeList[i])
            currentDis=1/(priorityRatio+0.00001)
            if minimalDistance > currentDis:
                nextTarget= nodeList[i]
                minimalDistance=currentDis
            if minimalDistance == currentDis and nodeList[i].priority>nextTarget.priority:
                nextTarget= nodeList[i]
                minimalDistance=currentDis
        currentTarget=nextTarget
    return(route)
    
#Algorithme du plus proche voisin en terme de distance angulaire
def greedyApproachNearestNeighbourDistance(nodeList,startNode):
    route=[]
    currentTarget=startNode
    while len(nodeList) > 0:
        route.append(currentTarget)
        minimalDistance = math.inf
        if currentTarget != startNode: 
           nodeList.remove(currentTarget)
        for i in range(0,len(nodeList)):
            travelTime,priorityRatio=currentTarget.edgeDistance(nodeList[i])
            currentDis=travelTime
            if minimalDistance > currentDis:
                nextTarget= nodeList[i]
                minimalDistance=currentDis
            if minimalDistance == currentDis and nodeList[i].priority>nextTarget.priority:
                nextTarget= nodeList[i]
                minimalDistance=currentDis
        currentTarget=nextTarget
    return(route)
    
#Génère aléatoirement une configuration de cibles
def generateNodeList(nodeListSize):  
    nodeList=[]
    for i in range (0,nodeListSize):
        nodeList.append(Node(i,120*random.random()-60,120*random.random()-60,100*random.random()))
    return(nodeList)
  
#Génère aléatoirement un point de départ 'start'
def generateStartNode():
    startNode=Node('start',120*random.random()-60,120*random.random()-60,math.inf)
    return(startNode)
    
nodeListSize=7
#On va lire les valeurs optimales de alpha dans le fichier "alpha values" dans le répertoire courant
fichier = open('alpha values.txt', 'r')
optimalAlphaList=fichier.readlines()
print(len(optimalAlphaList))
nodeList=generateNodeList(nodeListSize) 
startNode=generateStartNode()
if nodeListSize>7 and nodeListSize<len(optimalAlphaList):
    optimalAlpha=float(optimalAlphaList[nodeListSize])
    start=time.time()
    route=greedyApproachNearestNeighbourDistance(nodeList,startNode)
    route=two_opt(route,optimalAlpha)
    end=time.time()
    print(route)
if nodeListSize<=7:
    optimalAlpha=float(optimalAlphaList[nodeListSize])
    start=time.time()
    route=BruteForceApproach(nodeList,startNode,0.6)
    end=time.time()
    plotRoute(route)
    print(route)
if nodeListSize>=len(optimalAlphaList): 
    start=time.time()
    route=greedyApproachNearestNeighbourPriority(nodeList,startNode)
    end=time.time()
    plotRoute(route)
    print(route)
print(end-start)