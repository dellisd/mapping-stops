import csv
import io
import os
import pathlib
import shutil
import sys
import zipfile

SERVICE_ID = "DUMMY_SERVICE"
block = 101010


def make_route(name):
    return {
        "route_id": name,
        "route_short_name": name,
        "route_long_name": None,
        "route_desc": None,
        "route_type": 3,  # Bus Route
        "route_url": None,
    }


def make_trip(route_name):
    global block
    block = block + 1

    id = f"{route_name}.trip"
    return (id, {
        "route_id": route_name,
        "service_id": SERVICE_ID,
        "trip_id": id,
        "trip_headsign": "Dummy Headsign",
        "direction_id": 0,
        "block_id": block
    })


def make_stop_times(file, trip_id):
    with open(file, "r") as f:
        stop_sequence = f.readlines()

    times = []
    for index, stop in enumerate(stop_sequence):
        times.append({
            "trip_id": trip_id,
            "arrival_time": "00:00:00",
            "departure_time": "00:00:00",
            "stop_id": stop.strip("\n"),
            "stop_sequence": index + 1,
            "pickup_type": 0,
            "drop_off_type": 0,
        })
    return times


if len(sys.argv) < 3:
    print("Usage:")
    print("    generate_gtfs.py [source_gtfs.zip] [routes/]")

routes = []
trips = []
stop_times = []

files = os.listdir(sys.argv[2])
for entry in files:
    routes.append(make_route(entry))
    (trip_id, trip) = make_trip(entry)
    trips.append(trip)

    stop_times.extend(make_stop_times(
        pathlib.Path(sys.argv[2]) / entry, trip_id))

if not os.path.isdir("gtfs"):
    os.mkdir("gtfs")
with open("gtfs/routes.txt", "w") as routes_file:
    writer = csv.DictWriter(routes_file, fieldnames=[
        "route_id",
        "route_short_name",
        "route_long_name",
        "route_desc",
        "route_type",
        "route_url"
    ])
    writer.writeheader()
    writer.writerows(routes)

with open("gtfs/trips.txt", "w") as trips_file:
    writer = csv.DictWriter(trips_file, fieldnames=[
        "route_id",
        "service_id",
        "trip_id",
        "trip_headsign",
        "direction_id",
        "block_id"
    ])
    writer.writeheader()
    writer.writerows(trips)

with open("gtfs/stop_times.txt", "w") as stop_times_file:
    writer = csv.DictWriter(stop_times_file, fieldnames=[
        "trip_id",
        "arrival_time",
        "departure_time",
        "stop_id",
        "stop_sequence",
        "pickup_type",
        "drop_off_type",
    ])
    writer.writeheader()
    writer.writerows(stop_times)

with open("gtfs/calendar.txt", "w") as calendar_file:
    calendar_file.writelines([
        "service_id,monday,tuesday,wednesday,thursday,friday,saturday,start_date,end_date",
        f"{SERVICE_ID},1,1,1,1,1,1,1,20230101,20241212"
    ])

# Merge additional stops with original stops

with zipfile.ZipFile(sys.argv[1], "r") as gtfs_archive:
    with io.TextIOWrapper(gtfs_archive.open("stops.txt")) as stops_file:
        original_data = csv.DictReader(stops_file)
        with open("additional_stops.txt") as additional_file:
            additional_data = csv.DictReader(additional_file)

            with open("gtfs/stops.txt", "w") as stops_file:
                writer = csv.DictWriter(stops_file, fieldnames=[
                    "stop_id",
                    "stop_code",
                    "stop_name",
                    "stop_desc",
                    "stop_lat",
                    "stop_lon",
                    "zone_id",
                    "stop_url",
                    "location_type",
                    "parent_station",
                    "stop_timezone",
                    "wheelchair_boarding",
                    "platform_code",
                    "level_id",
                ])
                writer.writeheader()
                writer.writerows(original_data)
                writer.writerows(additional_data)

    gtfs_archive.extract("agency.txt", "gtfs")
