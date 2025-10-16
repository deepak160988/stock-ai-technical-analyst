import React, { useState, useEffect } from 'react';
import './App.css';
import StockSearch from './components/StockSearch';
import IndicatorsDashboard from './components/IndicatorsDashboard';
import PortfolioAnalytics from './components/PortfolioAnalytics';
import IndianStocks from './components/IndianStocks';
import Navigation from './components/Navigation';

function App() {
  const [activeTab, setActiveTab] = useState('search');
  const [selectedStock, setSelectedStock] = useState(null);

  return (
    <div className="app">
      <Navigation activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <div className="container">
        {activeTab === 'search' && (
          <StockSearch onSelectStock={setSelectedStock} />
        )}
        
        {activeTab === 'indicators' && selectedStock && (
          <IndicatorsDashboard symbol={selectedStock} />
        )}
        
        {activeTab === 'portfolio' && (
          <PortfolioAnalytics />
        )}
        
        {activeTab === 'indian' && (
          <IndianStocks />
        )}
      </div>
    </div>
  );
}

export default App;
