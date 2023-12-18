import partridge as ptg
import json
from collections import defaultdict

gtfs_path = "google_transit.zip"
gtfs_outpath = "cleaned_gtfs.zip"

feed = ptg.load_raw_feed(gtfs_path)

# print(feed.trips.__class__)

print("Computing trip patterns")
trip_ids_by_pattern = defaultdict(list)
pattern_by_trip_id = {}
for trip_id, stop_times in feed.stop_times.sort_values("stop_sequence").groupby("trip_id"):
    pattern = tuple(stop_times.stop_id)
    pattern_by_trip_id[trip_id] = pattern
    trip_ids_by_pattern[pattern].append(trip_id)

print("Matching routes to trips")
route_id_by_trip_id = {}
shape_by_trip_id = {}
for _, trip in feed.trips.iterrows():
    assert trip.trip_id not in shape_by_trip_id, f"{trip_id} {json.dumps(shape_by_trip_id)}"
    shape_by_trip_id[trip.trip_id] = trip.shape_id
    route_id_by_trip_id[trip.trip_id] = trip.route_id

print("Counting patterns by route")
patterns_by_route = defaultdict(list)
for pattern, trip_ids in trip_ids_by_pattern.items():
    trip = feed.trips.loc[feed.trips['trip_id'] == trip_ids[0]].iloc[0]
    patterns_by_route[(trip['route_id'], trip['direction_id'])].append(pattern)
print(patterns_by_route)

print("Computing most common pattern trip IDs")
most_common_pattern_trip_ids = []
for route, patterns in patterns_by_route.items():
    max_pattern = None
    max_pattern_len = 0
    for pattern in patterns:
        if max_pattern is None or len(trip_ids_by_pattern[pattern]) > max_pattern_len:
            max_pattern_len = len(trip_ids_by_pattern[pattern])
            max_pattern = pattern

    # Only taking one trip per route to make things simple
    most_common_pattern_trip_ids.append(trip_ids_by_pattern[max_pattern][0])

print("Getting output feed")
output_feed = ptg.load_raw_feed(gtfs_path)

trip_ids_set = set(most_common_pattern_trip_ids)

output_view = {
    'trips.txt': {'trip_id': trip_ids_set},
    'stop_times.txt': {'trip_id': trip_ids_set}
}

feed.set("trips.txt", feed.trips.loc[feed.trips['trip_id'].isin(trip_ids_set)])
feed.set("stop_times.txt", feed.stop_times.loc[feed.stop_times['trip_id'].isin(trip_ids_set)])

ptg.writers.write_feed_dangerously(feed, "cleaned_gtfs.zip")
