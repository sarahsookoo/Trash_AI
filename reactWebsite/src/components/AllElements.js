import React from 'react';
import Element from './Element';
import './AllElements.css';

function AllElements() {
    return (
        <div className='elements'>
            <h1> About </h1>
            <div className='elements_container'>
                <div className='elements_wrapper'>
                    <ul className="all_elements">
                        <Element 
                        src="images/recycle.jpg"
                        text="More Information"
                        label="About"
                        path="/services"
                        />
                        <Element 
                        src="images/hardware.jpg"
                        text="Mechanics/Hardware"
                        label="Learn More"
                        path="/services"
                        />
                        <Element 
                        src="images/ml.jpg"
                        text="Behind Machine Learning"
                        label="How It Works"
                        path="/services"
                        />
                    </ul>
                </div>
            </div>
        </div>
        
    )
}

export default AllElements
