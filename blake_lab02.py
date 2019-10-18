# -*- coding: utf-8 -*-
"""
Samuel Blake

Lab 2
"""
##Importing arcpy
import arcpy
from arcpy import env
env.workspace = r'H:\Samuel\Semester_3\GIS_Programming\lab2\data'
env.overwriteOutput = 1
arcpy.CheckOutExtension("Spatial")

#Part 1 reading the text file and extracting x,y coordinates

##Creating list of text files
###importing packages
import glob, os, errno


###pathwawys for text files
files = glob.glob(env.workspace + '.\*\*.txt')

for name in files:
    try:
        with open(name) as f:
            pass # Success
    except IOError as exc: # Error message
        if exc.errno != errno.EISDIR:
            raise
print(files)

##Setting projection
proj = arcpy.Describe(r'H:\Samuel\Semester_3\GIS_Programming\lab2\data\agriculture\GLOBCOVER_2004_lab2.tif').spatialReference
##Creating new shapefile
###fields specified
fields = ['SHAPE@', 'num_coords', 'district']

###Creating shapefile for new polygons
poly = arcpy.CreateFeatureclass_management(env.workspace, 'new_districts.shp', "polygon")

###Adding fields to the shapefile
arcpy.AddField_management('new_districts.shp', 'num_coords', 'short')
arcpy.AddField_management('new_districts.shp', 'district', 'text')

#Creating for loop for iterations

for coord in range(len(files)):
    with open(files[coord]) as f:
        lines = f.readlines()
        pairs = [l.split('\t') for l in lines]
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
        polygon = arcpy.Polygon(line_array)
        num_coords = len(pairs)
        district = files[coord][-5]
        cursor = arcpy.da.InsertCursor(poly, fields)
        cursor.insertRow((polygon, num_coords, district))
    del cursor

arcpy.DefineProjection_management(poly, proj)

#Part 2
os.chdir(r'H:\Samuel\Semester_3\GIS_Programming\lab2\data\agriculture')
ag_tif = [t for t in glob.glob("*.tif")]

ag_table = []
for i in ag_tif:
    ag_table.append(arcpy.sa.ZonalStatisticsAsTable(poly, 'district', i, 'zonal_results_'+i[-13:-9]+'.dbf', 'data', 'SUM'))
    
##Creating cursors for year differences
year = ['2004', '2009']
for s,m in zip(ag_table, year):
    rows = arcpy.SearchCursor(s)
    count = arcpy.ListFields(s)[5]
    pixels = arcpy.ListFields(s)[3]
    iden = arcpy.ListFields(s)[1]
    idname = iden.name
    ctname = count.name
    total = pixels.name
    for r in rows:
        print('Agricultural land in district' + str(r.getValue(idname))+ ' in year ' + m + ' is ' + str((r.getValue(ctname)/r.getValue(total))*100))
    
    
    