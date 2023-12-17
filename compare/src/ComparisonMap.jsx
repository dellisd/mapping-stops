import Map, { Source, Layer } from "react-map-gl";

const ComparisonMap = (props) => {
  return (
    <Map
      mapboxAccessToken={import.meta.env.VITE_MAPBOX_TOKEN}
      mapStyle="mapbox://styles/mapbox/light-v11"
      style={{ width: window.innerWidth / 2 - 3, height: window.innerHeight }}
      {...props.viewState}
      onMoveStart={props.onMoveStart}
      onMove={props.onMove}
    >
      <Source id="base-lines" type="geojson" data={props.source}>
        <Layer
          id="route-lines"
          type="line"
          paint={{
            "line-color": ["get", "color"],
            "line-width": 2,
          }}
          layout={{}}
        />
      </Source>
    </Map>
  );
};

export default ComparisonMap;
