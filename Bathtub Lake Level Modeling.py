# ---------------------------------------------------------------------------
# bathtub.py
# Created on: 
# Description: 
# This tool computes impacts of lake level rise using bath tub approach.
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

#Take inputs to simulate Lake Victoria Sea Level rise using the bathtub approach

#Digital Elevation Raster
DEM = arcpy.GetParameterAsText(0)

#Raster Surface Resolution
demResolution = arcpy.GetParameterAsText(1)

#Study Area to model inundation e.g basin
studyArea = arcpy.GetParameterAsText(2)

#Tidal Surface 
tidalSurface = arcpy.GetParameterAsText(3)

#Desired lake level rise seperated by comas 
lakeLevelRise = arcpy.GetParameterAsText(4)

#Working folder
projectWorkspace = arcpy.GetParameterAsText(5)

#Final output with simulated inundation
#simulatedInudation = arcpy.GetParameterAsText(6)



#------------------------------------------------------------------------------------
#make copies
DEM_ = DEM
studyArea_ = studyArea
tidalSurface_ = tidalSurface
lakeLevelRise_ = str(lakeLevelRise)
demResolution_ = int(demResolution)

#---------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------
#Clipping the DEM raster
#arcpy.AddMessage("Clipping the DEM to the Study Area  ...")

#demClip = projectWorkspace+"\\clippedRaster_.tif"

#arcpy.Clip_management(DEM_, "#", demClip, studyArea_ , "ClippingGeometry", "MAINTAIN_EXTENT")


#------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------
#Add desired sea level rise (SLR) amount to tidal surface grid
for level in lakeLevelRise_.split(','):

	#Add desired sea level rise (SLR) amount to tidal surface grid

	arcpy.AddMessage("Adding " + level + " meter lake level rise to tidal surface  ...")
	
	outPlus = Plus(tidalSurface_, int(level))
	outPlus.save(projectWorkspace+"\\surface_" + level + ".tif")
	
	
	
	#Subtract DEM values from water surface to derive initial inundation depth grid
	
	arcpy.AddMessage("Generating initial inundation depth grid for " + level + " meter rise...")
	
	outCon = Con(Raster(DEM_) < projectWorkspace+"\\surface_" + level + ".tif", Minus(projectWorkspace+"\\surface_" + level + ".tif" , DEM_))
	
	outCon.save(projectWorkspace+"\\depth_" + level + ".tif")
	
	
	
	#In preparation for evaluating connectivity, create single value DEM to show inundation extent.
	
	arcpy.AddMessage("Creating single value DEM to show inundation extent ...")
	
	outCon = Con(Raster(DEM_) < projectWorkspace+"\\surface_" + level + ".tif", 1)
	
	outCon.save(projectWorkspace+"\\single_" + level + ".tif")
	
	
	
	#Evaluate connectivity of extent raster.
	arcpy.AddMessage("Evaluating connectivity of inundation extent raster ...")
	
	outRgnGrp = RegionGroup(projectWorkspace+"\\single_" + level + ".tif", "EIGHT")
	
	outRgnGrp.save(projectWorkspace+"\\clumped_" + level + ".tif")
	
	
	
	#Extract connected inundation surface to be used as a mask for the original depth grid.
	arcpy.AddMessage("Extracting connected inundation surface to be used as a mask for the original depth grid ...")
	
	rows = arcpy.da.SearchCursor(projectWorkspace+"\\clumped_" + level + ".tif", ["Count"])
	
	countValues = []
	
	for row in rows:
	
		countValues.append (row[0])
		
	countValues.sort()
	
	maxCountValue = countValues[-1]
	
	attExtractConnected = ExtractByAttributes(projectWorkspace+"\\clumped_" + level + ".tif", "Count = " + str(maxCountValue)) 
	attExtractConnected.save(projectWorkspace+"\\connect_" + level + ".tif")
	
	
	#Derive low-lying areas greater than an acre.
	arcpy.AddMessage("Deriving low-lying areas greater than an acre ...")
	acreage = 4046.85 / (demResolution_*demResolution_)
	attExtractLowLying = ExtractByAttributes(projectWorkspace+"\\clumped_" + level + ".tif", "Count > " + str(acreage)) 
	attExtractLowLying.save(projectWorkspace+"\\lowlying_" + level + ".tif")
	
	
	#Create depth grid for connected areas.
	arcpy.AddMessage("Creating depth grid for connected areas ...")
	outExtractByMask = ExtractByMask(projectWorkspace+"\\depth_" + level + ".tif", projectWorkspace+"\\connect_" + level + ".tif")
	outExtractByMask.save(projectWorkspace+"\\con_depth_" + level + ".tif")

	#Create depth grid for connected areas.
	arcpy.AddMessage("Post-processing and cleaning up ...")

	# Set local variables
	inRaster = projectWorkspace+"\\con_depth_" + level + ".tif"
	inFalseRaster = projectWorkspace+"\\con_depth_" + level + ".tif"
	whereClause = "VALUE = 0 OR VALUE = " + level

	# Check out the ArcGIS Spatial Analyst extension license
	arcpy.CheckOutExtension("Spatial")

	# Execute SetNull
	outSetNull = SetNull(inRaster, inFalseRaster, whereClause)

	# Save the output 
	outSetNull.save(projectWorkspace+"\\inundation_at_" + level + "_Meters.tif")


	# Execute RasterToPolygon
	arcpy.RasterToPolygon_conversion(projectWorkspace+"\\inundation_at_" + level + "_Meters.tif", projectWorkspace+"\\slr" + level + ".shp", "SIMPLIFY", "VALUE")



	fc = projectWorkspace+"\\slr" + level + ".shp"

	with arcpy.da.UpdateCursor(fc, "gridcode") as cursor:

		for row in cursor:

			if row[0] == 0:

				cursor.deleteRow()


	fcDissolved = projectWorkspace+"\\lakerise" + level + ".shp"
	dissolveFields = ["GRIDCODE"]
	arcpy.Dissolve_management(fc, fcDissolved, dissolveFields, "", "SINGLE_PART", "DISSOLVE_LINES")







