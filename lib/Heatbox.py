#Code for temperature zones for the evolution simulator
import pygame

from lib.Helper import colourcontrol
from lib.Helper import vcolourcontrol
from lib.Helper import nonzero

class Heatbox(pygame.rect.Rect):
	"""docstring for Heatbox"""
	def __init__(self, temperature, x, y , width, height):
		self.temperature = temperature
		self.colour = (colourcontrol(self.temperature*5), colourcontrol(100-nonzero(self.temperature)), colourcontrol(100-self.temperature*5))
		super(Heatbox, self).__init__(x, y, width, height)

	def update(self):
		self.colour = (colourcontrol(self.temperature*5), colourcontrol(100-nonzero(self.temperature)), colourcontrol(100-self.temperature*5))
		