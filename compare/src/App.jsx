import { useState, useCallback } from "react";
import ComparisonMap from "./ComparisonMap.jsx";
import "mapbox-gl/dist/mapbox-gl.css";
import "./App.css";
import changes from "./changes.json";

function App() {
  const [viewState, setViewState] = useState({
    longitude: -75.6893682,
    latitude: 45.3961326,
    zoom: 11,
  });

  const [activeMap, setActiveMap] = useState("left");

  const onLeftMoveStart = useCallback(() => setActiveMap("left"), []);
  const onRightMoveStart = useCallback(() => setActiveMap("right"), []);
  const onMove = useCallback((evt) => setViewState(evt.viewState), []);

  return (
    <>
      <div id="maps-container">
        <ComparisonMap
          source="old.json"
          viewState={viewState}
          onMoveStart={onLeftMoveStart}
          onMove={activeMap === "left" && onMove}
          routeIds={changes.changesets["new-41"].oldRoutes}
        />
        <div className="divider"></div>
        <ComparisonMap
          source="new.json"
          viewState={viewState}
          onMoveStart={onRightMoveStart}
          onMove={activeMap === "right" && onMove}
          routeIds={changes.changesets["new-41"].newRoutes}
        />
      </div>
    </>
  );
}

export default App;
