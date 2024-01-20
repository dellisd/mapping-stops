## Setup

1. Create a venv and activate it `python3 -m venv .venv && source .venv/bin/activate`
2. Install the dependencies `pip install -r requirements.txt`
3. Download the original GTFS data `wget https://www.octranspo.com/files/google_transit.zip`

### Get a NCR region OSM file

```shell
# Download provincial extracts
wget https://download.geofabrik.de/north-america/canada/ontario-latest.osm.pbf
wget https://download.geofabrik.de/north-america/canada/quebec-latest.osm.pbf

osmium merge ontario-latest.osm.pbf quebec-latest.osm.pbf -o merged.osm.pbf

# Extract the National Capital Region
osmium extract -b -76.2616,45.1249,-75.1726,45.6620 merged.osm.pbf -o ncr.osm.pbf

# Extract an XML file from the PBF
osmium cat ncr.osm.pbf -o ncr.osm
```

## Generate the custom GTFS

This includes all of the route review changes in a simulated GTFS dataset that can be consumed by pfaedle.

```shell
python generate_gtfs.py google_transit.zip ../routes
# Outputs into 'generated_gtfs/'
```

## Generate the Shapes

```shell
pfaedle -x ncr.osm -D -o [output] [gtfs here]
```

## Processing Flow

```shell
# Clean input GTFS (input: google_transit.zip, output: cleaned_gtfs.zip)
python clean.py

# Generate custom GTFS
python generate_gtfs2.py ../routes cleaned_gtfs.zip

# Generate new shapes
pfaedle -x ncr.osm -D -o new_gtfs test.zip

# Convert the pfaedle output into a geojson file
python gtfs_to_geojson.py new_gtfs new.json new
# Copy the json file into the web app project!
```