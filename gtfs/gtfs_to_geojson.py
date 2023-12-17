from geojson import Point, LineString, Feature, FeatureCollection, dumps
import partridge as ptg
import sys
from route_color import route_color

if len(sys.argv) < 4:
    print("Usage:")
    print("    gtfs_to_geojson.py [source_gtfs.zip] [output.json] [old / new]")
    exit(-1)

gtfs_inpath = sys.argv[1]
geojson_outpath = sys.argv[2]
mode = sys.argv[3]
if mode not in ["old", "new"]:
    print("Must specify 'old' or 'new' mode")
    exit(-1)

feed = ptg.load_feed(gtfs_inpath)

geojson_features = []

print("Reading Stops")
for _, stop in feed.stops.iterrows():
    geojson_features.append(Feature(geometry=Point((stop['stop_lon'], stop['stop_lat'])), properties={
        'id': stop['stop_id'],
        'code': str(stop['stop_code']),
        'name': stop['stop_name'],
    }))

print("Reading Shapes")
shape_id_by_trip = feed.shapes.groupby('shape_id').apply(list)
# print(shape_id_by_trip.head())

for _, trip in feed.trips.iterrows():
    shape = feed.shapes.loc[feed.shapes['shape_id'] == trip['shape_id']]
    route = feed.routes.loc[feed.routes['route_id'] == trip['route_id']]
    pts = []
    for _, shape_pt in shape.iterrows():
        pts.append((shape_pt['shape_pt_lon'], shape_pt['shape_pt_lat']))
    geojson_features.append(Feature(geometry=LineString(pts), properties={
        'route_id': trip['route_id'],
        'direction_id': trip['direction_id'],
        'color': route_color(str(route.iloc[0]['route_short_name']), mode=mode)
    }))

with open(geojson_outpath, "w") as file:
    file.write(dumps(FeatureCollection(geojson_features)))
