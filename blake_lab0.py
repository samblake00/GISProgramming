'''
*********************************************
author: Samuel Blake
Date: 8/29/2019
Purpose: This script will clip the open space layer to the Boulder,  Lafayette
and Louisville city limits
*********************************************
'''
# Part I
# complete tasks for Part I here:
#Question #1
lst = ['roads', 'cities', 'counties', 'states']
print(lst)

lst2 = []
for i in lst:
    lst2.append(i + '.txt')
        
print(lst2)

#Question 2
import math

exponent = 1
num = math.pi

while num ** exponent < 10000:
    print (num ** exponent)
    exponent += 1

#Question 3
import os
import re

lst3 = os.listdir(r'G:\Samuel\Semester 3\GIS Programming\Lab 1\data\data')

print(lst3)


lst4 = []
for y in lst3:
    if re.search('.dbf', y):
        lst4 += [y]
        
print(lst4)


# Part II - modify the section below:
# import arc license and set workspace
import arcpy
from arcpy import env
env.workspace = r'G:\Samuel\Semester 3\GIS Programming\Lab 1\data\data' # change this to point to the correct folder/path
env.overwriteOutput = 1

# say you wanted to know what feature classes are in your workspace
print('listing feature classes in workspace:')
print(arcpy.ListFeatureClasses())

# define variables
openSpace = 'boulderCountyOpen.shp'

# create lists of shapefile names
cities = ['boulder', 'lafayette', 'louisville']
sites = ['sites53242bld', 'sites430183laf', 'sites329231lou']
sitebuffer = []

# loop through cities list and clip open space to each municipality
for i, s, in zip(cities, sites):
    arcpy.Clip_analysis(openSpace, i+'.shp',  i+'_OpenSpace.shp')
    print('open space clipped to', i, 'city limits')
    arcpy.Buffer_analysis(s+".shp", s+"Buff_3000.shp", "3000 Feet", "FULL", "ROUND", "ALL", "", "PLANAR")
    print('buffer of', s, 'complete')
    arcpy.Clip_analysis(s+"Buff_3000.shp", i+"_OpenSpace.shp", i+"_finalclip.shp")
    print('Site buffers clipped to', i, 'openspace')



print('analysis complete')
#Clip site buffers to Openspace












