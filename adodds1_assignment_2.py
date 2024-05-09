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
# Problem 1 (10 Points)
#
# This function reads all the feature classes in a workspace (folder or geodatabase) and
# prints the name of each feature class and the geometry type of that feature class in the following format:
# 'states is a point feature class'

######################################################################

def printFeatureClassNames(workspace):
#imports arcpy
    import arcpy
#sets the workspace
    arcpy.env.workspace = workspace
#this will get a list of all the feature classes in the workspace
    fcList = arcpy.ListFeatureClasses()
#this code will iterate over each feature class in the list
    for fc in fcList:
        #describe will get the description of objects
            desc = arcpy.Describe(fc)
        #this will get the shape type (polygon, polyline, point) of the feature class
            geometry_type = desc.shapeType
            #this will print the name of the feature class (fc) and its geometry type (geometry_type)
            print('{} is a {} feature class'.format(fc, geometry_type))

#printFeatureClassNames("C:/Users/Adam/Desktop/hw2.gdb")


###################################################################### 
# Problem 2 (20 Points)
#
# This function reads all the attribute names in a feature class or shape file and
# prints the name of each attribute name and its type (e.g., integer, float, double)
# only if it is a numerical type

###################################################################### 
def printNumericalFieldNames(inputFc, workspace):
    import arcpy
#sets the workspace
    arcpy.env.workspace = workspace
#gets a list of all fields in the input feature class
    fieldlist = arcpy.ListFields(inputFc)
#iterate over each field
    for field in fieldlist:
        #this will check to see if the feild type is numberical (integer, float, double)
         if field.type == 'Integer' or field.type == 'Float' or field.type == 'Double':
             #if it is numerical, it will print the field name and its type
             print("{} has a type of {}".format(field.name, field.type))
        


###################################################################### 
# Problem 3 (30 Points)
#
# Given a geodatabase with feature classes, and shape type (point, line or polygon) and an output geodatabase:
# this function creates a new geodatabase and copying only the feature classes with the given shape type into the new geodatabase

###################################################################### 
def exportFeatureClassesByShapeType(input_geodatabase, shapeType, output_geodatabase):
    import arcpy
    import os
#sets the workspace to the input database
    arcpy.env.workspace = input_geodatabase
#creates a new geodatabase using the name of the shape type input
    new_gdb = arcpy.CreateFileGDB_management(output.geodatabase, f"{shapeType}")
#lists all the feature classes from the input geodatabase
    fc_list = arcpy.ListFeatureClasses()
#iterate over each feature class
    for shapefile in fc_list:
    #this code uses Describe to get the shape type from the feature class
        desc = arcpy.Describe(shapefile)
    #check to see if the shape type matches the specified input shape type
        if desc.shapeType == shapeType:
            #this code defines the output path to the new geodatabase
            out_featureclass = os.path.join(new_gdb, os.path.splitext(shapefile)[0])
            #copys the feature class to the new geodatabase
            arcpy.management.CopyFeatures(shapefile, out_featureclass)


###################################################################### 
# Problem 4 (40 Points)
#
# Given an input feature class or a shape file and a table in a geodatabase or a folder workspace,
# join the table to the feature class using one-to-one and export to a new feature class.
# Print the results of the joined output to show how many records matched and unmatched in the join operation. 

###################################################################### 
def joinAndExportFeatures(inputFc, idFieldInputFc, inputTable, idFieldTable, workspace):
    import arcpy
    # Set the workspace 
    arcpy.env.workspace = workspace
    
    try:
        #Describe the input feature class
        fc_desc = arcpy.Describe(inputFc)
        #here we get the count of feautes in the input feature class before the join
        start_count = int(arcpy.GetCount_management(inputFc).getOutput(0))
        #Add a join to the input feature class from the given specified fields
        joined_fc = arcpy.AddJoin_management(inputFc, idFieldInputFc, inputTable, idFieldTable)
        #This defines the name for the output feature class
        output_fc_name = f"{fc_desc.baseName}_joined"
        #export the joined output to a new feature class
        output_fc = arcpy.conversion.FeatureClassToFeatureClass(joined_fc, workspace, output_fc_name)
        #this gets the count of features in the joined output
        joined_count = int(arcpy.GetCount_management(output_fc).getOutput(0))
        
        #define and calculate the number of matched and unmatched records
        matched_count = joined_count
        unmatched_count = start_count - matched_count
        
        #Prints the number of recrods that were matched in the join operation
        print(f"Matched records: {matched_count}")
        #Prints the number of recrods that could not be matched in the join operation
        print(f"Unmatched records: {unmatched_count}")
    #handles exceptions that occur 
    except arcpy.ExecuteError:
        print("An error occurred.")

######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
