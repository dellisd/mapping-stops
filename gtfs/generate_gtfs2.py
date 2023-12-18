import os
import pandas as pd
import partridge as ptg
from pathlib import Path
import sys
from additional_stops import stops as additional_stops

if len(sys.argv) < 3:
    print("Usage:")
    print("    generate_gtfs2.py [routes] [source_gtfs.zip] [output_gtfs.zip]")
    exit(-1)

routes_dir = sys.argv[1]
gtfs_inpath = sys.argv[2]

block = 101010

feed = ptg.load_raw_feed(gtfs_inpath)

print("Adding additional stops")
additional_stops_list = []
for id, name, lat, lon in additional_stops:
    additional_stops_list.append({
        'stop_id': id,
        'stop_code': '0000',
        'stop_name': name,
        'stop_lat': lat,
        'stop_lon': lon,
        'location_type': 0,
    })

additional_stops_df = pd.DataFrame(additional_stops_list)
feed.set("stops.txt", pd.concat([feed.stops, additional_stops_df]))

unchanged_routes = ['1', '6', '7', '11', '12', '14']
unchaged_route_ids = list(map(lambda x: f"{x}-349", unchanged_routes))
unchanged_trip_ids = []

for _, trip in feed.trips.loc[feed.trips["route_id"].isin(unchaged_route_ids)].iterrows():
    unchanged_trip_ids.append(trip['trip_id'])

used_route_ids = set()
new_routes = []
new_trips = []
new_stop_times = []

print("Reading Routes")
route_files = os.listdir(routes_dir)
for route_file in route_files:
    with open(Path(routes_dir) / route_file, "r") as file:
        block = block + 1
        lines = file.readlines()

        num, dir = lines[0].split(" ")
        route_stops = lines[1:]
        route_id = f"{num}-new"

        if route_id not in used_route_ids:
            used_route_ids.add(route_id)
            new_routes.append({
                "route_id": route_id,
                "route_short_name": num,
                "route_type": 3,
            })

        direction = dir.strip('\n')
        trip_id = f"{num}-{direction}-trip"
        new_trips.append({
            "trip_id": trip_id,
            "service_id": "dummy_service",
            "route_id": route_id,
            "direction_id": int(dir),
            "block_id": str(block)
        })

        for index, stop in enumerate(route_stops):
            new_stop_times.append({
                "trip_id": trip_id,
                "arrival_time": "00:00:00",
                "departure_time": "00:00:00",
                "stop_id": stop.strip("\n"),
                "stop_sequence": index + 1,
            })


# Filter routes
# Add "new" routes
feed.set("routes.txt", pd.concat([
    feed.routes.loc[feed.routes["route_short_name"].isin(unchanged_routes)],
    pd.DataFrame(new_routes)
]))

# Filter trips
# Add "new" trips
feed.set("trips.txt", pd.concat([
    feed.trips.loc[feed.trips["route_id"].isin(unchaged_route_ids)],
    pd.DataFrame(new_trips)
]))

# Filter stop times
# Add "new" stop times
feed.set("stop_times.txt", pd.concat([
    feed.stop_times.loc[feed.stop_times["trip_id"].isin(unchanged_trip_ids)],
    pd.DataFrame(new_stop_times)
]))


ptg.writers.write_feed_dangerously(feed, "test.zip")
print("Done.")
