#My second attempt at programming an evolution simulator
#Start date 29 Nov, 2016. Prototype dates back to Oct 25, 2016

import pygame #Import pygame, and variables
from pygame.locals import *

from random import randint #A function that generates random integers

from math import sin
from math import log

from time import time #Unix time module

import shelve #Library for saving/loading data

import os.path #Library for handling of filepaths based on operating system

from lib.Helper import tempcontrol #Import various functions from a script
from lib.Helper import nonzero
from lib.Helper import genderfromboolean
from lib.Helper import vcolourcontrol

from lib import UltraGlobals #Import the organisms lists from UltraGlobals.py

from lib.Organism import * #Import the classes for organisms
from lib.Heatbox import * #Import class used for temperature zones

from lib import pygame_textinput

pygame.font.init() #Initialise pygame's font-rendering module

oxygen_reg_path = "fonts/Oxygen-Regular.ttf" #Load some fonts
oxygen_bold_path = "fonts/Oxygen-Regular.ttf"
oxygen_font = pygame.font.Font(oxygen_reg_path, 12)
oxygen_bold_font = pygame.font.Font(oxygen_bold_path, 14)


screen_size = (800, 600) #Define the screen size, which is 1300x600
screen_size_including_gui = (1300, 600)

screen = pygame.display.set_mode(screen_size_including_gui) #Create the pygame window
pygame.display.set_caption("Evolution Simulator")

graph_screen_size = (500, 130)
graph_screen = pygame.Surface((graph_screen_size[0], graph_screen_size[1]))

clock = pygame.time.Clock() #Initialise the pygame clock



############################################################
class Button(): #Base class for buttons
	"""docstring for Button"""
	def __init__(self, x, y, width, height, colour, text):
		super(Button, self).__init__()
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.colour = colour
		self.text = text
		self.text = oxygen_bold_font.render(self.text,1,(0,0,0))


class SaveButton(Button):
	"""docstring for SaveButton"""
	def __init__(self, x, y, width, height, colour):
		self.text = "Save Simulation"
		super(SaveButton, self).__init__(x, y, width, height, colour, self.text)

	def activate(self):
		global savebox
		savebox = True

	def true_activate(self, text):
		global save_text_input
		save_text_input = pygame_textinput.TextInput(oxygen_reg_path, 20, True)

		loaded_simulation = shelve.open("saved_simulations/"+text)

		loaded_simulation["organisms"] = UltraGlobals.organisms
		loaded_simulation["temperature"] = temperature

class SaveCreature(Button):
	"""docstring for SaveCreature"""
	def __init__(self, x, y, width, height, colour):		
		self.text = "Save Creature"
		super(SaveCreature, self).__init__(x, y, width, height, colour, self.text)
		self.on = False

	def activate(self):
		if not self.on:
			self.on = True
			self.colour = (150,200,150)
		else:
			self.on = False
			self.colour = (150,150,150)

class LoadCreature(Button):
	"""docstring for LoadCreature"""
	def __init__(self, x, y, width, height, colour):
		self.text = "Load Creature"
		super(LoadCreature, self).__init__(x, y, width, height, colour, self.text)
		self.on = False

	def activate(self):
		global loadcreaturebox
		loadcreaturebox = True

	def true_activate(self, text):
		global loadcreature_text_input
		global creature_loaded
		global loaded_creature

		loadcreature_text_input = pygame_textinput.TextInput(oxygen_reg_path, 20, True)

		try:
			loaded_creature = shelve.open("saved_creatures/"+text)
			loaded_creature = loaded_creature["creature"]
			creature_loaded = True

		except:
			print("Creature "+text+" not found.")

class LoadButton(Button):
	"""docstring for LoadButton"""
	def __init__(self, x, y, width, height, colour):
		self.text = "Load Simulation"
		super(LoadButton, self).__init__(x, y, width, height, colour, self.text)
 
	def activate(self):
		global loadbox
		loadbox = True

	def true_activate(self, text):
		global temperature
		global load_text_input

		load_text_input = pygame_textinput.TextInput(oxygen_reg_path, 20, True)


		try:
			loaded_simulation = shelve.open("saved_simulations/"+text)
		
			UltraGlobals.organisms = loaded_simulation["organisms"]

			UltraGlobals.plants = []
			UltraGlobals.animals = []

			for organism in UltraGlobals.organisms:
				if organism.__class__ == Plant:
					UltraGlobals.plants.append(organism)
				elif organism.__class__ == Animal:
					UltraGlobals.animals.append(organism)

			temperature = loaded_simulation["temperature"]
		except:
			print("Saved simulation \""+text+"\" not found.")

class KillTool(Button):
	"""docstring for KillTool"""
	def __init__(self, x, y, width, height, colour):
		self.text = "Kill Creature"
		super(KillTool, self).__init__(x, y, width, height, colour, self.text)
		self.on = False

	def activate(self):
		if not self.on:
			self.on = True
			self.colour = (150,200,150)
		else:
			self.on = False
			self.colour = (150,150,150)

class SpeciesKill(Button):
	"""docstring for SpeciesKill"""
	def __init__(self, x, y, width, height, colour):
		self.text = "Kill Species"
		super(SpeciesKill, self).__init__(x, y, width, height, colour, self.text)
		self.on = False

	def activate(self):
		if not self.on:
			self.on = True
			self.colour = (150,200,150)
		else:
			self.on = False
			self.colour = (150,150,150)

class KillSmall(Button):
	"""docstring for KillSmall"""
	def __init__(self, x, y, width, height, colour):
		self.text = "Kill Small"
		super(KillSmall, self).__init__(x, y, width, height, colour, self.text)
		self.on = False

	def activate(self):
		average_sizes = []
		average_size = 0
		for organism2 in UltraGlobals.organisms:
			average_sizes.append(organism2.maxfitness)
							
		for i in range(len(average_sizes)):
			average_size += average_sizes[i]
		average_size /= len(average_sizes)

		for organism2 in UltraGlobals.organisms:
			if organism2.maxfitness < average_size:
				organism2.dead = True
						
############################################################



def class_string(Class): #A function that returns a simplified string from a class definition
	if Class == Animal:
		return "Animal"
	elif Class == Plant:
		return "Plant"

global temperature
temperature = tempcontrol(randint(-40,20) + randint(0,60))/2 #Sets the temperature of the environment

def main():
	global temperature
	global loadbox
	global savebox
	global load_text_input
	global save_text_input
	global loadcreature_text_input
	global loadcreaturebox
	global creature_loaded
	global loaded_creature

	refresh = True

	loadbox = False
	savebox = False

	loadcreaturebox = False
	creature_loaded = False

	load_text_input = pygame_textinput.TextInput(oxygen_reg_path, 20, True)
	save_text_input = pygame_textinput.TextInput(oxygen_reg_path, 20, True)
	loadcreature_text_input = pygame_textinput.TextInput(oxygen_reg_path, 20, True)

	placing = 0

	incrementor = 0

	start_time = time()

	rising = False #Variables to do with temperature control
	falling = False

	show_hitboxes = False #Controls whether hitboxes are drawn or not

	done = False #If true, pygame quits

	info_target = None #A variable to contain a reference to an organism instance when displaying information

	averaging_list = [] #Create an empty list

	calculate_extras = False #If true, calculate some extra things and display them

	PLANT_COLOUR = (90,255,90)#The base colour for plants
	ANIMAL_COLOUR = (255,255,90)#The base colour for animals

	load_button = LoadButton(1170, 10, 110, 30, (150,150,150))
	save_button = SaveButton(1170, 45, 110, 30, (150,150,150))
	kill_tool = KillTool(1170, 80, 110, 30, (150,150,150))
	species_kill = SpeciesKill(1170, 115, 110, 30, (150,150,150))
	kill_small = KillSmall(1170, 150, 110, 30, (150,150,150))
	save_creature = SaveCreature(1170, 185, 110, 30,(150,150,150))
	load_creature = LoadCreature(1170, 220, 110, 30,(150,150,150))

	buttons = [load_button, save_button, kill_tool, species_kill, kill_small, save_creature, load_creature]

	while not done: #Main loop
		events = pygame.event.get()
		if loadbox:
			if load_text_input.update(events):
				load_button.true_activate(load_text_input.get_text())
				loadbox = False

		if savebox:
			if save_text_input.update(events):
				save_button.true_activate(save_text_input.get_text())
				savebox = False

		if loadcreaturebox:
			if loadcreature_text_input.update(events):
				load_creature.true_activate(loadcreature_text_input.get_text())
				loadcreaturebox = False

		for event in events:
			#Event Handling
			if event.type == pygame.QUIT:
				done = True
			if event.type == pygame.KEYDOWN:
				if event.key == K_c:
					if not loadbox and not savebox and not loadcreaturebox:
						new_animal = Animal(ANIMAL_COLOUR,randint(0,screen_size[0]),randint(0,screen_size[1]))
						UltraGlobals.organisms.append(new_animal) #Creates a new Animal instance and adds it to the list
						UltraGlobals.animals.append(new_animal) #Adds the animal to the animals list as well
				if event.key == K_p:
					if not loadbox and not savebox and not loadcreaturebox:
						new_plant = Plant(PLANT_COLOUR,randint(0,screen_size[0]), randint(0,screen_size[1]))
						UltraGlobals.organisms.append(new_plant) #Creates a new Plant instance and adds it to the list
						UltraGlobals.plants.append(new_plant) #Adds the plant to the plants list as well
				if event.key == K_s:
					if not loadbox and not savebox and not loadcreaturebox:
						if show_hitboxes: #Toggles the show_hitboxes variable when s is pressed
							show_hitboxes = False
						elif not show_hitboxes:
							show_hitboxes = True
				if event.key == K_r:
					if not loadbox and not savebox and not loadcreaturebox:
						if refresh: #Toggles refresh
							refresh = False
						elif not refresh:
							refresh = True
				if event.key == K_k: #Toggles the calculate_extras variable when k is pressed
					if not loadbox and not savebox and not loadcreaturebox:
						if calculate_extras:
							calculate_extras = False
						elif not calculate_extras:
							calculate_extras = True
				if event.key == K_UP:# Controls the temperature with the up and down keys
					rising = True
				if event.key == K_DOWN:
					falling = True

			if event.type == pygame.KEYUP:
				if event.key == K_UP:
					rising = False
				if event.key == K_DOWN:
					falling = False

			if event.type == MOUSEBUTTONDOWN:
				for organism in UltraGlobals.organisms: #Detects organisms underneath the cursor when clicked
					if pygame.Rect.colliderect(organism.hitbox, (pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],1,1)) == 1:
						if kill_tool.on:
							organism.dead = True
						if species_kill.on:
							for organism2 in UltraGlobals.organisms:
								if organism2.name == organism.name:
									organism2.dead = True
						if save_creature.on:
							save_creature.activate()
							
							loaded_creature = shelve.open("saved_creatures/"+str(organism.name)+" "+str(organism.generation))
							loaded_creature["creature"] = organism
						else:
							info_target = organism

				if creature_loaded:
					loaded_creature.x = pygame.mouse.get_pos()[0]
					loaded_creature.y = pygame.mouse.get_pos()[1]
					UltraGlobals.organisms.append(loaded_creature)
					creature_loaded = False

				for button in buttons:
					if pygame.Rect.colliderect(pygame.Rect(button.x, button.y, button.width, button.height), (pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],1,1)) == 1:
						button.activate()

		#Logic Below

		organism_count = len(UltraGlobals.organisms)
		incrementor += 1

		temperature += sin((time()-start_time)/10)/200 #Creates the "seasons"

		if rising == True: #Controls the temperature
			temperature += 1
		if falling == True:
			temperature -= 1

		averaging_list = []
		for organism in UltraGlobals.organisms: #Iterates over every object in the organisms list
			organism.update() #Runs the organisms update method

			if calculate_extras: #Calculates some things
				if organism.name not in averaging_list:
					averaging_list.append(organism.name)

			if organism.energy < 1: #Slowly kills an organism if it runs out of energy
				organism.fitness -= 1	

			if round(temperature) not in organism.temprange: #Affects an organism if it is not in the right temperature
				if organism.__class__ == Animal:
					organism.fitness -= 5
				elif organism.__class__ == Plant:
					organism.dormant = True
					organism.energy -= 5
			else:
				if organism.__class__ == Plant:
					organism.dormant = False

			if organism.x > screen_size[0]-organism.size and organism.xspeed > 0:
				organism.xspeed *= -1 #Reverses an organisms direction if it tries to move out of bounds
			elif organism.x < 0 and organism.xspeed < 0:
				organism.xspeed *= -1
			if organism.y > screen_size[1]-organism.size and organism.yspeed > 0:
				organism.yspeed *= -1
			elif organism.y < 0+organism.size and organism.yspeed < 0:
				organism.yspeed *= -1

			if organism.__class__ == Animal:
				for organism2 in UltraGlobals.organisms:
					if organism != organism2:
						if pygame.Rect.colliderect(organism.view, organism2.hitbox) == 1:
							organism.sensory_input["organism"] = organism2
							#print("It sees!")

							if organism.targeter == organism2:
								organism.can_see_targeter = True
								#print("It sees back!")

						if abs(organism.trait_value-organism2.trait_value) < 2000 and organism2.__class__ == Animal and organism.gender != organism2.gender and organism.fitness > organism.maxfitness*0.75 and organism2.fitness > organism2.maxfitness*0.75:
							organism.mating_target = organism2
							#print("It yearns!")

						if pygame.Rect.colliderect(organism.hitbox, organism2.hitbox) == 1:
							if organism.target == organism2:
								#print("It consumes!")
								if organism2.dormant:
									organism.energy += (0.5+organism.poison)
								else:
									organism.energy += (6+organism.poison)
									organism.fitness += (2+organism.poison)
								organism.fitness -= organism2.poison
								organism2.fitness -= (6+organism.poison)
						
							if organism.mating_target == organism2:
								#print("It loves!")
								organism.reproduce((organism.size+organism2.size)/2, 
									(organism.maxspeed+organism2.maxspeed)/2, 
									(organism.maxfitness+organism2.maxfitness)/2, 
									(organism.insulation+organism2.insulation)/2, 
									(organism.mutability+organism2.mutability)/2,
									(organism.aggressiveness+organism2.aggressiveness)/2,
									(organism.defensiveness+organism2.defensiveness)/2)

			if organism.dead == True: #Removes dead organisms from the list and deletes their reference
				UltraGlobals.organisms.remove(organism)
				if organism in UltraGlobals.animals and organism.__class__ == Animal:
					UltraGlobals.animals.remove(organism)
				elif organism in UltraGlobals.plants and organism.__class__ == Plant:
					UltraGlobals.plants.remove(organism)
				del(organism)

		try:
			speciestext = oxygen_bold_font.render(info_target.name,1,(0,0,0)) #Renders text, but does not draw it
			typetext = oxygen_font.render("Type: "+str(class_string(info_target.__class__)),1,(0,0,0))
			sizetext = oxygen_font.render("Size: "+str(round(info_target.size, 1)),1,(0,0,0))
			gendertext = oxygen_font.render("Sex: "+genderfromboolean(info_target.gender),1,(0,0,0))
			generationtext = oxygen_font.render("Generation: "+str(info_target.generation),1,(0,0,0))
			fitnesstext = oxygen_font.render("Fitness: "+str(round(info_target.fitness, 1))+"/"+str(round(info_target.maxfitness, 1)),1,(0,0,0))
			energytext = oxygen_font.render("Energy: "+str(round(info_target.energy, 1)),1,(0,0,0))
			lifetext = oxygen_font.render("Time left: "+str(info_target.lifespan),1,(0,0,0))
			insulationtext = oxygen_font.render("Insulation: "+str(round(info_target.insulation, 1)),1,(0,0,0))
			mutabilitytext = oxygen_font.render("Mutability: "+str(round(info_target.mutability, 1)),1,(0,0,0))
			poisontext = oxygen_font.render("Poison: "+str(round(info_target.poison, 1)),1,(0,0,0))
			traitvaluetext = oxygen_font.render("Trait Value: "+str(info_target.trait_value),1,(0,0,0))
		except:
			speciestext = oxygen_bold_font.render("Click on an organism for statistics...",1,(0,0,0))

		if calculate_extras:
			averageinsulationtext = oxygen_font.render(str(averaging_list),1,(0,0,0))

		temperaturetext = oxygen_font.render("Temperature: "+str(round(temperature,1)),1,(0,0,0))

		if loadbox:
			load_prompt_text = oxygen_bold_font.render("Enter name of file to load:",1,(0,0,0))
		if savebox:
			save_prompt_text = oxygen_bold_font.render("Enter name of file to save:",1,(0,0,0))
		if loadcreaturebox:
			loadcreature_prompt_text = oxygen_bold_font.render("Enter name of creature to load:",1,(0,0,0))

		#Drawing Below
		if refresh:
			screen.fill((colourcontrol(temperature*5), colourcontrol(100-nonzero(temperature)), colourcontrol(100-temperature*5)))
			#Fills the screen with a colour based off of the temperature

			for organism in UltraGlobals.organisms: #Iterates over the organisms and draws them
				pygame.draw.circle(screen, vcolourcontrol((organism.colour)), (round(organism.x), round(organism.y)), round(organism.size/3)+2)

				if show_hitboxes: #Draws hitboxes if show_hitboxes is True
					pygame.draw.line(screen, (255,0,0), (organism.hitbox.x, organism.hitbox.y), (organism.hitbox.x+organism.hitbox.width, organism.hitbox.y))
					pygame.draw.line(screen, (255,0,0), (organism.hitbox.x+organism.hitbox.width, organism.hitbox.y), (organism.hitbox.x+organism.hitbox.width, organism.hitbox.y+organism.hitbox.height))
					pygame.draw.line(screen, (255,0,0), (organism.hitbox.x+organism.hitbox.width, organism.hitbox.y+organism.hitbox.height), (organism.hitbox.x, organism.hitbox.y+organism.hitbox.height))
					pygame.draw.line(screen, (255,0,0), (organism.hitbox.x, organism.hitbox.y+organism.hitbox.height), (organism.hitbox.x, organism.hitbox.y))

					pygame.draw.line(screen, (255,0,0), (organism.view.x, organism.view.y), (organism.view.x+organism.view.width, organism.view.y))
					pygame.draw.line(screen, (255,0,0), (organism.view.x+organism.view.width, organism.view.y), (organism.view.x+organism.view.width, organism.view.y+organism.view.height))
					pygame.draw.line(screen, (255,0,0), (organism.view.x+organism.view.width, organism.view.y+organism.view.height), (organism.view.x, organism.view.y+organism.view.height))
					pygame.draw.line(screen, (255,0,0), (organism.view.x, organism.view.y+organism.view.height), (organism.view.x, organism.view.y))


			#Draws the gui thing
			pygame.draw.rect(screen, (255,255,230), (801,0,399,470))
			pygame.draw.rect(screen, (255,245,210), (1101,0,199,470))
			pygame.draw.rect(screen, (60,60,60), (801,470,500,130))

			for button in buttons:
				pygame.draw.rect(screen, (button.colour), (button.x, button.y, button.width, button.height))
				screen.blit(button.text, (button.x, button.y))

			#Graphs things
			#pygame.draw.rect(graph_screen, (colourcontrol(255-organism_count),colourcontrol(0+organism_count),0), (placing,graph_screen_size[1]-organism_count/(600/130),1,organism_count/(600/130)))

			screen.blit(graph_screen, (806, 475))
			placing += 1
			if placing > 499:
				placing = 0
				graph_screen.fill((0,0,0))

			#Draws boxed when buttons are clicked
			if loadbox:
				pygame.draw.rect(screen, (255,255,210), (806,screen_size[1]-200,489,190))
				screen.blit(load_prompt_text, (808,screen_size[1]-200))
				screen.blit(load_text_input.get_surface(), (980,screen_size[1]-197))
			if savebox:
				pygame.draw.rect(screen, (255,255,210), (806,screen_size[1]-200,489,190))
				screen.blit(save_prompt_text, (808,screen_size[1]-200))
				screen.blit(save_text_input.get_surface(), (980,screen_size[1]-197))
			if loadcreaturebox:
				pygame.draw.rect(screen, (255,255,210), (806,screen_size[1]-200,489,190))
				screen.blit(loadcreature_prompt_text, (808,screen_size[1]-200))
				screen.blit(loadcreature_text_input.get_surface(), (1020,screen_size[1]-197))

			#Draws gui elements
			try:
				screen.blit(speciestext, (810,5)) #Draws text
				screen.blit(typetext, (810,25))
				screen.blit(sizetext, (810, 45))
				screen.blit(gendertext, (810,65))
				screen.blit(generationtext, (810,85))
				screen.blit(fitnesstext, (810,105))
				screen.blit(energytext, (810,125))
				screen.blit(lifetext, (810,145))
				screen.blit(insulationtext, (810,165))
				screen.blit(mutabilitytext, (810,205))
				screen.blit(poisontext, (810,225))
				screen.blit(traitvaluetext, (810,245))
			except:
				screen.blit(speciestext, (810,5))

			if calculate_extras:
				screen.blit(averageinsulationtext, (810,325))

			screen.blit(temperaturetext, (1170,265))
 
			pygame.display.flip() #Updates screen
		clock.tick(60) #Framerate

	pygame.quit() #Quits if all loops are exited

main() #Runs main function