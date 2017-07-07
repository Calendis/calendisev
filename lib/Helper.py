#Simple functions for manipulating numbers
from random import randint
from math import exp

def sigmoid(x):
	return 1 / (1 + exp(-x))

def colourcontrol(x):
	if x > 255:
		x = 255
	elif x < 0:
		x = 0
	return x

def vcolourcontrol(vector):
	if vector[0] > 255:
		v0 = 255
	elif vector[0] < 0:
		v0 = 0
	else:
		v0 = vector[0]
	if vector[1] > 255:
		v1 = 255
	elif vector[1] < 0:
		v1 = 0
	else:
		v1 = vector[1]
	if vector[2] > 255:
		v2 = 255
	elif vector[2] < 0:
		v2 = 0
	else:
		v2 = vector[2]
	return (v0, v1, v2)


def tempcontrol(x):
	if x > 40:
		x = 40
	elif x < -40:
		x = -40
	return x

def nonzero(x):
	if x == 0:
		x = 1
	return x

def nonzerov(x, y):
	if x == 0 and y == 0:
		x = 1
		y = 1
	return(x, y)

def nonzeror(x):
	if round(x) == 0:
		x = 1
	return x

def raisefromzero(x):
	if x < 0.1:
		x = 0.1
	return x

def raisefromn(x):
	if x < 0:
		x = 0
	return x

def alfour(x):
	if x < 4:
		x = 4
	return x

def customlimit(x, y):#limits x to negative y and y
	if x > y:
		return y
	elif x < -y:
		return -y
	return x

def binaps(x):
	p = randint(0,1)
	if p == 0:
		x *= -1
	return x

def genderfromboolean(bool):
	if bool == False:
		return "Male"
	elif bool == True:
		return "Female"
	else:
		return "Other"