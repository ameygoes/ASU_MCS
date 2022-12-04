
import {useState, useEffect} from 'react';
import {Map} from 'react-map-gl';
import {AmbientLight, PointLight, LightingEffect} from '@deck.gl/core';
import DeckGL from '@deck.gl/react';
import {TripsLayer} from '@deck.gl/geo-layers';






function ViewTrajectory(){

  const [data,setData] = useState([{}])
  const [layer,setLayer] = useState([])

  const INITIAL_VIEW_STATE = {
    longitude: -111.92518396810091,
    latitude: 33.414291502635706,
    zoom: 20,
    maxZoom: 30,
    pitch: 20,
    bearing: 0
  };

  const ambientLight = new AmbientLight({
    color: [255, 255, 255],
    intensity: 1.0
  });
  
  const pointLight = new PointLight({
    color: [255, 255, 255],
    intensity: 2.0,
    position: [-74.05, 40.7, 8000]
  });

  const lightingEffect = new LightingEffect({ambientLight, pointLight});

const material = {
  ambient: 0.1,
  diffuse: 0.6,
  shininess: 32,
  specularColor: [60, 64, 70]
};

const trailLength = 60
const loopLength = 300
const animationSpeed = 1
const theme = {
  buildingColor: [74, 80, 87],
  trailColor0: [253, 128, 93],
  material,
  effects: [lightingEffect]
};
const [time, setTime] = useState(0);
const [animation] = useState({});

const animate = () => {
  setTime(t => (t + animationSpeed) % loopLength);
  animation.id = window.requestAnimationFrame(animate);
};

useEffect(() => {
  animation.id = window.requestAnimationFrame(animate);
  return () => window.cancelAnimationFrame(animation.id);
}, [animation]);

  const MAP_STYLE = 'https://basemaps.cartocdn.com/gl/dark-matter-nolabels-gl-style/style.json';

    useEffect(()=>{
        fetch("/viewSpatial").then(
            res => res.json()
        ).then( data =>{
            
          setData(data)
          console.log(data)
          setLayer(
            new TripsLayer({
              id: 'trips',
              data,
              getPath: d => d.location,
              getTimestamps: d => d.timestamps,
              getColor: [253, 128, 93],
              opacity: 0.3,
              widthMinPixels: 2,
              rounded: true,
              trailLength,
              currentTime: time,
        
              shadowEnabled: false
            })
          )
        }
        )
    },[time])
  

  const layers = [
    layer
  ]

  return (
    <div style={{position:"relative",height: '80vh', width: '80vw'}}>
    {data === 'undefined'? 'Loading....' : (
      <DeckGL
      layers={layers}
      effects={theme.effects}
      initialViewState={INITIAL_VIEW_STATE}
      controller={true}
    >
      <Map mapboxAccessToken={''} reuseMaps mapStyle={MAP_STYLE} preventStyleDiffing={true} />
    </DeckGL>
    )}
    
      
    </div>
  );
}

export default ViewTrajectory;