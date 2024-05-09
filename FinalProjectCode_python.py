import arcpy

# Set environment
arcpy.env.workspace = "C:/Users/Adam/Desktop/3050_project/3050_Project/3050_Project.gdb"
arcpy.env.overwriteOutput = True

# Define inputs for the service area analysis
network ="https://www.arcgis.com/"
points_layer = "AccessPoints"
output_folder = "C:/Users/Adam/Desktop/3050_project/3050_Project/3050_Project.gdb"

# Create a feature layer from the access points
arcpy.MakeFeatureLayer_management(points_layer, "points_lyr")

# Create a service area layer for 5 minute walking distance
output_5min = output_folder + "/5min_Walk.shp"
arcpy.na.MakeServiceAreaAnalysisLayer(network, "ServiceArea_5min", "Walking Time", "FROM_FACILITIES", [5], None, "LOCAL_TIME_AT_LOCATIONS", "POLYGONS", "STANDARD", "DISSOLVE", "RINGS", "100 Meters", None, None, "SKIP")

# Add the points layer to the service area layer
arcpy.na.AddLocations("ServiceArea_5min", "Facilities", "points_lyr", "Name OBJECTID #;CurbApproach # 0;Attr_Minutes # 0;Attr_TravelTime # 0;Attr_Miles # 0;Attr_Kilometers # 0;Attr_TimeAt1KPH # 0;Attr_WalkTime # 0;Attr_TruckMinutes # 0;Attr_TruckTravelTime # 0;Breaks_Minutes # #;Breaks_TravelTime # #;Breaks_Miles # #;Breaks_Kilometers # #;Breaks_TimeAt1KPH # #;Breaks_WalkTime # #;Breaks_TruckMinutes # #;Breaks_TruckTravelTime # #", "200 Meters", None, "main.Routing_Streets SHAPE", "MATCH_TO_CLOSEST", "APPEND", "NO_SNAP", "5 Meters", "EXCLUDE", None, "ALLOW")

# Solve the service area layer for 5 minute distance
arcpy.na.Solve("ServiceArea_5min")

#define the inputs for 5 minute walk intersect
in_features=r"MuscatineBlocks #;ServiceArea_5min\Polygons #"
out_feature_class=r"C:\Users\Adam\Desktop\3050_project\3050_Project\3050_Project.gdb\Blocks_Intersect_5min"
join_attributes="ALL"
cluster_tolerance=None
output_type="INPUT"

arcpy.analysis.Intersect(in_features, out_feature_class, join_attributes, cluster_tolerance, output_type)

#defines the inputs for 5 minute walk disolve
#statistics field creates the average percent white for whole boundary
in_features="Blocks_Intersect_5min"
out_feature_class=r"C:\Users\Adam\Desktop\3050_project\3050_Project\3050_Project.gdb\Blocks_Dissolve_5min"
dissolve_field=None
statistics_fields="PCT_P0020005 MEAN"
multi_part="MULTI_PART"
unsplit_lines="DISSOLVE_LINES"
concatenation_separator=""

arcpy.management.Dissolve(in_features, out_feature_class, dissolve_field, statistics_fields, multi_part, unsplit_lines, concatenation_separator)

#defines inputs for the 10 minute walking distance service area analysis
network ="https://www.arcgis.com/"
points_layer = "AccessPoints"
output_folder = "C:/Users/Adam/Desktop/3050_project/3050_Project/3050_Project.gdb"
# Create the service area layer
output_10min = output_folder + "/10min_Walk.shp"
arcpy.na.MakeServiceAreaAnalysisLayer(network, "ServiceArea_10min", "Walking Time", "FROM_FACILITIES", [10], None, "LOCAL_TIME_AT_LOCATIONS", "POLYGONS", "STANDARD", "DISSOLVE", "RINGS", "100 Meters", None, None, "SKIP")

#add the points to the layer
arcpy.na.AddLocations("ServiceArea_10min", "Facilities", "points_lyr", "Name OBJECTID #;CurbApproach # 0;Attr_Minutes # 0;Attr_TravelTime # 0;Attr_Miles # 0;Attr_Kilometers # 0;Attr_TimeAt1KPH # 0;Attr_WalkTime # 0;Attr_TruckMinutes # 0;Attr_TruckTravelTime # 0;Breaks_Minutes # #;Breaks_TravelTime # #;Breaks_Miles # #;Breaks_Kilometers # #;Breaks_TimeAt1KPH # #;Breaks_WalkTime # #;Breaks_TruckMinutes # #;Breaks_TruckTravelTime # #", "200 Meters", None, "main.Routing_Streets SHAPE", "MATCH_TO_CLOSEST", "APPEND", "NO_SNAP", "5 Meters", "EXCLUDE", None, "ALLOW")

#solve the service area layer for 10 mintue walking distance
arcpy.na.Solve("ServiceArea_10min")

#define the inputs for 10 minute walk intersect to select only blocks within
in_features=r"MuscatineBlocks #;ServiceArea_10min\Polygons #"
out_feature_class=r"C:\Users\Adam\Desktop\3050_project\3050_Project\3050_Project.gdb\Blocks_Intersect_10min"
join_attributes="ALL"
cluster_tolerance=None
output_type="INPUT"

arcpy.analysis.Intersect(in_features, out_feature_class, join_attributes, cluster_tolerance, output_type)

#defines the inputs for 10 minute walk disolve
#statistics field creates the average percent white for whole boundary
in_features="Blocks_Intersect_10min"
out_feature_class=r"C:\Users\Adam\Desktop\3050_project\3050_Project\3050_Project.gdb\Blocks_Dissolve_10min"
dissolve_field=None
statistics_fields="PCT_P0020005 MEAN"
multi_part="MULTI_PART"
unsplit_lines="DISSOLVE_LINES"
concatenation_separator=""

arcpy.management.Dissolve(in_features, out_feature_class, dissolve_field, statistics_fields, multi_part, unsplit_lines, concatenation_separator)

#selecting the blocks within the 10 minute walking distance
in_layer="MuscatineBlocks"
overlap_type="INTERSECT"
select_features="Blocks_Intersect_10min"
search_distance=None
selection_type="NEW_SELECTION"
invert_spatial_relationship="NOT_INVERT"

arcpy.management.SelectLayerByLocation(in_layer, overlap_type, select_features, search_distance, selection_type, invert_spatial_relationship)

#uses the 'switch_selection' to selecet the blocks outside of the 10 minute walking distance
in_layer="MuscatineBlocks"
overlap_type="INTERSECT"
select_features="Blocks_Intersect_10min"
search_distance=None
selection_type="SWITCH_SELECTION"
invert_spatial_relationship="NOT_INVERT"

arcpy.management.SelectLayerByLocation(in_layer, overlap_type, select_features, search_distance, selection_type, invert_spatial_relationship)

#turns the selection into its own layer
arcpy.CopyFeatures_management("MuscatineBlocks", "Blocks_Inverse")

#disolves the blocks outside of the walking distance
#uses the statistics field to generate the average percent white for the whole area
in_features="Blocks_Inverse"
out_feature_class=r"C:\Users\Adam\Desktop\3050_project\3050_Project\3050_Project.gdb\Inverse_Dissolve"
dissolve_field=None
statistics_fields="PCT_P0020005 MEAN"
multi_part="MULTI_PART"
unsplit_lines="DISSOLVE_LINES"
concatenation_separator=""

arcpy.management.Dissolve(in_features, out_feature_class, dissolve_field, statistics_fields, multi_part, unsplit_lines, concatenation_separator)

#merge the 3 layers into one
inputs="Inverse_Dissolve;Blocks_Dissolve_10min;Blocks_Dissolve_5min"
output=r"C:\Users\Adam\Desktop\3050_project\3050_Project\3050_Project.gdb\Layers_Merge"
field_mappings='MEAN_PCT_P0020005 "MEAN_PCT_P0020005" true true false 8 Double 0 0,First,#,Inverse_Dissolve,MEAN_PCT_P0020005,-1,-1,Blocks_Dissolve_10min,MEAN_PCT_P0020005,-1,-1,Blocks_Dissolve_5min,MEAN_PCT_P0020005,-1,-1;Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,Inverse_Dissolve,Shape_Length,-1,-1,Blocks_Dissolve_10min,Shape_Length,-1,-1,Blocks_Dissolve_5min,Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,Inverse_Dissolve,Shape_Area,-1,-1,Blocks_Dissolve_10min,Shape_Area,-1,-1,Blocks_Dissolve_5min,Shape_Area,-1,-1'
add_source="NO_SOURCE_INFO"

arcpy.management.Merge(inputs, output, field_mappings, add_source)

#creates a bar chart for percent white at the 3 different boundaries
aprx = arcpy.mp.ArcGISProject("current")
map = aprx.listMaps()[0]
censusLayer = map.listLayers('Layers_Merge')[0]
chart = arcpy.Chart('MyChart')

chart.type = 'bar'
chart.title = 'Mean Percent White within Boundary Distances'
chart.description = ''
chart.xAxis.field = 'OBJECTID'
chart.yAxis.field = 'MEAN_PCT_P0020005'
chart.xAxis.title = 'Boundary'
chart.yAxis.title = 'Mean Percent White'
chart.addToLayer(censusLayer)

#interset tool for 5 minute walking distance and residential parcels
in_features=r"Residential_Parcels #;ServiceArea_5min\Polygons #"
out_feature_class=r"C:\Users\Adam\Desktop\3050_project\3050_Project\3050_Project.gdb\Parcels_Intersect_5min"
join_attributes="ALL"
cluster_tolerance=None
output_type="INPUT"

arcpy.analysis.Intersect(in_features, out_feature_class, join_attributes, cluster_tolerance, output_type)

#interset tool for 10 minute walking distance and residential parcels
in_features=r"Residential_Parcels #;ServiceArea_10min\Polygons #"
out_feature_class=r"C:\Users\Adam\Desktop\3050_project\3050_Project\3050_Project.gdb\Parcels_Intersect_10min"
join_attributes="ALL"
cluster_tolerance=None
output_type="INPUT"

arcpy.analysis.Intersect(in_features, out_feature_class, join_attributes, cluster_tolerance, output_type)

# 5 mintue parcel dissolve
#statistics field creates the average parcel value for whole boundary
in_features="Parcels_Intersect_5min"
out_feature_class=r"C:\Users\Adam\Desktop\3050_project\3050_Project\3050_Project.gdb\Parcels_Dissolve_5min"
dissolve_field=None
statistics_fields="NetValue MEAN"
multi_part="MULTI_PART"
unsplit_lines="DISSOLVE_LINES"
concatenation_separator=""

arcpy.management.Dissolve(in_features, out_feature_class, dissolve_field, statistics_fields, multi_part, unsplit_lines, concatenation_separator)

#10 minute parcel disolve
#statistics field creates the average parcel value for whole boundary
in_features="Parcels_Intersect_10min"
out_feature_class=r"C:\Users\Adam\Desktop\3050_project\3050_Project\3050_Project.gdb\Parcels_Dissolve_10min"
dissolve_field=None
statistics_fields="NetValue MEAN"
multi_part="MULTI_PART"
unsplit_lines="DISSOLVE_LINES"
concatenation_separator=""

arcpy.management.Dissolve(in_features, out_feature_class, dissolve_field, statistics_fields, multi_part, unsplit_lines, concatenation_separator)

#selecting the parcels within the 10 minute walking distance
in_layer="Residential_Parcels"
overlap_type="INTERSECT"
select_features="Parcels_Intersect_10min"
search_distance=None
selection_type="NEW_SELECTION"
invert_spatial_relationship="NOT_INVERT"

arcpy.management.SelectLayerByLocation(in_layer, overlap_type, select_features, search_distance, selection_type, invert_spatial_relationship)

#uses the 'switch_selection' to selecet the parcels outside of the 10 minute walking distance
in_layer="Residential_Parcels"
overlap_type="INTERSECT"
select_features="Parcels_Intersect_10min"
search_distance=None
selection_type="SWITCH_SELECTION"
invert_spatial_relationship="NOT_INVERT"

arcpy.management.SelectLayerByLocation(in_layer, overlap_type, select_features, search_distance, selection_type, invert_spatial_relationship)

#turns the selection into its own layer
arcpy.CopyFeatures_management("Residential_Parcels", "Parcels_Inverse")

#dissolves parcels into single polygon with average parcel value
in_features="Parcels_Inverse"
out_feature_class=r"C:\Users\Adam\Desktop\3050_project\3050_Project\3050_Project.gdb\Parcels_Inverse_Dissolve"
dissolve_field=None
statistics_fields="NetValue MEAN"
multi_part="MULTI_PART"
unsplit_lines="DISSOLVE_LINES"
concatenation_separator=""

arcpy.management.Dissolve(in_features, out_feature_class, dissolve_field, statistics_fields, multi_part, unsplit_lines, concatenation_separator)

#merge the 3 parcel boundary layers into one
inputs="Parcels_Inverse_Dissolve;Parcels_Dissolve_10min;Parcels_Dissolve_5min"
output=r"C:\Users\Adam\Desktop\3050_project\3050_Project\3050_Project.gdb\Parcels_Layers_Merge"
field_mappings='MEAN_NetValue "MEAN_NetValue" true true false 8 Double 0 0,First,#,Parcels_Inverse_Dissolve,MEAN_NetValue,-1,-1,Parcels_Dissolve_10min,MEAN_NetValue,-1,-1,Parcels_Dissolve_5min,MEAN_NetValue,-1,-1;Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,Parcels_Inverse_Dissolve,Shape_Length,-1,-1,Parcels_Dissolve_10min,Shape_Length,-1,-1,Parcels_Dissolve_5min,Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,Parcels_Inverse_Dissolve,Shape_Area,-1,-1,Parcels_Dissolve_10min,Shape_Area,-1,-1,Parcels_Dissolve_5min,Shape_Area,-1,-1'
add_source="NO_SOURCE_INFO"

arcpy.management.Merge(inputs, output, field_mappings, add_source)

#chart for parcel values
#creates a bar chart for parcel values at the 3 different boundaries
aprx = arcpy.mp.ArcGISProject("current")
map = aprx.listMaps()[0]
censusLayer = map.listLayers('Parcels_Layers_Merge')[0]
chart = arcpy.Chart('MyChart')

chart.type = 'bar'
chart.title = 'Mean Parcel Value within Boundary Distances'
chart.description = ''
chart.xAxis.field = 'OBJECTID'
chart.yAxis.field = 'MEAN_NetValue'
chart.xAxis.title = 'Boundary'
chart.yAxis.title = 'Mean Parcel Value'
chart.addToLayer(censusLayer)


