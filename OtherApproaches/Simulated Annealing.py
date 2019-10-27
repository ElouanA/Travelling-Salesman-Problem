import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt
import math

#Define target class
class Target:
   #Initialize Target object
  def __init__(self,x,y,priority):
    self.x = x
    self.y = y
    self.priority = priority
  #Define Oriented distance from Self to target
  def distance(self,target):
    euclidianDis = np.sqrt((self.x-target.x)**2+(self.y-target.y)**2)
    priorityDis = self.priority-target.priority
    totalDis = euclidianDis + priorityDis
    return(totalDis) 

  def __repr__(self):
    return("( x =" + str(self.x) +", y =" + str(self.y) +",priority =" + str(self.priority) +")" )
    
#Define fitness class, which is going to be used to rank individuals
class Fitness:
  #Initialize Fitness object
  def __init__(self,route):
    self.route = route
    self.distance = 0
    
  #Computes and return the total distance of the route
  def routeDistance(self): 
    if self.distance == 0:
      routeDis = 0
      for i in range (0,len(self.route)):
        fromTarget = self.route[i]
        if i+1< len(self.route):
          toTarget = self.route[i+1]
        else: 
          toTarget = self.route[0]
        routeDis += fromTarget.distance(toTarget)
      self.distance=routeDis
    return(self.distance)

#Creates a random route (a permutation of the elements in targetList)
def createRoute(targetList):
  route = random.sample(targetList,len(targetList))
  return(route)
  
#Mutates individual by randomly swapping targets in the route
def mutateIndividual(individual):
  for swapped in range(len(individual)):
    swapWith = int(random.random() * len(individual))
    target1 = individual[swapped]
    target2 = individual[swapWith]   
    individual[swapped] = target2
    individual[swapWith] = target1
  return individual

#Computes a transition probability with the difference of fitness and the current temperature (energy)
def computeTransitionProbability(currentDistance, nextDistance, temperature):
  if nextDistance<currentDistance: 
    transitionProbability = 1
  else: 
    transitionProbability = math.exp(-abs(currentDistance-nextDistance)/temperature)
  return(transitionProbability)

#The function to call to run the simulated annealing algorithm
def simulatedAnnealingAlgorithm(targetList,initialTemperature,coolingRate,stopEpsilonCriteria):
  currentRoute = createRoute(targetList)
  currentDistance = Fitness(currentRoute).routeDistance()
  bestRoute = currentRoute
  bestDistance = currentDistance
  temperature = initialTemperature
  while temperature > stopEpsilonCriteria: 
    nextRoute = mutateIndividual(currentRoute)
    nextDistance = Fitness(nextRoute).routeDistance()
    print("current" + str(currentDistance))
    print("next" + str(nextDistance))
    pick = random.random()
    transitionProbability = computeTransitionProbability(currentDistance,nextDistance,temperature)
    if pick < transitionProbability:
      print("oui")
      currentRoute=nextRoute
      currentDistance=nextDistance
    else:
      print("non")
    if currentDistance < bestDistance: 
      bestRoute = currentRoute
      bestDistance = currentDistance
    temperature = temperature*coolingRate
    print("best" + str(bestDistance))
  return(bestRoute)
 

###  MAIN   ###
  
#Initialize parameters for Simulated Annealing Algorithm
targetListSize=25
initialTemperature= 1000
coolingRate= 0.9995
stopEpsilonCriteria=0.01

#Initialize target list 
targetList=[]
for i in range(0,targetListSize):
  targetList.append(Target(100*random.random(),100*random.random(),100*random.random()))

#Call the simulated annealing on target list with parameters set above
simulatedAnnealingAlgorithm(targetList,initialTemperature,coolingRate,stopEpsilonCriteria)

