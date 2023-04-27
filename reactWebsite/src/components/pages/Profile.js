import React, { useState } from 'react';
import { Button } from '../Button';
import './Profile.css';

function Profile() {

    const [plotPath, setPlotPath] = useState(null);

    const handleStatisticsClick = async () => {
        const response = await fetch('http://127.0.0.1:5000/statistics');
        const data = await response.json();
        setPlotPath(data.plot_path);
    }

    return (
        <div className='profile'>
            <video src='/vid5.mp4' autoPlay loop muted />
            <div className='profile-title'> 
                <h1>Profile</h1>
            </div>
            <div className='account'> 
                My Account
            </div>
            <div className='name'> 
                Name:
            </div>
            <div className='email'> 
                Email:
            </div>
            <div className='stats-btn'>
                <Button 
                    className='btns' 
                    button type="submit"
                    buttonStyle='btn--outline'
                    buttonSize='btn--large'
                    onClick={handleStatisticsClick}>
                        My Trash AI Statistics
                </Button>
            </div>
            {plotPath && 
                <div className='stats-plot'>
                    <img src={plotPath} alt='Trash AI Statistics' />
                </div>
            }
        </div>
    );
}

export default Profile;
