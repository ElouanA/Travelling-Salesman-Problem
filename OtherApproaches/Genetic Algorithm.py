import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt

#Define target class, in the context of this genetic algorithm, target are genes
class Target:
  #Initialize Target object
  def __init__(self,index,x,y,priority):
    self.index = index
    self.x = x
    self.y = y
    self.priority = priority
  #Define Oriented distance from Self to target
  def distance(self,target):
    euclidianDis = np.sqrt((self.x-target.x)**2+(self.y-target.y)**2)
    priorityDis = self.priority-target.priority
    totalDis = euclidianDis - priorityDis
    return(totalDis) 
  def __repr__(self):
    return(str(self.index))

class Fitness:
  #Initialize Fitness object
  def __init__(self,route):
    self.route = route
    self.distance = 0
    self.fitness = 0
  #Computes and return the total distance of the route
  def routeDistance(self): 
    if self.distance == 0:
      routeDis = 0
      for i in range (0,len(self.route)-1):
        routeDis += self.route[i].distance(self.route[i+1])
      self.distance=routeDis
    return(self.distance)
  #Computes and return the fitness of the route as the inverse of the distance of the route
  def routeFitness(self): 
    if self.fitness == 0: 
      self.fitness = 1 / float(self.routeDistance())
    return(self.fitness)

def createRoute(targetList):
  route = random.sample(targetList,len(targetList))
  return(route)

def createInitialPopulation(populationSize, targetList): 
  initialPopulation = []
  for i in range (0, populationSize):
    initialPopulation.append(createRoute(targetList))
  return(initialPopulation)

def rankPopulation(population): 
  fitnessResults={}
  for i in range (0, len(population)):
    fitnessResults[i] = Fitness(population[i]).routeFitness()
  return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)

#Gather the index of the selected individuals 
def selectMatingPool(rankedPopulation, eliteSize):
  selectionResults = [] 
  df = pd.DataFrame(np.array(rankedPopulation), columns=["Index","Fitness"])
  df['cum_sum'] = df.Fitness.cumsum()
  df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
  for i in range(0, eliteSize):
    selectionResults.append(rankedPopulation[i][0])
  for i in range(0,len(rankedPopulation)-eliteSize):
    pickProbability = 100*random.random()
    for i in range(0,len(rankedPopulation)):
      if pickProbability <= df.iat[i,3]:
        selectionResults.append(rankedPopulation[i][0])
        break
  return(selectionResults)

#Extract the selected individuals to create the Mating Pool
def createMatingPool(population, selectionResults):
  matingPool=[]
  for i in range (0, len(selectionResults)):
    matingPool.append(population[selectionResults[i]])
  return(matingPool)

def breedIndividuals(parent1,parent2):
  childP1=[]
  childP2=[]
  GeneA=int(random.random()*len(parent1))
  GeneB=int(random.random()*len(parent1))
  startGene=min(GeneA,GeneB)
  endGene=max(GeneA,GeneB)
  for i in range (startGene,endGene):
    childP1.append(parent1[i])
  for i in range(0,len(parent2)):
    if parent2[i] not in childP1:
      childP2.append(parent2[i])
  child = childP1 + childP2
  return(child)

def reproducePopulation(matingPool, eliteSize):
  nextPopulation=[]
  length=len(matingPool)-eliteSize
  #shuffle the Mating Pool
  pool=random.sample(matingPool,len(matingPool))
  for i in range(0, eliteSize):
    nextPopulation.append(matingPool[i])
  
  for i in range (0,length):
    child = breedIndividuals(pool[i], pool[len(matingPool)-i-1])
    nextPopulation.append(child)
  return(nextPopulation)

def mutateIndividual(individual, mutationRate):
  for swapped in range(len(individual)):
    if(random.random() < mutationRate):
      swapWith = int(random.random() * len(individual))
      target1 = individual[swapped]
      target2 = individual[swapWith]   
      individual[swapped] = target2
      individual[swapWith] = target1
  return individual
  
def mutatePopulation(population, mutationRate):
  mutatedPopulation = []
  for individual in range(0, len(population)):
    mutatedIndividual = mutateIndividual(population[individual], mutationRate)
    mutatedPopulation.append(mutatedIndividual)
  return mutatedPopulation

def nextGeneration(currentGeneration, eliteSize, mutationRate):
  rankedPopulation = rankPopulation(currentGeneration)
  selectionResults = selectMatingPool(rankedPopulation,eliteSize)
  matingPool = createMatingPool(currentGeneration, selectionResults)
  nextPopulation = reproducePopulation(matingPool, eliteSize)
  nextGeneration = mutatePopulation(nextPopulation,mutationRate)
  return(nextGeneration)

def geneticAlgorithm(targetList, populationSize, eliteSize, mutationRate, numberOfGenerations):
  population=createInitialPopulation(populationSize,targetList)
  bestRoute = population[0]
  bestFitness = Fitness(bestRoute).routeFitness()
  print(bestFitness)
  for i in range(0, numberOfGenerations):
    population = nextGeneration(population, eliteSize, mutationRate)
    print("fitness à la génération" + str(i) +" :" + str(rankPopulation(population)[0][1]))
    if rankPopulation(population)[0][1]>bestFitness:
      bestRoute=population[rankPopulation(population)[0][0]]
      bestFitness = Fitness(bestRoute).routeFitness()
    print("meilleure fitness rencontrée" + str(bestFitness))
  return(bestRoute)






#Initialize parameters for Genetic Algorithm
targetListSize=1500
populationSize=50
eliteSize = 10
mutationRate = 0.005
numberOfGenerations = 500
targetList=[]

for i in range(0,targetListSize):
  targetList.append(Target(i,100*random.random(),100*random.random(),100*random.random()))
  
targetListRoute = geneticAlgorithm(targetList, populationSize, eliteSize, mutationRate, numberOfGenerations)

x=[]
y=[]
colors=[]
sizes=[]
for target in targetListRoute:
    x.append(target.x)
    y.append(target.y)
    colors.append(target.priority)
    sizes.append(10*target.priority)

for i in range(0,len(targetListRoute)-1):
    plt.plot([targetListRoute[i].x,targetListRoute[i+1].x],[[targetListRoute[i].y],[targetListRoute[i+1].y]])
plt.scatter(x, y, c=colors, s=sizes, alpha=0.5,
            cmap='magma')
for i,txt in enumerate(targetListRoute):
    plt.annotate(txt, (x[i],y[i]))
plt.colorbar()