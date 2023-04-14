import React from 'react';
import '../../App.css';
import HeroSection from '../HeroSection';
import AllElements from '../AllElements';
import Footer from '../Footer';

function Home() {
    return (
        <>
          <HeroSection />
          <AllElements />
          <Footer />
        </>
    );
}

export default Home;