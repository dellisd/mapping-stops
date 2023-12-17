import {useState, useCallback} from "react";
import ComparisonMap from "./ComparisonMap.jsx";
import "mapbox-gl/dist/mapbox-gl.css";
import './App.css'

function App() {

  const [viewState, setViewState] = useState({
    longitude: -75.6893682,
    latitude: 45.3961326,
    zoom: 11,
  });

  const [activeMap, setActiveMap] = useState('left');

  const onLeftMoveStart = useCallback(() => setActiveMap('left'), []);
  const onRightMoveStart = useCallback(() => setActiveMap('right'), []);
  const onMove = useCallback(evt => setViewState(evt.viewState), []);

  return (
    <>
      <div id="maps-container">
        <ComparisonMap
          viewState={viewState}
          onMoveStart={onLeftMoveStart}
          onMove={activeMap === 'left' && onMove}
        />
        <div className="divider"></div>
        <ComparisonMap
          viewState={viewState}
          onMoveStart={onRightMoveStart}
          onMove={activeMap === 'right' && onMove}/>
      </div>
    </>
  )
}

export default App
