import React, { useState, useEffect } from 'react';
import './Dashboard.css';
import StockChart from './StockChart';
import Indicators from './Indicators';
import MLPrediction from './MLPrediction';
import Portfolio from './Portfolio';
import api from '../services/api';

function Dashboard() {
  const [symbol, setSymbol] = useState('AAPL');
  const [stockData, setStockData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStockData();
  }, [symbol]);

  const fetchStockData = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getStockData(symbol, 30);
      setStockData(data);
    } catch (err) {
      setError('Failed to fetch stock data. Make sure the API is running on port 8000');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSymbolChange = (e) => {
    setSymbol(e.target.value.toUpperCase());
  };

  return (
    <div className="dashboard-container">
      <div className="search-container">
        <input
          type="text"
          placeholder="Enter stock symbol (e.g., AAPL, RELIANCE)"
          value={symbol}
          onChange={handleSymbolChange}
          className="search-input"
        />
        <button onClick={fetchStockData} className="search-button">
          Search
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="dashboard-grid">
        <div className="section-full">
          <StockChart symbol={symbol} data={stockData} />
        </div>
        <div className="section">
          <Indicators symbol={symbol} />
        </div>
        <div className="section">
          <MLPrediction symbol={symbol} />
        </div>
        <div className="section-full">
          <Portfolio />
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
