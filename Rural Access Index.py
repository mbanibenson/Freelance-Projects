# ---------------------------------------------------------------------------
# linerepair.py
# Created on: 2017-03-15  
# Description: 
# This tool is used to compute Rural Access Index (RAI) based on a set of population, urban area and roads data
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

#Take input point excel file and other user generated parameters

#Worldpop population raster file
worldPop = arcpy.GetParameterAsText(0)

#GRUMP urban extents
grumpUrbanExtents = arcpy.GetParameterAsText(1)

#Roads layer 
roads = arcpy.GetParameterAsText(2)

#Field from the roads layer indicating the Road Type - Expecting Category
roadTypeField_paved = arcpy.GetParameterAsText(3)

#Value for the road type - Expecting paved
roadTypeValue_paved = arcpy.GetParameterAsText(4)

#Field from the roads layer indicating IRI
iriField_paved = arcpy.GetParameterAsText(5)

#Option for IRI value
iriValueMin_paved = arcpy.GetParameterAsText(6)

#Option for IRI value
iriValueMax_paved = arcpy.GetParameterAsText(7)

#Field from the roads layer indicating road condition
goodRoadConditionField1 = arcpy.GetParameterAsText(8)

#Option for road condition
goodRoadConditionThresholdValue1 = arcpy.GetParameterAsText(9)

#Field from the roads layer indicating road condition
goodRoadConditionField2 = arcpy.GetParameterAsText(10)

#Option for road condition
goodRoadConditionThresholdValue2 = arcpy.GetParameterAsText(11)

#Field from the roads layer indicating road condition
goodRoadConditionField3 = arcpy.GetParameterAsText(12)

#Option for road condition
goodRoadConditionThresholdValue3 = arcpy.GetParameterAsText(13)

#Road Type Field
roadTypeField_unpaved = arcpy.GetParameterAsText(14)

#Road Type Value
roadTypeValue_unpaved = arcpy.GetParameterAsText(15)

#Field from the roads layer indicating IRI
iriField_unpaved = arcpy.GetParameterAsText(16)

#Option for IRI value
iriValueMin_unpaved = arcpy.GetParameterAsText(17)

#Option for IRI value
iriValueMax_unpaved = arcpy.GetParameterAsText(18)

#Field from the roads layer indicating road condition
goodRoadConditionField1_unpaved = arcpy.GetParameterAsText(19)

#Option for road condition
goodRoadConditionThresholdValue1_unpaved = arcpy.GetParameterAsText(20)

#Field from the roads layer indicating road condition
goodRoadConditionField2_unpaved = arcpy.GetParameterAsText(21)

#Option for road condition
goodRoadConditionThresholdValue2_unpaved = arcpy.GetParameterAsText(22)

#Field from the roads layer indicating road condition
goodRoadConditionField3_unpaved = arcpy.GetParameterAsText(23)

#Option for road condition
goodRoadConditionThresholdValue3_unpaved = arcpy.GetParameterAsText(24)

#Roads buffer distance
goodRoadBufferDistance = arcpy.GetParameterAsText(25)

#Administrative boundaries
adminUnitsBoundaries = arcpy.GetParameterAsText(26)

#Unique field to identify the admin boundaries
adminUnitsField = arcpy.GetParameterAsText(27)

#Working folder
projectWorkspace = arcpy.GetParameterAsText(28)

#Final output with RAI attached
Output_RAI_Shapefile = arcpy.GetParameterAsText(29)

#------------------------------------------------------------------------------------
#make copies
roadTypeField_paved_ = roadTypeField_paved
roadTypeField_unpaved_ = roadTypeField_unpaved
goodRoadConditionField1_ = goodRoadConditionField1
goodRoadConditionField2_ = goodRoadConditionField2
goodRoadConditionField3_ = goodRoadConditionField3
goodRoadConditionField1_unpaved_ = goodRoadConditionField1_unpaved
goodRoadConditionField2_unpaved_ = goodRoadConditionField2_unpaved
goodRoadConditionField3_unpaved_ = goodRoadConditionField3_unpaved
  


#---------------------------------------------------------------------------------------------------------
#Build attribute tables for both the WorldPop and GRUMP raster datasets as they are downloaded without any
#arcpy.BuildRasterAttributeTable_management(worldPop, "Overwrite")

arcpy.AddMessage("Building raster attribute tables ...")

#arcpy.Resample_management(grumpUrbanExtents, projectWorkspace+"\\GRUMPRasterResampled.tif", '0.0008333 0.0008333', "NEAREST")

#arcpy.BuildRasterAttributeTable_management(projectWorkspace+"\\GRUMPRasterResampled.tif", "Overwrite")

arcpy.BuildRasterAttributeTable_management(grumpUrbanExtents, "Overwrite")


#---------------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------
#Convert GRUMP raster data to polygon

arcpy.AddMessage("Converting gridded Grump to polygon ...")

#arcpy.RasterToPolygon_conversion(grumpUrbanExtents, projectWorkspace+"\\GRUMPRasToPoly.shp", "SIMPLIFY", "VALUE")

# Set local variables
inRaster = grumpUrbanExtents
outPolygons = projectWorkspace+"\\GRUMPRasToPoly.shp"
field = "VALUE"

# Execute RasterToPolygon
#arcpy.RasterToPolygon_conversion(inRaster, outPolygons, "NO_SIMPLIFY", field)

arcpy.RasterToPolygon_conversion(inRaster, outPolygons)

#----------------------------------------------------------------------------------------------------------



#----------------------------------------------------------------------------------------------------------

#Select only rural polygons

arcpy.AddMessage("Selecting rural polygons and excluding urban ...")

# Set local variables
in_features = projectWorkspace+"\\GRUMPRasToPoly.shp"
out_feature_class = projectWorkspace+"\\GRUMPRasToPolySelected.shp"
where_clause = '"gridcode" = 1'

# Execute Select
arcpy.Select_analysis(in_features, out_feature_class, where_clause)

#Save the selected rural polygons for Q/A
arcpy.CopyFeatures_management(projectWorkspace+"\\GRUMPRasToPolySelected.shp", projectWorkspace+"\\GRUMP_rural.shp")

#----------------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------
# Set local variables
#inFeatures = projectWorkspace+"\\GRUMP_rural.shp"
#valField = "GRIDCODE"
#outRaster = projectWorkspace+"\\GRUMP_rural.tif"
#assignmentType = "MAXIMUM_AREA"
#priorityField = "MALES"
#cellSize = 0.5

# Execute PolygonToRaster
#arcpy.PolygonToRaster_conversion(inFeatures, valField, outRaster, assignmentType)

#----------------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------
#Use urban-only GRUMP polygon to mask out urban area pixels from the worldpop data



#outExtractByMask = ExtractByMask(worldPop, projectWorkspace+"\\GRUMP_rural.shp")
#outExtractByMask.save(projectWorkspace+"\\ruralPopulationRaster.tif")

#----------------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------
#Clip the raster using the grump rural shapefile
arcpy.AddMessage("Masking out urban area pixels from population raster ...")

arcpy.Clip_management(worldPop, "#", projectWorkspace+"\\ruralPopulationRaster.tif", projectWorkspace+"\\GRUMP_rural.shp", "-3.40282346639e+038", "ClippingGeometry")

#----------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------
#Use GRUMP raster to mask out urban area pixels from the worldpop data
#arcpy.AddMessage("Masking out urban area pixels from population raster ...")
#outSetNull = SetNull(grumpUrbanExtents, worldPop, "VALUE = 2")

#outCon2.save(projectWorkspace+"\\ruralPopulationRaster.tif")

# Execute Con using a map algebra expression instead of a where clause
#outCon2 = Con(Raster(projectWorkspace+"\\GRUMPRasterResampled.tif")>1, 0, worldPop)
#outCon2 = Con(Raster(grumpUrbanExtents)>1, 0, worldPop)
#outCon2.save(projectWorkspace+"\\ruralPopulationRaster.tif")



#------------------------------------------------------------------------------------



#------------------------------------------------------------------------------------
#Generate rural population per admin units using zonal statistics
arcpy.AddMessage("Deriving rural population per administrative units ...")

# Set local variables
inZoneData = adminUnitsBoundaries
zoneField = adminUnitsField
inValueRaster = projectWorkspace+"\\ruralPopulationRaster.tif"
outTable = "ruralPopulationPerAdminUnit"

# Execute ZonalStatisticsAsTable
outZSaT = ZonalStatisticsAsTable(inZoneData, zoneField, inValueRaster, outTable, "DATA", "SUM")

ruralPopulationPerAdminUnitSaved = arcpy.TableToExcel_conversion(outTable, projectWorkspace+"\\ruralPopAdminUnit.xls")

if ruralPopulationPerAdminUnitSaved:

    arcpy.AddMessage("Zonal statistics table for two km buffer has been saved in hard drive ...")

#------------------------------------------------------------------------------------



#------------------------------------------------------------------------------------
#Rename the SUM field from the above process to 'Rural Population'
arcpy.AddMessage("Renaming fields accordingly ...")
arcpy.AlterField_management(outTable, 'SUM', 'ruralP', 'Rural Population')

#------------------------------------------------------------------------------------



#--------------------------------------------------------------------------------------------------------
#Filter the roads first using the road type then the other selections shall be based on this layer
#goodRoadTypeValuethreshold = "'" + str(goodRoadTypeValue) +"'"

#where_clause_type = '{} = {}'.format(arcpy.AddFieldDelimiters(roads, goodRoadType), goodRoadTypeValuethreshold)



#goodRdByType = arcpy.Select_analysis(roads, "goodRoadsByType", where_clause_type)

#if roadTypeField_paved and roadTypeValue_paved and iriField_paved and roadTypeField_unpaved and roadTypeValue_unpaved and iriField_unpaved and not (goodRoadConditionThresholdValue1 and goodRoadConditionThresholdValue2 and goodRoadConditionThresholdValue3 and goodRoadConditionThresholdValue1_unpaved and goodRoadConditionThresholdValue2_unpaved and goodRoadConditionThresholdValue3_unpaved):
#  where_clause_CASE_ONE (param1,param2,param3,param4,param5,param6,param7,param8,param9,param10,param11)  

#goodRdByType = arcpy.Select_analysis(roads, "goodRoadsByType", where_clause_SQL)


#---------------------------------------------------------------------------------------------------------



#--------------------------------------------------------------------------------------------------------
#Select good roads, using the user defined threshold
#arcpy.Select_analysis(roads, "goodRoads", '"goodRoadIndicatorField" > 0.8')
#goodRoadIndicatorField '>= ' goodRoadIndicatorThresholdValue

#arcpy.AddMessage("Selecting good roads as per defined threshold ...")
#field_indicator = goodRoadIndicatorField
#minimum_threshold = goodRoadIndicatorThresholdValue # IRI
#condition_field_indicator = goodRoadConditionField
# condition_minimum_threshold = "'" + str(goodRoadConditionThresholdValue) +"'"

def format_string_value(str_value):
    """Takes a double quoted string and returns it single quoted"""
	
    return "'" + str(str_value) +"'"

def gen_where_clause(fclass, field, value):
    """Takes in a parameter and value and returns a string"""
	
    value = format_string_value(value)
    where_clause =  '{} = {}'.format(arcpy.AddFieldDelimiters(fclass, field), value)
    return where_clause
	
	

	
def where_clause_CASE_ONE (param1,param2,param3,param4,param5,param6,param7,param8,param9,param10,param11,param12,param13,param14,param15,param16,param17,param18,param19,param20,param21,param22,param23):
	"""Generate where clause for the set of conditions - Everything supplied including conditions"""
	
	clause_1 = gen_where_clause (param1,param2, param3)#where surface=paved for example
	clause_2 = '{} > {}'.format(arcpy.AddFieldDelimiters(param1, param4), param5)#iri > minimum threshold
	clause_3 = '{} <= {}'.format(arcpy.AddFieldDelimiters(param1, param4), param6)#iri <= maximum threshold
	clause_4 = gen_where_clause (param1,param7, param8)#where surface=unpaved for example
	clause_5 = '{} > {}'.format(arcpy.AddFieldDelimiters(param1, param9), param10)#iri > minimum threshold
	clause_6 = '{} <= {}'.format(arcpy.AddFieldDelimiters(param1, param9), param11)#iri <= maximum threshold
	clause_7 = gen_where_clause (param1,param12, param13)#where condition=excellent for example
	clause_8 = gen_where_clause (param1,param14, param15)#where condition=good for example
	clause_9 = gen_where_clause (param1,param16, param17)#where condition=good for example
	clause_10 = gen_where_clause (param1,param18, param19)#where condition=excellent for example
	clause_11 = gen_where_clause (param1,param20, param21)#where condition=good for example
	clause_12 = gen_where_clause (param1,param22, param23)#where condition=good for example
	
	where_clause_SQL = str(   " ( " + clause_1 + " and " + " ( " + clause_2 + " and " + clause_3 + " ) " + " and " + " ( " + clause_7 + " or " + clause_8 + " or " + clause_9 + " ) ) "  +  " or "  + " ( " + clause_4 + " and " + " ( " + clause_5 + " and " + clause_6 + " ) " + " and " + " ( " + clause_10 + " or " + clause_11 + " or " + clause_12 + " ) ) "    )
	#where_clause_SQL = str(   " ( " + clause_1 + " or " + " ( " + clause_2 + " and " + clause_3 + " ) " + " or " + " ( " + clause_7 + " or " + clause_8 + " or " + clause_9 + " ) ) "  +  " or "  + " ( " + clause_4 + " and " + " ( " + clause_5 + " and " + clause_6 + " ) " + " and " + " ( " + clause_10 + " or " + clause_11 + " or " + clause_12 + " ) ) "    )

	return where_clause_SQL
	

#def setMissingOptionsToNull (iriField_paved,iriValueMin_paved,iriValueMax_paved,roadTypeField_unpaved, roadTypeValue_unpaved,iriField_unpaved,iriValueMin_unpaved,iriValueMax_unpaved,goodRoadConditionField1,goodRoadConditionThresholdValue1,goodRoadConditionField2,goodRoadConditionThresholdValue2,goodRoadConditionField3,goodRoadConditionThresholdValue3,goodRoadConditionField1_unpaved,goodRoadConditionThresholdValue1_unpaved,goodRoadConditionField2_unpaved,goodRoadConditionThresholdValue2_unpaved,goodRoadConditionField3_unpaved,goodRoadConditionThresholdValue3_unpaved,roadTypeField_paved):
def setMissingOptionsToNull ():
	"""Use the above generated where_clause_SQL to make selection"""
	
	global iriField_paved
	global iriValueMin_paved
	global iriValueMax_paved
	global roadTypeField_unpaved
	global roadTypeValue_unpaved
	global iriField_unpaved
	global iriValueMin_unpaved
	global iriValueMax_unpaved
	global goodRoadConditionField1
	global goodRoadConditionThresholdValue1
	global goodRoadConditionField2
	global goodRoadConditionThresholdValue2
	global goodRoadConditionField3
	global goodRoadConditionThresholdValue3
	global goodRoadConditionField1_unpaved
	global goodRoadConditionThresholdValue1_unpaved
	global goodRoadConditionField2_unpaved
	global goodRoadConditionThresholdValue2_unpaved
	global goodRoadConditionField3_unpaved
	global goodRoadConditionThresholdValue3_unpaved
	global roadTypeField_paved 
	
	
	if not iriField_paved:
	
	
		iriField_paved = "FID" #null
		iriValueMin_paved = 100000000 #null
		iriValueMax_paved = 100000000 #null

	if not roadTypeField_unpaved:
		roadTypeField_unpaved = roadTypeField_paved 
		roadTypeValue_unpaved = "NULL"
		
	if not iriField_unpaved:
		iriField_unpaved = "FID" #null
		iriValueMin_unpaved = 100000000 #null
		iriValueMax_unpaved = 100000000 #null	
	
	if not goodRoadConditionField1:
		goodRoadConditionField1 = roadTypeField_paved
		goodRoadConditionThresholdValue1  = "NULL"

	if not goodRoadConditionField2:
		goodRoadConditionField2 = roadTypeField_paved
		goodRoadConditionThresholdValue2  = "NULL"
		
	if not goodRoadConditionField3:
		goodRoadConditionField3 = roadTypeField_paved
		goodRoadConditionThresholdValue3  = "NULL"
		
	if not goodRoadConditionField1_unpaved:
		goodRoadConditionField1_unpaved = roadTypeField_paved
		goodRoadConditionThresholdValue1_unpaved  = "NULL"
		
	if not goodRoadConditionField2_unpaved:
		goodRoadConditionField2_unpaved = roadTypeField_paved
		goodRoadConditionThresholdValue2_unpaved  = "NULL"
		
	if not goodRoadConditionField3_unpaved:
		goodRoadConditionField3_unpaved = roadTypeField_paved
		goodRoadConditionThresholdValue3_unpaved  = "NULL"
		
		



#setMissingOptionsToNull (iriField_paved,iriValueMin_paved,iriValueMax_paved,roadTypeField_unpaved, roadTypeValue_unpaved,iriField_unpaved,iriValueMin_unpaved,iriValueMax_unpaved,goodRoadConditionField1,goodRoadConditionThresholdValue1,goodRoadConditionField2,goodRoadConditionThresholdValue2,goodRoadConditionField3,goodRoadConditionThresholdValue3,goodRoadConditionField1_unpaved,goodRoadConditionThresholdValue1_unpaved,goodRoadConditionField2_unpaved,goodRoadConditionThresholdValue2_unpaved,goodRoadConditionField3_unpaved,goodRoadConditionThresholdValue3_unpaved)	
setMissingOptionsToNull ()

where = where_clause_CASE_ONE(roads ,roadTypeField_paved ,roadTypeValue_paved,iriField_paved,iriValueMin_paved , iriValueMax_paved ,roadTypeField_unpaved, roadTypeValue_unpaved ,iriField_unpaved , iriValueMin_unpaved, iriValueMax_unpaved,goodRoadConditionField1 , goodRoadConditionThresholdValue1 , goodRoadConditionField2 , goodRoadConditionThresholdValue2 ,goodRoadConditionField3, goodRoadConditionThresholdValue3 , goodRoadConditionField1_unpaved , goodRoadConditionThresholdValue1_unpaved ,goodRoadConditionField2_unpaved ,goodRoadConditionThresholdValue2_unpaved ,goodRoadConditionField3_unpaved ,goodRoadConditionThresholdValue3_unpaved )

where_stripped = where.replace('and  ( "FID" > 100000000 and "FID" <= 100000000 )','')

#text = str('and  ( "' + goodRoadConditionField1 + ' = 'NULL' or ' + goodRoadConditionField2 +  " = 'NULL' or " + goodRoadConditionField3 + " = 'NULL' )")
if not goodRoadConditionField1_:
	goodRoadConditionField1 = '"' + str(goodRoadConditionField1) + '"'
	
if not goodRoadConditionField2_:
	goodRoadConditionField2 = '"' + str(goodRoadConditionField2) + '"'
	
if not goodRoadConditionField3_:
	goodRoadConditionField3 = '"' + str(goodRoadConditionField3) + '"'
	
if not roadTypeField_unpaved_:
	roadTypeField_unpaved = '"' + str(roadTypeField_unpaved) + '"'
	
else:
	roadTypeField_unpaved = '"' + str(roadTypeField_unpaved_) + '"'

text = str("and  ( " +goodRoadConditionField1+" = 'NULL' or "+goodRoadConditionField2+" = 'NULL' or "+goodRoadConditionField3+" = 'NULL' )" )

where_stripped_1 = where_stripped.replace(text,"")

where_stripped_2 = where_stripped_1.replace('and  ( "FID" > 200000000 and "FID" <= 200000000 )','')

text_1 = str("or  ( "+roadTypeField_unpaved+" = 'NULL'    )")

where_stripped_3 = where_stripped_2.replace(text_1,"")

#and  ( "is_fixed" = 'NULL' or "is_fixed" = 'NULL' or "is_fixed" = 'NULL' )
if not goodRoadConditionField1_unpaved_:
	goodRoadConditionField1_unpaved  =  '"' +str(goodRoadConditionField1_unpaved)+ '"'
else:
	goodRoadConditionField1_unpaved  =  '"' +str(goodRoadConditionField1_unpaved_)+ '"'
	
if not goodRoadConditionField2_unpaved_:
	goodRoadConditionField2_unpaved  =  '"' +str(goodRoadConditionField2_unpaved)+ '"'
	
else:
	goodRoadConditionField2_unpaved  =  '"' +str(goodRoadConditionField2_unpaved_)+ '"'
	
if not goodRoadConditionField3_unpaved_:
	goodRoadConditionField3_unpaved  =  '"' +str(goodRoadConditionField3_unpaved)+ '"'
else:
	goodRoadConditionField3_unpaved  =  '"' +str(goodRoadConditionField3_unpaved_)+ '"'

text_2 = "and  ( "+goodRoadConditionField1_unpaved+" = 'NULL' or "+goodRoadConditionField2_unpaved+" = 'NULL' or "+goodRoadConditionField3_unpaved+" = 'NULL' )"

where_stripped_4 = where_stripped_3.replace(text_2,"")


text_3 = "or "+roadTypeField_unpaved+" = 'NULL'"

where_stripped_5 = where_stripped_4.replace(text_3,"")

text_4 = roadTypeField_unpaved+" = 'NULL' or"

#"is_fixed" = 'NULL'  or
#"is_fixed" = 'false'   and

where_stripped_6 = where_stripped_5.replace(text_4,"")

text_5 = roadTypeField_unpaved+" = 'NULL' and"


where_stripped_7 = where_stripped_6.replace(text_5,"")

text_6 = roadTypeField_unpaved+" = 'false'   and"

where_stripped_8 = where_stripped_7.replace(text_6,"")

text_7 = roadTypeField_unpaved+" = 'NULL'  or"

where_stripped_9 = where_stripped_8.replace(text_7,"")

text_8 = "or  ( "+roadTypeField_unpaved+" = 'NULL'    )"

where_stripped_10 = where_stripped_9.replace(text_8,"")


arcpy.AddMessage("Your SQL Statement is: Select roads where " + str(where_stripped_10))

#arcpy.AddMessage("Your replace text is: " + text_5)

#arcpy.AddMessage("Your original SQL Statement was : " + str(where))
#arcpy.AddMessage("Your refined SQL Statement : " + str(where_stripped))
#arcpy.AddMessage("Your refined SQL Statement : " + str(where_stripped_1))
#arcpy.AddMessage("Your refined SQL Statement : " + str(text))
#arcpy.AddMessage("Text 3 : " + str(text_3))

#arcpy.AddMessage('Your replace text is : and  ( "FID" > 100000000 and "FID" <= 100000000 )')

#setMissingOptionsToNull ()
		
goodRdSelect = arcpy.Select_analysis(roads, "goodRoadsByType", where_stripped_10)

if goodRdSelect:

    arcpy.AddMessage("Good roads have been successfully selected ...")

goodRdSaved = arcpy.CopyFeatures_management("goodRoadsByType", projectWorkspace+"\\goodRoadsByType.shp" , "", "0", "0", "0")

if goodRdSaved:

    arcpy.AddMessage("Good roads have been saved in hard drive ...")


#--------------------------------------------------------------------------------------------------------



#---------------------------------------------------------------------------------------------------------------
#Buffer 2km about the selected good roads
arcpy.AddMessage("Buffering good roads selection ...")
arcpy.Buffer_analysis("goodRoadsByType", "goodrdsBuffer", str(goodRoadBufferDistance) + " Kilometers", "FULL", "ROUND", "ALL", "")

goodRdbufferSaved = arcpy.CopyFeatures_management("goodrdsBuffer", projectWorkspace+"\\goodrdsBuffer.shp" , "", "0", "0", "0")

if goodRdbufferSaved:

    arcpy.AddMessage("Buffered Roads have been saved in hard drive ...")

#----------------------------------------------------------------------------------------------------------------



#-----------------------------------------------------------------------------------------------------------------
#Intersect admin boundary with good roads buffer
arcpy.AddMessage("Performing intersections and dissolving ...")
inFeatures = ["goodrdsBuffer", adminUnitsBoundaries]
intersectOutput = "countyandGoodRds"
#clusterTolerance = ""    
arcpy.Intersect_analysis(inFeatures, intersectOutput, "", "", "INPUT")

adminandgdroadsSaved = arcpy.CopyFeatures_management(intersectOutput, projectWorkspace+"\\countyandGoodRds.shp" , "", "0", "0", "0")

if adminandgdroadsSaved:

    arcpy.AddMessage("Buffered Roads plus Admin Units Intersection has been saved in hard drive ...")

#-----------------------------------------------------------------------------------------------------------------



#-----------------------------------------------------------------------------------------------------------------
#Dissolve the above output so as to end up with only one polygon per admin unit
arcpy.Dissolve_management(intersectOutput, "countyandGoodRdsDissolved",[adminUnitsField], "", "", "")

adminandgdroadsDissolvedSaved = arcpy.CopyFeatures_management("countyandGoodRdsDissolved", projectWorkspace+"\\countyandGoodRdsDissolved.shp" , "", "0", "0", "0")

if adminandgdroadsDissolvedSaved:

    arcpy.AddMessage("Buffered Roads plus Admin Units Intersection was Dissolved and has been saved in hard drive ...")
#-----------------------------------------------------------------------------------------------------------------



#------------------------------------------------------------------------------------
#Generate rural population per 2km Buffer generated above using zonal statistics

arcpy.AddMessage("Generating rural population within the 2 Km Buffer(s) ...")

# Set local variables
inZoneData = "countyandGoodRdsDissolved"
zoneField = adminUnitsField
inValueRaster = projectWorkspace+"\\ruralPopulationRaster.tif"
outTable2km = "TwokmBufRuralPop"

# Execute ZonalStatisticsAsTable
ZonalStatisticsAsTable(inZoneData, zoneField, inValueRaster, outTable2km, "DATA", "SUM")


TwoKmBuffRuralPopSaved = arcpy.TableToExcel_conversion(outTable2km, projectWorkspace+"\\TwokmBufRuralPop.xls")

if TwoKmBuffRuralPopSaved:

    arcpy.AddMessage("Zonal statistics table for two km buffer has been saved in hard drive ...")

#------------------------------------------------------------------------------------



#------------------------------------------------------------------------------------
#Rename the SUM field from the above process to '2km Rural Population'
arcpy.AlterField_management(outTable2km, 'SUM', 'Buffer', '2km Rural Population')

#------------------------------------------------------------------------------------



#------------------------------------------------------------------------------------------------
#Make a copy of the boundaries data
arcpy.CopyFeatures_management(adminUnitsBoundaries, Output_RAI_Shapefile, "", "0", "0", "0")
#------------------------------------------------------------------------------------------------



#------------------------------------------------------------------------------------
# Set the local parameters
arcpy.AddMessage("Compiling the Rural Area Index and cleaning up ...")
inFeatures = Output_RAI_Shapefile
joinField = adminUnitsField
joinTable = outTable
fieldList = ['ruralP']

# Join two feature classes by the adminUnitsField and only carry 
# over the ruralP field
arcpy.JoinField_management (inFeatures, joinField, joinTable, joinField, fieldList)
#------------------------------------------------------------------------------------

#Delete null admin units
#EingabeTabelle = inFeatures  
#field = "ruralP" 
#whereClause = field + " IS NULL"  
#updCurs = arcpy.UpdateCursor(EingabeTabelle, whereClause) 
#for row in updCurs:     
#    if not row.getValue(field):         
#	    updCurs.deleteRow(row)  


#------------------------------------------------------------------------------------
# Set the local parameters
inFeatures = Output_RAI_Shapefile
joinField = adminUnitsField
joinTable = outTable2km
fieldList = ['Buffer']

# Join two feature classes by the adminUnitsField and only carry 
# over the ruralP field
arcpy.JoinField_management (inFeatures, joinField, joinTable, joinField, fieldList)
#------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------


		
#EingabeTabelle = inFeatures  
#field = "Buffer" 
#whereClause = field + " IS NULL"  
#updCurs = arcpy.UpdateCursor(EingabeTabelle, whereClause) 
#for row in updCurs:     
#    if not row.getValue(field):         
#	    updCurs.deleteRow(row)		
#------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------
#arcpy.AddMessage("Saving output to storage device ...")
# Add RAI field		 
arcpy.AddField_management(inFeatures, 'RAI', "DOUBLE", "", "")
 
expression = "getRAI(!Buffer!,!ruralP!)"

codeblock = """def getRAI(pop2km,popAdminUnit):
    if popAdminUnit == 0:
	   RAI = 0
    else:
       RAI = pop2km/popAdminUnit
    
    return RAI"""
    
 

 
# Execute CalculateField : Calculate Rural Access Index
arcpy.CalculateField_management(inFeatures, "RAI", expression, "PYTHON_9.3", 
                                codeblock)

#---------------------------------------------------------------------------------------------------------






















