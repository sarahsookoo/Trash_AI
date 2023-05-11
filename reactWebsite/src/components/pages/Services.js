import React from 'react';
import './Services.css';

function Services() {
    return (
        <div>
        {/* <h1 className='services'>SERVICES</h1>; */}
        <video src='/vid3.mp4' autoPlay loop muted />
        
            <h1>Info</h1>
        
       
        
        <div className="body-header">
        <h1>How does Trash AI work? </h1>

        </div>

        <div className="body">
        <h1>Trash AI is a combination of hardware including an arduino, weight sensor, HX711 module, raspberry pi, pi camera, stepper motor, and an actuator. However, the brains behind the garbage can is actually a trained machine learning model that uses image classification to discern trash and types of recyclables. They work together to create moving parts and store all this data while doing so. </h1>

        </div>
        

        

        </div>

    );
}
export default Services;

// import React from 'react';
// import './App.css';
// import { fetchData } from './fetchData';

// const App = () => {
//   const fetchDataFormDynamoDb = () => {
//     fetchData('users')
//   }

//   return (
//     <>
//       <button onClick={() => fetchDataFormDynamoDb()}> Fetch </button>
//     </>
//   );
// }

// export default App;