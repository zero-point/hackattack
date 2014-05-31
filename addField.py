from osgeo import ogr
def addField(shapefile,field):
	source = ogr.Open(shapefile, 1)
	layer = source.GetLayer()
	layer_defn = layer.GetLayerDefn()
	new_field = ogr.FieldDefn(field, ogr.OFTInteger)
	layer.CreateField(new_field)
	source = None
# addField('A_Roads.shp','example') add the 'example' field to A_Roads shapefile
