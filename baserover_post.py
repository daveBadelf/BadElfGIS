#This script adjusts rover points based on post processing
import arcpy

#arcpy.env.workspace = r'C:\Default.gdb'
#user entered coords from opus
OPUS_lat = arcpy.GetParameterAsText(0).lstrip().rstrip()
OPUS_lon = arcpy.GetParameterAsText(1).lstrip().rstrip()
OPUS_orth = arcpy.GetParameter(2)
base_lat = arcpy.GetParameter(3)
base_lon = arcpy.GetParameter(4)
base_orth = arcpy.GetParameter(5)
#points shot using base rover to be shifted
rover_pts = arcpy.GetParameterAsText(6)
cleanedLat = 0
cleanedLon = 0
#base_pt = arcpy.GetParameterAsText(3)
updateFields = ['SHAPE@X','SHAPE@Y','SHAPE@Z']
wrkspce = arcpy.env.workspace



# #names table for where offset calcs are created
# def nameTable(wrkspce):
#     #creating table name, adding 1 to whatever the last table created was
#     tableName = 'opus0'
#     tableList = arcpy.ListTables() 
#     for table in tableList:
#         try:
#             num = int(table[-1])
#             if "opus" in table:
#                 if int(tableName[-1]) <= num:
#                     tableName = 'opus' + str(num+1)
#         except: continue

#     #creating table with new name
#     arcpy.management.CreateFeatureclass(wrkspce,tableName,'POINT',has_z='ENABLED',spatial_reference=rover_pts)
    
#     #list of relevant lat lon fields to calc offset
#     fieldList = ['oLat','oLon','bLat','bLon','dLat','dLon']
#     for field in fieldList:
#         arcpy.management.AddField(tableName, field, 'DOUBLE')
#     return tableName



#calcs xy offset for base point
def offsetCalc(OPUS_lat, OPUS_lon, OPUS_orth, base_lat, base_lon, base_orth):
    #converting from dms
    OPUS_lat_split = [float(item) for item in OPUS_lat.split(' ')]
    OPUS_lon_split = [float(item) for item in OPUS_lon.split(' ')]
    OPUS_lat_dd = (OPUS_lat_split[0] + (OPUS_lat_split[1]/60) + (OPUS_lat_split[2]/3600))
    OPUS_lon_dd = -1*(OPUS_lon_split[0] + (OPUS_lon_split[1]/60) + (OPUS_lon_split[2]/3600))
    #calcing offset
    lat_offset = OPUS_lat_dd - base_lat
    lon_offset = OPUS_lon_dd - base_lon
    orth_offset = OPUS_orth - base_orth
    return [lat_offset,lon_offset,orth_offset]
    



# #getting geom from input base point
#     basePt = arcpy.da.SearchCursor(base_pt, ['SHAPE@X','SHAPE@Y'])

# #error if there's multiple basepoints, recording base points
#     basePtCount = 0
#     with basePt as cursor:
#         for row in basePt:
#             basePtCount +=1
#             if basePtCount > 1:
#                 arcpy.AddError('Too many points in Base feature Class')
#             bLat = row[1]
#             bLon = row[0]
     
#     #fields to update
#     fieldList = ['oLon','oLat','bLat','bLon','dLat','dLon','SHAPE@XY']
# #updating table and calcing offset
#     fLat = float(lat)
#     fLon = float(lon)
#     fbLat = float(bLat)
#     fbLon = float(bLon)
#     latDiff = fLat - fbLat
#     lonDiff = fLon - fbLon
#     valueList = [(fLon,fLat,fbLat,fbLon,latDiff,lonDiff,(fLon,fLat,)),]
#     uCursor = arcpy.da.InsertCursor(tableName, fieldList)
#     with arcpy.da.SearchCursor(rover,['SHAPE@X','SHAPE@Y']) as sCursor:
#         for feature in sCursor:
#             newLat = float(feature[1])+valueList[0][4]
#             newLon = float(feature[0])+valueList[0][5]
#             valueList.append((fLat,fLon,fbLat,fbLon,latDiff,lonDiff,(newLon,newLat)))
#     for row in valueList:
#         uCursor.insertRow(row)
#     del uCursor    
        
#     return [latDiff,lonDiff]

#shifts points a certain amount based on results of near tool
def shiftXY(roverPoints, updateFields, offset):
    # with arcpy.da.SearchCursor(ppTable,['dLat','dLon']) as cursor:
    #     for row in cursor:
    #         lonShift = row[1]
    #         latShift = row[0]
    
    #fix the order so its not confusing
    with arcpy.da.UpdateCursor(roverPoints, updateFields) as cursor:
        for geom in cursor:
            geom[0] = geom[0] + float(offset[1])
            geom[1] = geom[1] + float(offset[0])
            geom[2] = geom[2] + float(offset[2])
            cursor.updateRow(geom)
            arcpy.AddMessage(f'offseting rover points by {geom[1]} deg lat and {geom[1]} deg lon')
    del cursor        


# tableName = nameTable(wrkspce)
offset = offsetCalc(OPUS_lat,OPUS_lon,OPUS_orth,base_lat,base_lon,base_orth)
arcpy.AddMessage(f'offseting rover points by {offset[0]} deg lat and {offset[1]} deg lon')
shiftXY(rover_pts,updateFields,offset)
    
