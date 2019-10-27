import random, matplotlib.pyplot as plt,math,itertools

#Fonction qui calcule la vitesse nécéssaire pour le ralliement d'une cible en fonction de l'espacement angulaire
#Calculé à partir des données constructeur du Pan & Tilt 
def computeTravelTime(theta0,phi0,theta1,phi1):
    distance= max(abs(theta1-theta0),abs(phi1-phi0))
    if distance < 25: 
        return(1.286*(1-math.exp(-distance/12.75)))
    else: 
        return(0.75+0.0142*distance)

#Algorithme itératif, on regarde toutes les routes possibles et on retourne celle qui minimise la distance
def BruteForceApproach(targetList,startPoint,ponderation):
    minimalDistance = math.inf
    for permutation in itertools.permutations(targetList):
        route=[startPoint]+list(permutation)
        currentRouteDistance = Fitness(route).routeDistance(ponderation)
        if  currentRouteDistance < minimalDistance:
            bestRoute=route
            minimalDistance=currentRouteDistance
    return(bestRoute)  

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
        travelTime = computeTravelTime(self.theta, self.phi, node.theta, node.phi)
        priorityRatio=node.priority/self.priority
        return(travelTime,priorityRatio) 
    #On override la fonction de représentation pour pouvoir utiliser la commande print et identifier les node par l'index    
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
                routeDistance+=alpha*travelTime+(1-alpha)*(i+1)*priorityRatio 
            self.distance=routeDistance
        return(self.distance)

#On crée aléatoirement une route a partir de la liste des noeuds
def createRoute(targetList):
  route = random.sample(targetList,len(targetList))
  return(route)

#Fonction qui affiche les cibles et la route sur un graphe en utilisant la bibliothèque Matplotlib
def plotRoute(route):
    plt.figure()
    x=[]
    y=[]
    colors=[]
    sizes=[]
    for target in route:
        x.append(target.theta)
        y.append(target.phi)
        colors.append(target.priority)
        sizes.append(10*target.priority)
    for i in range(0,len(route)-1):
        plt.plot([route[i].theta,route[i+1].theta],[[route[i].phi],[route[i+1].phi]],color='grey') 
    plt.scatter(x, y, c=colors, s=sizes, alpha=0.5,cmap='magma')
    for i,txt in enumerate(route):
        plt.annotate(txt, (x[i],y[i]))
    plt.colorbar()
    
#Fonction intermédiaire utilisée dans l'algorithme heuristique, permute deux cibles
def twoSwap(route,i,j):
    new=route[:]
    for k in range(i,j+1):
        new[k]=route[i+j-k]
    return(new)
    
#Algorithme heuristique, teste toutes les permutations de deux cibles possible sur une route et retourne la route minimisant la distance 
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
     
#Algoritme du plus proche voisin
def greedyApproachNearestNeighbour(nodeList,startNode):
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

#Fonction qui calcule la liste des valeurs optimale de alpha
def getOptimalAlphaList(maxNodeNumber):
    optimalAlphaList=[]
    #Pour tous les nombres de cibles allant jusqu'a maxNodeNumber
    for nodeListSize in range(0,maxNodeNumber):
        #On fait la moyenne sur numberOfIterations
        numberOfIteration=1000 #nombre d'itération sur lequel on calcule notre valeur en moyenne
        #augmenter ce nombre augmente le temps de calcul et augmente la précision
        #diminuer ce nombre diminue le temps de calcul et diminue la précision
        optimalWeightList=[]
        print(nodeListSize)
        for i in range(0,numberOfIteration):
            print(i)
            nodeList=generateNodeList(nodeListSize)
            startNode=generateStartNode()
            weight=0
            bestWeight=0
            bestTime=math.inf
            while weight<1:
                #Si le nombre de cible est supérieur ou égal à 8
                if nodeListSize>7:
                    copyNodeList=nodeList[:]
                    #On utilise d'abord la méthode du plus proche voisin pour obtenir une route déjà efficace
                    route=greedyApproachNearestNeighbour(copyNodeList,startNode)
                    #On améliore cette route en utilisant la méthode de permutations successives
                    targetListRoute=two_opt(route,weight)
                #Si le nombre de cible est inférieur ou égal à 7
                else: 
                    #On utilise la méthode itérative pour obtenir la route optimale
                    targetListRoute=BruteForceApproach(nodeList,startNode,weight)
                time=percentageTime(targetListRoute,0.80)
                #On calcule la valeur de alpha qui minimise le minimum de temps de réponse a 80% par exemple
                if time<bestTime: 
                    bestWeight=weight
                    bestTime=time
                weight+=0.001#incrément sur lequel on joue pour obtenir des valeurs plus fines 
                #augmenter l'incrément diminue le temps de calcul et diminue la précision
                #diminuer l'incrément augmente le temps de calcule et augmente la précision
            #On ajoute à la liste des valeurs optimales de alpha la valeur trouvée
            optimalWeightList.append(bestWeight)
        #On trouve la valeur moyenne des poids optimaux calculés sur le nombre d'itérations
        optimalAlphaList.append(sum(optimalWeightList)/len(optimalWeightList))
    return(optimalAlphaList)
    
#Fonction qui calcule pour une route donnée le temps de réponse pour traiter un pourcentage de la priorité totale
def percentageTime(targetListRoute,percentage):
    totalPriority=0
    for target in targetListRoute[1:]:
        totalPriority += target.priority
    currentPriority=0
    currentTime=0
    currentIndex=0
    while currentPriority < percentage*totalPriority:
        currentPosition=targetListRoute[currentIndex]
        nextPosition=targetListRoute[currentIndex+1]
        currentTime+=currentPosition.edgeDistance(nextPosition)[0]
        currentPriority+=targetListRoute[currentIndex+1].priority
        currentIndex+=1
    return(currentTime)

#Fonction qui génère aléatoirement une configuration de cible
def generateNodeList(nodeListSize):  
    nodeList=[]
    for i in range (0,nodeListSize):
        nodeList.append(Node(i,120*random.random()-60,120*random.random()-60,100*random.random()))
    return(nodeList)
    
#Fonction qui génère aléatoirement une cible de départ
def generateStartNode():
    startNode=Node('start',120*random.random()-60,120*random.random()-60,math.inf)
    return(startNode)

#MAIN#
    
#On définit le nombre de cible maximal jusqu'auquel on va calculer la valeur optimale de alpha
maxNodeNumber=20
#On appelle la fonction qui calcule les valeurs optimales de alpha
optimalAlphaList=getOptimalAlphaList(maxNodeNumber)
#On trace les valeurs de alpha
plt.scatter([i for i in range(0,maxNodeNumber)],optimalAlphaList)
#On écrit les valeurs de alpha dans un fichier texte dans le répertoire courant
fichier=open("alpha values.txt",'w')
for alpha in optimalAlphaList:
    fichier.write(str(alpha) + '\n')
fichier.close()


