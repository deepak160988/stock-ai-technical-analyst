import React from 'react';
import { Home, TrendingUp, BarChart3, Globe } from 'lucide-react';

function Navigation({ activeTab, setActiveTab }) {
  return (
    <nav className="navigation">
      <div className="nav-brand">📊 Stock AI Analyst</div>
      <div className="nav-menu">
        <button
          className={`nav-item ${activeTab === 'search' ? 'active' : ''}`}
          onClick={() => setActiveTab('search')}
        >
          <Home size={20} />
          <span>Search</span>
        </button>
        <button
          className={`nav-item ${activeTab === 'indicators' ? 'active' : ''}`}
          onClick={() => setActiveTab('indicators')}
        >
          <TrendingUp size={20} />
          <span>Indicators</span>
        </button>
        <button
          className={`nav-item ${activeTab === 'portfolio' ? 'active' : ''}`}
          onClick={() => setActiveTab('portfolio')}
        >
          <BarChart3 size={20} />
          <span>Portfolio</span>
        </button>
        <button
          className={`nav-item ${activeTab === 'indian' ? 'active' : ''}`}
          onClick={() => setActiveTab('indian')}
        >
          <Globe size={20} />
          <span>Indian Stocks</span>
        </button>
      </div>
    </nav>
  );
}

export default Navigation;
