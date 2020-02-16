# -*- coding: utf-8 -*-
"""
Samuel Blake

lab 5
"""
import numpy as np
import rasterio, os
import gdal 
import pandas as pd
import glob
import matplotlib, scipy

#can import functions from other script when in same folder
os.chdir(r'G:\Samuel\Semester_3\GIS_Programming\lab5\data\data')
from lab5functions import *

#Opening DEM
bigElk = 'bigElk_dem.tif'
raster = rasterio.open(bigElk, 'r')
raster.read()
raster.shape

#Read as an Array
ds = gdal.Open('bigElk_dem.tif')
dem = np.array(ds.GetRasterBand(1).ReadAsArray())
cellsize = raster.transform[0]
print(cellsize)
print(dem)

#DEM to numpy array
with rasterio.open(bigElk, 'r') as ds:
    dem = ds.read(1)
    profile = ds.profile
print(dem)
print(profile)

#Convert fire perimeter raster to array
with rasterio.open('fire_perimeter.tif', 'r') as ds:
    fire = ds.read(1)
fire_boolean = np.where(fire ==2, 1, 0)
fire_burned = np.where(fire == 1, 1, 0)

#calculate slope and aspect of clipped DEM
slope, asp = slopeAspect(dem, 30)
print(slope, asp)
#reclassify 
aspect = reclassAspect(asp).astype(np.int8)
print(aspect)
#reclass slope into 5 bins
reclass_slope = reclassByHisto(slope,10)
print(reclass_slope)

#changing directory
os.chdir(r'G:\Samuel\Semester_3\GIS_Programming\lab5\data\data\L5_big_elk')

#grabbing tif files from dir
list = [i for i in glob.glob('*.tif')]
print(list)

#red
b3 = []
#near-IR
b4 = []

#binning files based on b3 or b4
for f in list:
    if f.endswith("B3.tif"):
        b3.append(f)
    elif f.endswith("B4.tif"):
        b4.append(f)
print(b3)
print(b4)

#empty band lists
b3_NDVI = []
b4_NDVI = []

RRlist = []
RRflat = []
for b,s in zip(b3, b4):
    red = rasterio.open(b, 'r').read(1)
    NIR = rasterio.open(s, 'r').read(1)
    rhealth = np.multiply(red, fire_boolean)
    NIRhealth = np.multiply(NIR, fire_boolean)
    NDVI = ((NIR - red)/(NIR + red))
    health = ((NIRhealth - rhealth) / (NIRhealth + rhealth))
    meanNDVI = np.full((280, 459), (np.sum(np.nan_to_num(health))) / np.sum(fire_boolean))
    print(meanNDVI)
    RR = NDVI / meanNDVI
    RRlist.append(RR)
    flat = RR.ravel()
    RRflat.append(flat)
    print(RRflat)

#calculating slope
stackedRR = np.vstack(RRflat)
print(stackedRR)

#polyfit
slp = scipy.polyfit(range(10), stackedRR, 1)[0]
slope = slp.reshape(280, 459)
print(slope)
burned = np.mean(slope[(fire==1)])


#get values from arrays
year = 2002
for i in RRlist:
    burned_RR = np.where(fire==1, i, 0)
    burned_RR = burned_RR[burned_RR !=0]
    RR_complete = burned_RR.mean()
    print('Recovery ratio in year ', year, ' is ', RR_complete)
    year = year+1
print('The coefficient of recovery in the burned area for all years is ' + str(round(burned, 5)))


############################Part 2################################
#classes is the raster classes
#slope is the continuous raster
def zonal_stats (reclass_slope, slope, exclusion_array, exclusion_value, output_csv):
    minimum = []
    maximum = []
    mean2 = []
    stddev = []
    count= []  
    for i in np.unique(reclass_slope):
        reclass_mask = reclass_slope[(exclusion_array==exclusion_value)]
        slope_mask = slope[((exclusion_array==exclusion_value))]
        stat_min = np.min(slope_mask[(reclass_mask==i).flatten()])
        minimum.append(stat_min)
        stat_max = np.max(slope_mask[(reclass_mask==i).flatten()])
        maximum.append(stat_max)
        stat_mean = np.mean(slope_mask[(reclass_mask==i).flatten()])
        mean2.append(stat_mean)
        stat_stddev = np.std(slope_mask[(reclass_mask==i).flatten()])
        stddev.append(stat_stddev)
        stat_count = np.sum(np.where(reclass_mask==i,1,0))
        count.append(stat_count)
    tmin = (np.asarray(minimum)).reshape(len(minimum),1)
    tmax = (np.asarray(maximum)).reshape(len(maximum),1)
    tmean = (np.asarray(mean2)).reshape(len(mean2),1)
    tstd = (np.asarray(stddev)).reshape(len(stddev),1)
    tcount = (np.asarray(count)).reshape(len(count),1)
    stack = np.hstack((tmin, tmax, tmean, tstd, tcount))
    df = pd.DataFrame(stack)
    df.columns = ['Min', 'Max', 'Mean', 'STD', 'Count']
    df.to_csv(output_csv)
    

zonal_stats(reclass_slope, slope, fire, 1, "slope1.csv")
zonal_stats(aspect, slope, fire, 1, "aspect1.csv")

#making values more visible
COF = fire_burned + slope
COF = np.where(COF > .8, slope, np.nan)
#exporting geotiff
with rasterio.open("G:\Samuel\Semester_3\GIS_Programming\lab5\data\data\L5_big_elk\L5034032_2002_B3.tif") as src:
    cof_meta = src.profile
    with rasterio.open("CoefficientRecovery.tif", "w", **cof_meta) as dest:
        dest.write(COF.astype('float32'), indexes=1)

#Print statement conclusion
print('The data shows that aspect of the terrain is best for class 8, or areas between 292.5 and 337.5.' + '\n' + 
      'This indicates that areas facing northwestern will preform best for the recovery ratio while areas facing southeaste' + '\n' + 
      'will preform the worst (112.5 - 157.5). Additionally, areas with higher slope such as classes near class 10 will having a lower mean in recovery.' + '\n' + 
      'Slopes in class 2 preform the best while slopes in class 10 preform the worst. Generally speaking, as slope increases, it decreases in preformance for recovery.')














