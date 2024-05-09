#Adam Dodds
#Quiz 5

import arcpy

#set the workspace for where the shapefile is located
arcpy.env.workspace = r"C:\Users\Adam\Desktop\airports"

#Adding a new field BUFFER to the airports shapefile where I will add the buffer distances
arcpy.management.AddField('airports.shp', 'BUFFER', 'integer')

#input the shapefile
input_fc = 'airports.shp'
#List the fields that will be used in the UpdateCursor
fields = ["FEATURE", "TOT_ENP", "BUFFER"]

#using the update cursor to create the buffer distances based on the feature type(FEATURE), and activity level (TOT_ENP)
with arcpy.da.UpdateCursor(input_fc, fields) as cursor:
    for row in cursor:
        feature = row[0]
        tot_enp = row[1]
        
        #setting the buffer distance based on the feature type and total enplanments
        if feature == "Airport":
            #check if enplanments exceed 10,000 for airports
            if tot_enp > 10000:
                row[2] = 15000
            else:
                #if below the 10,000 enplanements, creates a 10,000 meter buffer
                row[2] = 10000
        elif feature == "Seaplane Base":
            #check if enplanments exceed 1,000 for seaplane base
            if tot_enp > 1000:
                row[2] = 7500
            else:
                #here it wont create a buffer for seaplane bases with minimal activity (less than 1,000)
                row[2] = 0
        else:
            row[2] = 0
            #update the row with the new buffer distance values
        cursor.updateRow(row)

#create the buffers and export as a new shapefile
arcpy.Buffer_analysis(input_fc, r"C:\Users\Adam\Desktop\airports\buffer_airports.shp", "BUFFER")
