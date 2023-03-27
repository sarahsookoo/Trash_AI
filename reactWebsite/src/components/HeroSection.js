import React from 'react';
import '../App.css';
import { Button } from './Button';
import './HeroSection.css';

function HeroSection() {
    return (
        <div className='hero-container'>
            <video src='/img2.mp4' autoPlay loop muted />
            <h1>Trash Statistics</h1>
            {/* <p>click here</p> */}
            <div className='hero-btns'>
                <Button 
                className='btns' 
                buttonStyle='btn--outline'
                buttonSize='btn--large'>
                    Get Started
                </Button>
                <Button 
                className='btns' 
                buttonStyle='btn--primary'
                buttonSize='btn--large'
                onClick={console.log('hey')}>

                {/* See Info <i className='far fa-play-circle' /> */}
                See Info
                </Button>
            </div>
        </div>
    );
}

export default HeroSection;
