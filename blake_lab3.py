# -*- coding: utf-8 -*-
"""
Samuel Blake

lab 3
"""


##Importing arcpy
import arcpy, random
from arcpy import env
env.workspace = r'G:\Samuel\Semester_3\GIS_Programming\lab3\lab3\lab3\lab3\lab3\lab3.gdb'
env.overwriteOutput = 1
arcpy.CheckOutExtension("Spatial")

#Listing feature classes
sheds = ['wdbhuc8', 'wdbhuc12']
soils = 'ssurgo_mapunits_lab3'

#need to set this
random.seed(0)

#spatial reference
proj = arcpy.Describe(sheds[1]).spatialReference

#create a function for generating a point which sits inside extent.
def create_point(extent):
    x_coord = random.uniform(extent.XMin, extent.XMax)
    y_coord = random.uniform(extent.YMin, extent.YMax)
    point = arcpy.Point(x_coord, y_coord)
    return point

#for loop begins
for shed in sheds:
    arcpy.CreateFeatureclass_management(env.workspace, shed + '_points', "POINT", "", "", "", proj)
    arcpy.AddField_management(shed + '_points', 'shed_id', "TEXT")
    scur = arcpy.da.SearchCursor(shed, ['shape@', shed[3:]])
    point_list =[]
    counts = 0
    for row in scur:
        area = row[0].area
        n = round(row[0].area / 1000000 * 0.05)
        counts += (n)
        extent = row[0].extent
        points_created = 0
        while points_created < n:
            point = create_point(extent)
            if row[0].contains(point):
                point_list.append(point)
                points_created += 1
                shed_id = row[1][0:8]
                incur = arcpy.da.InsertCursor(shed + '_points', ["SHAPE@", 'shed_id'])
                incur.insertRow([point, shed_id])
                del incur
    del scur
    #Intersect & Statistics
    arcpy.Intersect_analysis([shed + "_points", soils], shed + '_intersect', "", "", "INPUT")
    stats = arcpy.Statistics_analysis(shed + '_intersect', shed + "_statistics", [["aws0150", "MEAN"]], "shed_id")
    #Part 2
    curs = arcpy.da.SearchCursor(shed + "_statistics", ["shed_id", "MEAN_aws0150"])
    for rows in curs:
        print('In ' + shed + ' the mean value for watershed ' + str(rows[0]) + ' is ' + str(rows[1]))
    del curs
print('Watershed HUC12 is the beter sampling method as the variance of the mean calculated for wdbhuc12 is less than wdbhuc08. Therefore, the wdbhuc12 sampling method should be used.')







