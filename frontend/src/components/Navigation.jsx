import React from 'react';
import './Navigation.css';

function Navigation() {
  return (
    <nav className="navigation">
      <div className="nav-container">
        <div className="nav-logo">
          📈 Stock AI Technical Analyst
        </div>
        <ul className="nav-menu">
          <li><a href="#home">Dashboard</a></li>
          <li><a href="#predict">Predictions</a></li>
          <li><a href="#portfolio">Portfolio</a></li>
          <li><a href="#signals">Signals</a></li>
        </ul>
      </div>
    </nav>
  );
}

export default Navigation;
