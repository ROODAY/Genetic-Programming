# The following code evolves a set of random numbers to reach a target sum
# An individual in this case is a list of numbers
# A population is a collection of such lists
# As the populations evolve, the fitness scores should go to 0 (i.e. individuals are approaching the target)

from random import random, randint
from operator import add
from functools import reduce

def individual(length,min,max):
  return [randint(min,max) for x in range(length)]

def population(count, length, min, max):
  return [individual(length,min,max) for x in range(count)]

def fitness(individual, target):
  total = reduce(add, individual, 0)
  return abs(target - total)

def grade(pop, target):
  summed = reduce(add, (fitness(x,target) for x in pop), 0)
  return summed / (len(pop) * 1.0)

def evolve(pop, target, retain=0.2, random_select=0.05, mutate=0.01):
  # grade population and take the best to be parents for next generation
  graded = [(fitness(x,target), x) for x in pop]
  graded = [x[1] for x in sorted(graded)]
  retain_length = int(len(graded)*retain)
  parents = graded[:retain_length]

  # randomly add other individuals for diversity
  for individual in graded[retain_length:]:
    if random_select > random():
      parents.append(individual)

  # randomly mutate inviduals to get new features
  for individual in parents:
    if mutate > random():
      index = randint(0, len(individual)-1)
      individual[index] = randint(min(individual), max(individual))

  # "breed" children from parents
  parents_length = len(parents)
  desired_length = len(pop) - parents_length
  children = []
  while len(children) < desired_length:
    parent1 = randint(0,parents_length - 1)
    parent2 = randint(0,parents_length - 1)
    if parent1 != parent2:
      parent1 = parents[parent1]
      parent2 = parents[parent2]
      half = int(len(parent1) / 2)
      child = parent1[:half] + parent2[half:]
      children.append(child)

  parents.extend(children)
  return parents

print("Ensure all inputs are integers")
target = int(input("Target: "))
p_count = int(input("Population Size: "))
i_length = int(input("Individual Length: "))
i_min = int(input("Individual Min Value: "))
i_max = int(input("Individual Max Value: "))
generations = int(input("Number of Generations to Simulate: "))
p = population(p_count, i_length, i_min, i_max)
fitness_history = [grade(p,target)]

for i in range(generations):
  p = evolve(p, target)
  fitness_history.append(grade(p,target))

for datum in fitness_history:
  print(datum)