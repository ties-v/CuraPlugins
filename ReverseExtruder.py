#Name:Reverse Extruder direction
#Info:Reverses the direction of the extruder. You can edit the extrude amount by the Flow setting.
#Help:ReverseExtruder
#Depend: GCode
#Type: postprocess

## Written by TV productions info@tv-productions.org
## This script is licensed under the GPLv3

__copyright__ = "Written by TV productions and licensed under the GPLv3"

import re

def getValue(line, key, default = None):
	if not key in line or (';' in line and line.find(key) > line.find(';')):
		return default
	subPart = line[line.find(key) + 1:]
	m = re.search('^[0-9]+\.?[0-9]*', subPart)
	if m == None:
		return default
	try:
		return float(m.group(0))
	except:
		return default

with open(filename, "r") as g:
	lines = g.readlines()

x = dx = y = dy = z = dz = e = de = f = df = 0

with open(filename, "w") as g:
	for line in lines:
		if getValue(line, 'G', None) == 1:
			x = getValue(line, 'X', dx)
			y = getValue(line, 'Y', dy)
			z = getValue(line, 'Z', dz)
			e = getValue(line, 'E', e)
			f = getValue(line, 'F', f)
			
			line = "G1 ";
			if dx != x:
			    line += "X%f " % (x)
			if dy != y:
			    line += "Y%f " % (y)
			if dz != z:
			    line += "Z%f " % (z)
			if de != e:
			    if e != 0:
			        e = -e
			    line += "E%f " % (e)
			if df != f:
			    line += "F%f " % (f)
			
			line += "\n"
			dx = x
			dy = y
			dz = z
			de = e
			df = f
		g.write(line)