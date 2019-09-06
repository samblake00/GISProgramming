# -*- coding: utf-8 -*-
"""
Samuel Blake
GIS Programming and Automation
Lab 1
"""
#Setting up the workspace and importing arcpy
import csv
import arcpy
from arcpy import env
env.workspace = r'G:\Samuel\Semester 3\GIS_Programming\Lab1\data\lab1\lab1\lab1.gdb'
env.overwriteOutput = 1
env.qualifiedFieldNames = "UNQUALIFIED"


# List of feature classes
fcs = arcpy.ListFeatureClasses()
print(fcs)

#List of tables
tables = arcpy.ListTables()
print(tables)

#List features classes without watershed
lstfc = ['soilmu_a_co001', 'soilmu_a_co618', 'soilmu_a_co641', 'soilmu_a_co642',
         'soilmu_a_co643', 'soilmu_a_co644', 'soilmu_a_co645', 'soilmu_a_co651',
         'soilmu_a_co653']
print(lstfc)

#List tables
lsttb = ['muaggatt_co001', 'muaggatt_co618', 'muaggatt_co641', 'muaggatt_co642',
         'muaggatt_co643', 'muaggatt_co644', 'muaggatt_co645', 'muaggatt_co651',
         'muaggatt_co653']
print(lsttb)

#Edit feature class strings for last 5 characters
lst2 = []
for i in lstfc:
    lst2.append(i[-5:])
        
print(lst2)

#Joining tables to feature classes
for f, t, z, in zip(lstfc, lsttb, lst2):
    arcpy.JoinField_management(f, "MUSYM", t, "musym")
    arcpy.AddField_management(f, 'map_unit', 'string')
    arcpy.CalculateField_management(f, 'map_unit', ''.join(('"',z,'"')), 'python_9.3')

#carry out the merge operation
arcpy.Merge_management(lstfc,'soil_merge')


#Executing the intersect between soil_merge and watersheds
inFeatures = ['soil_merge', 'wbdhu8_lab1']
intersectOutput = "soil_watershed_intersect"
arcpy.Intersect_analysis(inFeatures, intersectOutput, "ALL")


#PART 2
#Use Select By Attributes to subset features which are withing each watershed
Selection1 = arcpy.SelectLayerByAttribute_management('soil_watershed_intersect', 'NEW_SELECTION', '"HUC8" = 10190005')
Statistics1 = (arcpy.Statistics_analysis(Selection1, r'G:\Samuel\Semester 3\GIS_Programming\Lab1\data\lab1\lab1\Selection5.csv', [["HUC8", "Count"]], ""))


Selection2 = arcpy.SelectLayerByAttribute_management('soil_watershed_intersect', 'NEW_SELECTION', '"HUC8" = 10190006')
Statistics2 = (arcpy.Statistics_analysis(Selection2, r'G:\Samuel\Semester 3\GIS_Programming\Lab1\data\lab1\lab1\Selection3.csv', [["HUC8", "Count"]], ""))

#Read CSV for row with count
FindCount1 = csv.reader(open(r'G:\Samuel\Semester 3\GIS_Programming\Lab1\data\lab1\lab1\Selection5.csv'))
for row in FindCount1:
    text1 = row[2]
print(text1)

FindCount2 = csv.reader(open(r'G:\Samuel\Semester 3\GIS_Programming\Lab1\data\lab1\lab1\Selection3.csv'))
for row in FindCount2:
    text2 = row[2]
print(text2)

#Print of both counts
print("Count where HUC8 = 10190005 is " + text1 + " and " + "Count where HUC8 = 10190006 is " + text2)





