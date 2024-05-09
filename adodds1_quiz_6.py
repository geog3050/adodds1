#Adam Dodds
#Quiz 6

import arcpy

def calculatePercentAreaOfPolygonAInPolygonB(input_geodatabase, fcPolygonA, fcPolygonB, idFieldPolygonB):
    #sets the workspace
    arcpy.env.workspace = input_geodatabase
    
    #Adding a new field to fcPolygonB where i'll store the percentage area
    arcpy.AddField_management(fcPolygonB, "Percent_Area", "DOUBLE")
    
    #Used a spatial join to intersect features and calculate intersection area
    #Using the 'in_memory' makes it so the output will be store in the memory so it is temporary to the data and does not save it to a file output
                #but could be changed to output a file instead by specifying a file path
    intersect_output = arcpy.analysis.Intersect([fcPolygonA, fcPolygonB], "in_memory/intersection")
    
    #Calculate the total area of fcPolygonA for each fcPolygonB feature
    #Dictionary to store total areas of intersected Polygon B features based on their IDs
    total_areas = {}
    #Here it uses a search cursor to iterate through the intersected features and calculates the total areas
    with arcpy.da.SearchCursor(intersect_output, [idFieldPolygonB, 'Shape_Area']) as cursor:
        for row in cursor:
            if row[0] not in total_areas:
                total_areas[row[0]] = 0
            total_areas[row[0]] += row[1]
    
    #Calculates the percentage and updates fcPolygonB
    #Uses an update cursor to calculate and update the percentage area for each feature
    with arcpy.da.UpdateCursor(fcPolygonB, [idFieldPolygonB, 'SHAPE_AREA', 'Percent_Area']) as cursor:
        for row in cursor:
            #gets the total area of intersected feautres with the same ID from the dictionary
            total_area = total_areas.get(row[0], 0)
            if total_area > 0:
                #calculates the percentage area
                percent_area = (total_area / row[1]) * 100
                #updates the 'Percent_Area' field with the percentage that was calculated
                row[2] = percent_area
                cursor.updateRow(row)
            else:
                #if the total area is 0, this will set the percentage to 0
                row[2] = 0
                cursor.updateRow(row)

#the code below is used to define the input parameters
input_geodatabase = r'C:\Users\Adam\Desktop\Quiz_6\quiz6.gdb'  #Path to the input geodatabase
fcPolygonA = 'parks'  #The name of the first feature class
fcPolygonB = 'block_groups'  #The name of the second  feature class
idFieldPolygonB = 'FIPS'  #This is the ID field in fcPolygonB

#calls the function using the defined parameters above
calculatePercentAreaOfPolygonAInPolygonB(input_geodatabase, fcPolygonA, fcPolygonB, idFieldPolygonB)  # Call the function
