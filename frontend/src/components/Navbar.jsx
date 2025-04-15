import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav style={{ padding: '10px', background: '#eee' }}>
      <Link to="/" style={{ margin: '0 10px' }}>Home</Link>
      <Link to="/crop" style={{ margin: '0 10px' }}>Crop</Link>
      <Link to="/disease" style={{ margin: '0 10px' }}>Disease</Link>
      <Link to="/chat" style={{ margin: '0 10px' }}>ChatBot</Link>
    </nav>
  );
};

export default Navbar;
