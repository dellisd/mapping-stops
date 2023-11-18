import { useEffect, useState, useRef } from "react";
import "mapbox-gl/dist/mapbox-gl.css";
import "./App.css";
import Map, { Layer, Source } from "react-map-gl";
import stops from "./stops.json";

function Status(props) {
  const containerRef = useRef();

  useEffect(() => {
    if (containerRef.current != null) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [props.selection]);

  return (
    <div ref={containerRef} className="status">
      <ol>
        {props.selection.map((i) => (
          <li key={i.properties.id}>
            {`${i.properties.name} (${i.properties.code})`}
          </li>
        ))}
      </ol>
      <div className="controls">
        <button onClick={props.onCopyList}>Copy List</button>
        <button onClick={props.onClear}>Clear</button>
      </div>
    </div>
  );
}

const selectionSet = new Set();

function App() {
  const [selection, setSelection] = useState([]);

  const handleMapClick = (e) => {
    if (e.features.length != 1) {
      return;
    }
    const feature = e.features[0];
    const id = feature.properties.id;

    if (selectionSet.has(id)) {
      selectionSet.delete(id);

      setSelection((current) => current.filter((i) => i.properties.id != id));
    } else {
      selectionSet.add(id);

      setSelection((current) => [
        ...current,
        {
          type: "Feature",
          geometry: {
            type: "Point",
            coordinates: feature.geometry.coordinates,
          },
          properties: feature.properties,
        },
      ]);
    }
  };

  const handleCopyList = () => {
    const text = selection.map((i) => i.properties.id).join("\n");
    navigator.clipboard.writeText(text);
  };
  const handleClear = () => {
    setSelection([]);
  };

  const geojson = {
    type: "FeatureCollection",
    features: [
      {
        type: "Feature",
        geometry: {
          type: "LineString",
          coordinates: selection.map((i) => i.geometry.coordinates),
        },
      },
    ],
  };
  const geojsonPoints = {
    type: "FeatureCollection",
    features: selection,
  };

  return (
    <>
      <Map
        mapboxAccessToken={import.meta.env.VITE_MAPBOX_TOKEN}
        mapStyle="mapbox://styles/mapbox/streets-v9"
        style={{ width: window.innerWidth, height: window.innerHeight }}
        initialViewState={{
          longitude: -75.6893682,
          latitude: 45.3961326,
          zoom: 11,
        }}
        onMouseEnter={(e) => {
          e.target.getCanvas().style.cursor = "pointer";
        }}
        onMouseLeave={(e) => {
          e.target.getCanvas().style.cursor = "";
        }}
        onClick={handleMapClick}
        interactiveLayerIds={["stops"]}
      >
        <Source id="stops" type="geojson" data={stops}>
          <Layer
            id="stops"
            type="circle"
            paint={{
              "circle-color": "#e63b3b",
              "circle-radius": [
                "interpolate",
                ["exponential", 2],
                ["zoom"],
                10,
                2,
                15,
                8,
              ],
            }}
          />
        </Source>
        <Source id="selection" type="geojson" data={geojson}>
          <Layer
            id="selection"
            type="line"
            paint={{ "line-color": "#ecd60d", "line-width": 4 }}
          />
        </Source>
        <Source id="selection-radius" type="geojson" data={geojsonPoints}>
          <Layer
            id="stops-outline"
            type="circle"
            paint={{
              "circle-stroke-color": "#FFFFFF",
              "circle-stroke-width": 4,
              "circle-color": "#ecd60d",
              "circle-radius": [
                "interpolate",
                ["exponential", 2],
                ["zoom"],
                10,
                2,
                15,
                8,
              ],
            }}
          />
        </Source>
      </Map>
      <Status
        selection={selection}
        onCopyList={handleCopyList}
        onClear={handleClear}
      />
    </>
  );
}

export default App;
