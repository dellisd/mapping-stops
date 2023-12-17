import Map from "react-map-gl";

const ComparisonMap = (props) => {
    return <Map
        mapboxAccessToken={import.meta.env.VITE_MAPBOX_TOKEN}
        mapStyle="mapbox://styles/mapbox/streets-v9"
        style={{ width: (window.innerWidth / 2) - 3, height: window.innerHeight }}
        {...props.viewState}
        onMoveStart={props.onMoveStart}
        onMove={props.onMove}
        ></Map>
}

export default ComparisonMap;
