# ---------------------------------------------------------------------------
# reduce-size.py
# Created on: 2017-08-26  
# Description: 
# This tool is used to reduce the size of road network shapefile to ease processing time
# ---------------------------------------------------------------------------

# Set the necessary product code
# import arcinfo


# Import arcpy module
import arcpy
import math
from arcpy import env
from arcpy.sa import *

arcpy.env.Workspace='S:\\Action Items\\Laban\\Debug.gdb'
#arcpy.env.Workspace='S:\\Action Items\\Laban\\February 2017\\Output Workspace'
arcpy.env.overwriteOutput = True
#------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------
# Script arguments

#Take input road network file and other user generated parameters

#Input road network
input_Road_Network = arcpy.GetParameterAsText(0)

#Road Name Field
road_Name = arcpy.GetParameterAsText(1)

#Field name for the iri field
iri_field = arcpy.GetParameterAsText(2)

#User defined seperation distance or percentage
interval = arcpy.GetParameterAsText(3)

#Output workspace
output_Workspace = arcpy.GetParameterAsText(4)

#Output road network reduced in size
output_Road_Network = arcpy.GetParameterAsText(5)


arcpy.AddMessage('Reprojecting ...')
# create a spatial reference object for the output coordinate system
out_coordinate_system = arcpy.SpatialReference(3857)

# run the project tool
arcpy.Project_management(input_Road_Network, output_Workspace+"\\roads_projected.shp", out_coordinate_system)



# Set local variables
inFeatures = output_Workspace+"\\roads_projected.shp"

dissolveFields = [road_Name]

outFeatureClass = output_Workspace+"\\roads_dissolved.shp"


arcpy.AddMessage('Dissolving based on the road name ...')
arcpy.Dissolve_management(inFeatures, outFeatureClass, dissolveFields, "", 
                          "SINGLE_PART", "DISSOLVE_LINES")

						  
						  
##create points along line to signify locations of splitting the line, at the indicated intervals as percentage#

desc = arcpy.Describe(output_Workspace+"\\roads_projected.shp")

 # Create output feature class
 
arcpy.AddMessage('Beginning to divide the line based on the defined interval ...')
arcpy.CreateFeatureclass_management(
            output_Workspace,
            "pointsOnLine.shp",
            "POINT", 
			"", "", "",
			#"roads_projected.shp"
            desc.spatialReference
			)

        # Add a field to transfer FID from input
fid_name = "FID_1"
end_points = 1

#arcpy.AddMessage(int(interval))

#interval = 250

arcpy.AddField_management(output_Workspace+"\\pointsOnLine.shp", fid_name, "LONG")


arcpy.AddMessage('Creating splitting vertices ...')

        # Create new points based on input lines
with arcpy.da.SearchCursor(
                output_Workspace+"\\roads_dissolved.shp", ['SHAPE@', desc.OIDFieldName]) as search_cursor:
            with arcpy.da.InsertCursor(
                    output_Workspace+"\\pointsOnLine.shp", ['SHAPE@', fid_name]) as insert_cursor:
                for row in search_cursor:
                    line = row[0]

                    if line:  # if null geometry--skip
                        #if end_points:
                        #    insert_cursor.insertRow([line.firstPoint, row[1]])

                        cur_length = int(interval)

                        max_position = line.length
                        #if not use_percentage:
                            #max_position = line.length

                        while cur_length < max_position:
                            insert_cursor.insertRow(
                                [line.positionAlongLine(
                                    cur_length, False), row[1]])
                            #cur_length += interval
                            cur_length = int(cur_length) + int(interval)

                        #if end_points:
                        #    insert_cursor.insertRow(
                        #        [line.positionAlongLine(line.length, False), row[1]])
								

								
						
##Split line at these junctions (using points above as reference)

arcpy.AddMessage('Splitting the line ...')

arcpy.SplitLineAtPoint_management(output_Workspace+"\\roads_dissolved.shp",output_Workspace+"\\pointsOnLine.shp",output_Workspace+"\\splitline_out.shp","")




arcpy.AddMessage('Performing spatial join ...')
#Perform the spatial join

# Want to join 100 meter road network to the compressed network and calculate the mean iri
# for each state
targetFeatures = output_Workspace+"\\splitline_out.shp"
joinFeatures = output_Workspace+"\\roads_projected.shp"
 
# Output will be the target features, road network, with a mean average iri field 
#outfc = output_Workspace+"\\roads_compressed.shp"

outfc = output_Road_Network
 
# Create a new fieldmappings and add the two input feature classes.
fieldmappings = arcpy.FieldMappings()
fieldmappings.addTable(targetFeatures)
fieldmappings.addTable(joinFeatures)
 
# First get the POP1990 fieldmap. POP1990 is a field in the cities feature class.
# The output will have the states with the attributes of the cities. Setting the
# field's merge rule to mean will aggregate the values for all of the cities for
# each state into an average value. The field is also renamed to be more appropriate
# for the output.
iriFieldIndex = fieldmappings.findFieldMapIndex( str(iri_field) )
fieldmap = fieldmappings.getFieldMap(iriFieldIndex)
 
# Get the output field's properties as a field object
field = fieldmap.outputField
 
# Rename the field and pass the updated field object back into the field map
field.name = "mean_iri"
field.aliasName = "Average IRI"
fieldmap.outputField = field
 
# Set the merge rule to mean and then replace the old fieldmap in the mappings object
# with the updated one
fieldmap.mergeRule = "mean"
fieldmappings.replaceFieldMap(iriFieldIndex, fieldmap)
 
# Delete fields that are no longer applicable, such as city CITY_NAME and CITY_FIPS
# as only the first value will be used by default
#x = fieldmappings.findFieldMapIndex("CITY_NAME")
#fieldmappings.removeFieldMap(x)
#y = fieldmappings.findFieldMapIndex("CITY_FIPS")
#fieldmappings.removeFieldMap(y)
 
#Run the Spatial Join tool, using the defaults for the join operation and join type
arcpy.SpatialJoin_analysis(targetFeatures, joinFeatures, outfc, "JOIN_ONE_TO_ONE", "KEEP_COMMON", fieldmappings)

### outfc saved at output_Workspace+"\\roads_compressed.shp" ###







