import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from './Button';
import './Footer.css';

function Footer() {
    return (
        <div className='footer-container'>
            <section className="footer-detail">
                <p className="footer-detail-heading">
                    Learn more
                </p>
                <p className="footer-detail-text">
                    Receive Updates!
                </p>
                <div className="input-areas">
                    <form>
                        <input 
                        type="email" 
                        name="email" 
                        placeholder="your email" 
                        className="footer-input"/>
                        <Button buttonStyle='btn--outline'>
                            Enter
                        </Button>
                    </form>
                </div>
            </section>
            <div className='footer-links'>
                <div className='footer-link-wrapper'>
                    <div className='footer-link-items'>
                        <h2>About Us</h2>
                        <Link to='/'>How it works</Link>
                    </div>
                </div>
            </div>
            {/* social media logos ? */}
        </div>
    );
}

export default Footer;
