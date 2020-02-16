# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 16:20:05 2019
Samuel Blake
lab 4
"""
import numpy as np
import arcpy
import rasterio, os
from arcpy import env
import arcpy.sa as sa

arcpy.CheckOutExtension('Spatial')
env.workspace = r'G:\Samuel\Semester_3\GIS_Programming\lab4\lab4\lab4\lab4\data'
env.overwriteOutput = 1


list = ['urban_areas.tif', 'water_bodies.tif', 'protected_areas.tif', 'slope.tif', 'ws80m.tif']
list2 =[]

def movingwindow(x,y):
    array = arcpy.RasterToNumPyArray(x)
    meanArray = np.zeros_like(array, dtype=np.float32)
    np.where(array < 0, 0, array)
    for row in range(5, array.shape[0] - 5):
        for col in range(4, array.shape[1] - 4):
            win = array[row - 5:row + 6, col - 4:col + 5]
            if x == list[2]:
                meanArray[row,col] = win.sum()
            elif x == list[1]:
                meanArray[row,col] = win.sum()
            else:
                meanArray[row, col] = win.mean()
    return list2.append(meanArray)


for i in list:
    movingwindow(i, list2)
  
list2 =[]
for x in list:
    array = arcpy.RasterToNumPyArray(x)
    meanArray = np.zeros_like(array, dtype=np.float32)
    np.where(array < 0, 0, array)
    for row in range(5, array.shape[0] - 5):
        for col in range(4, array.shape[1] - 4):
            win = array[row - 5:row + 6, col - 4:col + 5]
            if x == list[2]:
                meanArray[row,col] = win.sum()
            elif x == list[1]:
                meanArray[row,col] = win.sum()
            else:
                meanArray[row, col] = win.mean()
    list2.append(meanArray)


#urban
urban = np.where(list2[0] == 0, 1, 0)
print(urban.sum())
#water    
water = np.where(list2[1] < 0.02, 1, 0)
print(water.sum())
#protected area
protected = np.where(list2[2] < 0.05, 1, 0)
print(protected.sum())
#slope
slope = np.where(list2[3] < 15, 1, 0)
print(slope.sum())
#wind
wind = np.where(list2[4] > 8.5, 1, 0)
print(wind.sum())


#Sum of all criteria
selection_boolean = (urban + water + protected + slope + wind)
print(selection_boolean.sum())

#Ones which sum to 5
five = np.where(selection_boolean == 5)[0].size
print(five)

#Creating a raster file for visualization purposes
os.chdir(r'G:\Samuel\Semester_3\GIS_Programming\lab4\lab4\lab4\lab4\data')
raster = rasterio.open('water_bodies.tif')


#lower left point created
raster.bounds
llpt = arcpy.Point(raster.bounds[0], raster.bounds[1])
sr = arcpy.Describe('slope.tif').spatialReference


resultRast = arcpy.NumPyArrayToRaster(selection_boolean, llpt, 1000, 1000)
arcpy.DefineProjection_management(resultRast, sr)
resultRast.save('FinalResult')
print('The number of suitable sites with a score of 5: {}' .format(np.where(selection_boolean == 5)[0].size))

##Part 2
import numpy as np
from scipy.spatial import cKDTree
import glob, errno 
files = glob.glob(env.workspace + '.\*.txt')

#Reading text files
for name in files:
    try:
        with open(name) as f:
            pass # Success
    except IOError as exc: # Error message
        if exc.errno != errno.EISDIR:
            raise
print(files)

#for loop to get coords into array
for coord in range(len(files)):
    with open(files[coord]) as f:
        lines = f.readlines()
        pairs = [l.split(',') for l in lines]
        pairs.remove(['X', 'Y\n'])
        xcoords=[]
        ycoords=[]
        line_array = arcpy.Array()
        for coords in pairs:
            xcoords.append(coords[0])
            ycoords.append(coords[1])
        for l in range(len(pairs)):
            point = arcpy.Point(float(xcoords[l]), float(ycoords[l]))
            line_array.add(point)
    print(pairs)

#creating target pairs
targetPairs = np.vstack([xcoords,ycoords])
targetPairs2 = targetPairs.T
print(targetPairs2)

#getting upper left and lower right
raster.bounds
ul = [-934830.7131322037, 4016727.486357622]
lr = [186169.28686779633, 2251727.486357622]
cellsize = 1000

#finding centroids
xx = ul[0] + cellsize/2
yy = lr[1] + cellsize/2
xx, yy

#creating arrays containing all x and y coords
x_coords = np.arange(ul[0] + cellsize/2, lr[0], cellsize)
y_coords = np.arange(lr[1] + cellsize/2, ul[1], cellsize)
x_coords, y_coords

#Mesh it up
xx, yy = np.meshgrid(x_coords, y_coords)
coords = np.c_[xx.ravel(), yy.ravel()]

#Reclassifying 5 as 1, everything else as 0
best_suit = np.where(selection_boolean == 5, 1, 0)
print(best_suit.min())
print(best_suit.max())

#Reshape boolean
ravel_coords = xx.ravel()

wind = best_suit.reshape(ravel_coords.shape)
wind

#Muliplying by coords
new_coords = []
for i, e in zip(coords, wind):
    xxx = np.multiply(i[0], e)
    yyy = np.multiply(i[1], e)
    if xxx != 0 and yyy != 0:
        new_coords.append([xxx, yyy])

new_coords
len(new_coords)

#calculate distance between centerpoints and stations
dist, indices = cKDTree(targetPairs2).query(new_coords)

print('The maximum distance in kilometers between the transmission station and suitable site is: ' + str(dist.max()/1000))
print('The minimum distance in kilometers between the transmission station and suitable site is: ' + str(dist.min()/1000))

indices































