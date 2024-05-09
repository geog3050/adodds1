###################################################################### 
# Edit the following function definition, replacing the words
# 'name' with your name and 'hawkid' with your hawkid.
# 
# Note: Your hawkid is the login name you use to access ICON, and not
# your firsname-lastname@uiowa.edu email address.
# 
# def hawkid():
#     return(["Caglar Koylu", "ckoylu"])
###################################################################### 
def hawkid():
    return(["Adam Dodds", "adodds1"])

###################################################################### 
# Problem 1: 20 Points
#
# Given a csv file import it into the database passed as in the second parameter
# Each parameter is described below:

# csvFile: The absolute path of the file should be included (e.g., C:/users/ckoylu/test.csv)
# geodatabase: The workspace geodatabase
###################################################################### 
def importCSVIntoGeodatabase(csvFile, geodatabase):
    arcpy.env.workspace = geodatabase
    
    #Create a table name for the CSV file
    tableName = arcpy.ValidateTableName(arcpy.os.path.basename(csvFile))
    
    #Define the full path for the output table
    outputTable = arcpy.management.CreateTable(geodatabase, tableName)
    
    #Use the Table to Table tool to import the CSV file into the geodatabase
    arcpy.conversion.TableToTable(csvFile, geodatabase, tableName)
    
    print("CSV file imported into the geodatabase.")

csvFile = r"C:\Users\Adam\Desktop\3050_Assignment_3\yearly.csv"
geodatabase = r"C:\Users\Adam\Desktop\3050_Assignment_3\weather.gdb"
importCSVIntoGeodatabase(csvFile, geodatabase)    

##################################################################################################### 
# Problem 2: 80 Points Total
#
# Given a csv table with point coordinates, this function should create an interpolated
# raster surface, clip it by a polygon shapefile boundary, and generate an isarithmic map

# You can organize your code using multiple functions. For example,
# you can first do the interpolation, then clip then equal interval classification
# to generate an isarithmic map

# Each parameter is described below:

# inTable: The name of the table that contain point observations for interpolation       
# valueField: The name of the field to be used in interpolation
# xField: The field that contains the longitude values
# yField: The field that contains the latitude values
# inClipFc: The input feature class for clipping the interpolated raster
# workspace: The geodatabase workspace

# Below are suggested steps for your program. More code may be needed for exception handling
#    and checking the accuracy of the input values.

# 1- Do not hardcode any parameters or filenames in your code.
#    Name your parameters and output files based on inputs. For example,
#    interpolated raster can be named after the field value field name 
# 2- You can assume the input table should have the coordinates in latitude and longitude (WGS84)
# 3- Generate an input feature later using inTable
# 4- Convert the projection of the input feature layer
#    to match the coordinate system of the clip feature class. Do not clip the features yet.
# 5- Check and enable the spatial analyst extension for kriging
# 6- Use KrigingModelOrdinary function and interpolate the projected feature class
#    that was created from the point feature layer.
# 7- Clip the interpolated kriging raster, and delete the original kriging result
#    after successful clipping. 
#################################################################################################################### 

#wont run correctly as a function, using the code below in an arc notebook it runs and works.
#also each line needs to be in a seperate cell to run 1 cell at a time
#def krigingFromPointCSV(inTable, valueField, xField, yField, inClipFc, workspace = "assignment3.gdb"):
#def krigingFromPointCSV(geodatabase, xField, yField, valueField):

import arcpy
from arcpy.sa import *

#set the workspace
arcpy.env.workspace = geodatabase
geodatabase = r"C:\Users\Adam\Desktop\3050_Assignment_3\weather.gdb"

#lists all the feature classes and tables in the workspace, can print(fcList)or (tbList) to make sure they are all there
fcList = arcpy.ListFeatureClasses()
tbList = arcpy.ListTables()
#selectes the first table from the list
yearly_table = tbList[0]

#defines the xField and yField for the table to point tool
xField = "Longitude"
yField = "Latitude"

#this takes the selected table and converts it to a point feature class using the Longitude and Latitude fields that is defined above
#also uses NAD 1983 as the spatial reference
arcpy.management.XYTableToPoint(yearly_table, "yearly_points", xField, yField, "#", arcpy.SpatialReference("NAD 1983"))

#here we define the valuefield, selecting the row we want to use from the yearly_csv table
valueField = "F2018_PREC"

#runs the Kriging interpolation using the points we created with the attached values (f2018_prec) from the table
outKrig = Kriging("yearly_points", valueField, KrigingModelOrdinary("SPHERICAL"))

#saves the result of the Kiriging interpolation
outKrig.save("kriging_result")
    
#here is where you wold put the shapefile that you want to clip the raster down to, but we only have the points so it clips it at the same extent
rectangle = "yearly_points"

#clipping tool, saves it as clipped_raster
arcpy.management.Clip("kriging_result", rectangle, "clipped_raster")


#krigingFromPointCSV(geodatabase, xField, yField, valueField)

######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
