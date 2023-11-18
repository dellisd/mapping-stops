import csv
import io
import json
import sys
import zipfile

if len(sys.argv) < 2:
    print("Usage:\n    stops.py gtfs.zip\n\nOutputs a stops.json file")
    exit(-1)

stops = []

gtfs_archive = zipfile.ZipFile(sys.argv[1], "r")
with io.TextIOWrapper(gtfs_archive.open("stops.txt")) as stops_file:
    data = csv.DictReader(stops_file)

    for row in data:
        stops.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [float(row["stop_lon"]), float(row["stop_lat"])],
            },
            'properties': {
                'id': row["stop_id"],
                'code': row["stop_code"],
                'name': row["stop_name"],
            }
        })

geojson = {
    'type': 'FeatureCollection',
    'features': stops
}

with open("stops.json", "wt") as f:
    json.dump(geojson, f)
