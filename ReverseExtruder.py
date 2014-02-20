#Name:Reverse Extruder direction
#Info:Reverses the direction of the extruder. You can edit the extrude amount by the Flow setting.
#Help:ReverseExtruder
#Depend: GCode
#Type: postprocess
#Param: temperature(float:50) Temperature of the hot-end
#Param: hotindex(float:0) Hot-end index (starting at 0)

## Written by TV productions info@tv-productions.org
## This script is licensed under the GPLv3

__copyright__ = 'Written by TV productions and licensed under the GPLv3'

import re


def getValue(line, key, default=None):
    if not key in line or ';' in line and line.find(key) > line.find(';'
            ):
        return default
    subPart = line[line.find(key) + 1:]
    m = re.search('^[0-9]+\.?[0-9]*', subPart)
    if m == None:
        return default
    try:
        return float(m.group(0))
    except:
        return default


with open(filename, 'r') as g:
    lines = g.readlines()

x = dx = y = dy = z = dz = e = de = ee = f = df = c = 0
comment = ''

with open(filename, 'w') as g:
    for line in lines:
        if getValue(line, 'M', None) == 109:
            line = 'M109 T% S%f\n' % (hotindex, temperature)
        
        if getValue(line, 'G', None) == 1:
            x = getValue(line, 'X', dx)
            y = getValue(line, 'Y', dy)
            z = getValue(line, 'Z', dz)
            e = getValue(line, 'E', e)
            f = getValue(line, 'F', f)
            if de != e:
                c = line.find(';')
                if -1 != c:
                    comment = line[c:].strip()
                
                # Remove another extruder move
                if comment == ";move Z up a bit and retract filament even more":
                    e = de
                
                line = 'G1 '
                if dx != x:
                    line += 'X%f ' % x
                if dy != y:
                    line += 'Y%f ' % y
                if dz != z:
                    line += 'Z%f ' % z
                if e != 0:
                    e = -e

                line += 'E%f ' % e
                if df != f:
                    line += 'F%f ' % f

                # add comment if needed

                line += comment + '\n'
                
                # if comment is the extruder movements before and after the print, remove that line
                if comment == ";retract the filament a bit before lifting the nozzle, to release some of the pressure":
                    line = ";ReverseExtruder: Removed '" + comment + "'\n"
                dx = x
                dy = y
                dz = z
                de = e
                df = f
                comment = ''
        g.write(line)