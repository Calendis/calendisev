#Code for organisms in the evolution simulator

from random import random #Imports some functions for generating random numbers
from random import randint

from time import time #Unix time module

from lib.Name import * #Imports lists from Name.py

import pygame #Imports pygame library

from lib.Helper import nonzero #Imports functions from Helper.py
from lib.Helper import nonzerov
from lib.Helper import alfour
from lib.Helper import customlimit
from lib.Helper import binaps
from lib.Helper import raisefromzero

from lib import UltraGlobals #Imports organism lists

PLANT_POPULATION_LIMIT = 500 #This limit is arbitrary and is to keep the simulation running smoothly. I am using 500 on my chromebook,
#so feel free to adjust this based on your CPU power.

ANIMAL_POPULATION_LIMIT = 50 #The limit is lesser for animals, since they are more cpu-intensive.

class Organism(): #Base class for all organisms
	"""docstring for Organism"""
	def __init__(self, colour): #Initialisation function, run when the class is initialised
		super(Organism, self).__init__() #Initialises the parent, which happens not to exist
		self.colour = colour
		self.x = 0 #Some basic properties that an organism must have
		self.y = 0
		self.size = (random()*10) +1
		self.maxspeed = (nonzero(17-self.size/2)/20 +0.05)*2
		self.xspeed = binaps(self.maxspeed / 4)
		self.yspeed = binaps(self.maxspeed / 4)
		self.xaccel = 0
		self.yaccel = 0
		self.hitbox = pygame.Rect(self.x, self.y, self.size/3+2, self.size/3+2)
		self.maxfitness = 175 * (self.size/2)
		self.fitness = self.maxfitness/2
		self.dead = False
		self.dormant = False
		self.seedrange = randint(1,40)
		self.poison = random()

		self.energy = self.maxfitness*2
		self.lifespan = round(((self.maxfitness)*self.size)*0.6)

		self.seerange = randint(round(self.size*2), round(self.size*2))*4	
		
		self.insulation = random()*10
		self.waterproofing = random()*10

		self.mutability = random()*2
		self.gender = randint(0,1)
		if self.gender == 0:
			self.gender = False
		else:
			self.gender = True

		self.target = "other"

		self.colourmod = (0,0,0)
		self.generation = 0

		self.name = name_1[randint(0,(len(name_1)-1))]+name_2[randint(0,len(name_2)-1)]+" "+name_1[randint(0,(len(name_1)-1))]+name_2[randint(0,len(name_2)-1)]

	def update(self): #Function that performs basic tasks on the organism, such as moving
		'''if abs(self.xspeed) > self.maxspeed or abs(self.yspeed) > self.maxspeed:
			self.colour = (255,0,255)#Change to magenta if speed is malfunctioning. (Useful for debugging)
			print("Speed error on "+str(self))
			print(self.xspeed)
			print(self.yspeed)
			print(self.maxspeed)
		else:
			print("Speed normal on "+str(self))
			print(self.xspeed)
			print(self.yspeed)
			print(self.maxspeed)'''

		self.fitness = customlimit(self.fitness, self.maxfitness)
		self.energy = customlimit(self.energy, self.maxfitness)
		if self.energy < 0:
			self.energy = 0

		self.lifespan -= 1 #An organism dies when its lifespan reaches zero
		
		if self.__class__ == Animal: #An organism loses energy, and loses more if it is larger and the closer it is to max speed
			self.energy -= 0.05*self.size*(((self.xspeed+self.yspeed)/2)/self.maxspeed)
			self.energy -= self.poison #It takes energy to produce poison
		
		if self.fitness < 1 or self.lifespan < 0:
			self.dead = True #Kills the organism if its fitness or lifespan variables go too low

		if self.x > 800: #Teleports an organism to the screen edges if it moves beyond
			self.x = 800
		if  self.y > 600:
			self.y = 600
		if self.x < 0:
			self.x = 0
		if self.y < 0:
			self.y  = 0
		
		self.xspeed += self.xaccel #Speed is updated with the acceleration
		self.yspeed += self.yaccel

		self.xspeed = customlimit(self.xspeed, self.maxspeed) #Speed is limited to the max speed
		self.yspeed = customlimit(self.yspeed, self.maxspeed)

		if self.__class__ == Animal: #Speed must never be zero if the organism is an animal
			#self.xspeed = nonzero(self.xspeed)
			#self.yspeed = nonzero(self.yspeed)
			self.xspeed, self.yspeed = nonzerov(self.xspeed, self.yspeed)

		if self.target == False: #Acceleration is set to zero if the organism has no target
			self.xaccel = 0
			self.yaccel = 0
		elif self.target == "other":
			pass
		else:
			self.xaccel = ((self.target.x - self.x)/2) #Acceleration is based on the difference between...
			self.yaccel = ((self.target.y - self.y)/2) #...the coordinates of the organism and the target

			if self.target.dead == True:
				self.target = False #Removes the target if it dies

		if not self.dead:
			self.x += self.xspeed #Updates the x and y positions with the speed, if the organism is alive
			self.y += self.yspeed
		
		self.hitbox = pygame.Rect(self.x-self.size/3, self.y-self.size/3, self.size*2/3+2, self.size*2/3+2)
		#A rectangle object based on the organism's size and position

		self.view = pygame.Rect(self.x-self.seerange/2, self.y-self.seerange/2, self.seerange, self.seerange)
		#Another larger rectangle object based on the organism's size and position
		#It can be thought of as the limits of the organism's vision
		
		if self.__class__ == Plant:
			self.grow() #Runs the grow function if the organism is a plant

			self.size = alfour(self.fitness/50) #Plant size is based off of its fitness
			if self.dormant == True:
				self.colour = ((0,0,0)) #Changes to grey if the plant is dormant...
			elif self.dormant == False:
				self.colour = self.true_colour #...otherwise it reverts to its original colour

	def mutate(self): #Mutates the organism. This can be thought of as a post-init
		
		self.generation += 1 #Increments the generation variable when a creature is created

		#Mutates the colour of the organism
		self.colourmod = (self.colourmod[0]+randint(round(-self.mutability*2),round(self.mutability*2)), self.colourmod[1]+randint(round(-self.mutability*2),round(self.mutability*2)), self.colourmod[2]+randint(round(-self.mutability*2),round(self.mutability*2)))
		self.colour = (self.colour[0]-self.colourmod[0], self.colour[1]-self.colourmod[1], self.colour[2]-self.colourmod[2])
		self.true_colour = self.colour

		#Mutates the size by an amount based on the organism's mutability value
		self.size += randint(round(-self.mutability),round(self.mutability))

		#Mutates the vision range by an amount based on the organism's mutability value
		self.seerange += randint(round(-self.mutability*10),round(self.mutability*10))/10
		
		#Mutates the maximum fitness of the organism...
		self.maxfitness += randint(round(-self.mutability*10),round(self.mutability*10))/10
		
		#Mutates the insulation value of the organism...
		self.insulation += randint(round(-self.mutability*10),round(self.mutability*10))/10
		if self.insulation < 0:
			self.insulation = 0
		self.temprange = range(round(50-(6*self.insulation))-40,round(50-(6*self.insulation)))

		#Mutates the waterproofing value of the organism...
		self.waterproofing += randint(round(-self.mutability*10),round(self.mutability*10))/10
		if self.waterproofing < 0:
			self.waterproofing = 0
		self.waterrange = range(round(50-(6*self.waterproofing))-40,round(50-(6*self.waterproofing)))

		#Mutates the seedrange value if the organism is a plant...
		if self.__class__ == Plant or self.__class__ == CallablePlant:
			self.seedrange += randint(round(-self.mutability),round(self.mutability))

		#Mutates the poison value
		self.poison += randint(round(-self.mutability),round(self.mutability))

		#Mutates the mutability itself
		self.mutability = raisefromzero(self.mutability+randint(round(-self.mutability*10),round(self.mutability*10))/10)

class Animal(Organism): #Class for animal
	"""docstring for Animal"""
	def __init__(self, colour, x, y):
		super(Animal, self).__init__(colour) #Initialises the parent, Organism
		self.colour = colour
		self.x = x
		self.y = y

		self.xspeed *= binaps(randint(0,1)) #Has a 50% chance of reversing the animal's direction
		self.yspeed *= binaps(randint(0,1))

		self.mutate() #Mutates the animal

	def reproduce(self, rsize, rmaxspeed, rmaxfitness, rinsulation, rwaterproofing, rmutability):
		if len(UltraGlobals.animals) < ANIMAL_POPULATION_LIMIT: #The animal can reproduce if this function is called...
			self.fitness -= self.maxfitness/2 #...and there are fewer organsims than the limit

			offspring = CallableAnimal(self.colour, self.x, self.y, rsize, rmaxspeed, rmaxfitness, rinsulation, rwaterproofing, rmutability, self.generation, self.name, self.colourmod)
			UltraGlobals.organisms.append(offspring) #Creates another animal based off of itself
			UltraGlobals.animals.append(offspring)
			self.target = False

class CallableAnimal(Animal): #An Animal class that takes more arguements. Needed for reproduction
	"""docstring for CallableAnimal"""
	def __init__(self, colour, x, y, size, maxspeed, maxfitness, insulation, waterproofing, mutability, generation, name, colourmod):
		super(CallableAnimal, self).__init__(colour, x, y)
		self.colour = colour
		self.x = x
		self.y = y
		self.size = size
		self.maxspeed = maxspeed
		self.maxfitness = maxfitness
		self.insulation = insulation
		self.waterproofing = waterproofing
		self.mutability = mutability

		self.generation = generation
		self.name = name
		self.colourmod = self.colourmod

		self.mutate()
		self.__class__ = Animal #Changes the class of the CallableAnimal to Animal

class Plant(Organism): #Class for plants
	"""docstring for Plant"""
	def __init__(self, colour, x, y):
		super(Plant, self).__init__(colour)
		self.colour = colour
		self.true_colour = colour
		self.x = x
		self.y = y

		self.reproduction_timer = time()

		self.mutate()

		self.maxspeed = 0

	def grow(self): #Function that lets plants grow and reproduce
		if not self.dormant:
			self.energy += 1
			if self.energy >= self.maxfitness:

				self.fitness += 1

			if len(UltraGlobals.plants) < PLANT_POPULATION_LIMIT and time() - self.reproduction_timer > 5 and self.energy > self.maxfitness*0.5:
				self.energy -= self.maxfitness/4 #A plant may reproduce at the cost of energy
				offspring = CallablePlant(self.colour, self.x, self.y, self.seedrange, self.insulation, self.waterproofing, self.mutability, self.size, self.maxfitness, self.poison, self.hitbox, self.generation, self.name, self.colourmod)
				UltraGlobals.organisms.append(offspring)
				UltraGlobals.plants.append(offspring)
				self.reproduction_timer = time()

class CallablePlant(Plant): #Plant class that takes more arguements, needed for reproduction
	"""docstring for CallablePlant"""
	def __init__(self, colour, x, y, seedrange, insulation, waterproofing, mutability, size, maxfitness, poison, hitbox, generation, name, colourmod):
		super(CallablePlant, self).__init__(colour, x, y)
		self.colour = colour
		self.x = x + binaps(self.seedrange)
		self.y = y + binaps(self.seedrange)
		self.seedrange = seedrange
		self.insulation = insulation
		self.waterproofing = waterproofing
		self.mutability = mutability
		self.size = size
		self.maxfitness = maxfitness
		self.poison = poison
		self.hitbox = hitbox
		self.x += binaps(self.size/2)
		self.y += binaps(self.size/2)

		self.generation = generation
		self.name = name
		self.colourmod = colourmod

		self.mutate()

		self.__class__ = Plant #Changes from CallablePlant to Plant after everything is done