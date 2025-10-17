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
  const [isIndianStock, setIsIndianStock] = useState(false);
  const [indianStocksList, setIndianStocksList] = useState([]);
  const [showError, setShowError] = useState(true);

  // Fetch Indian stocks list on component mount
  useEffect(() => {
    const loadIndianStocks = async () => {
      try {
        console.log('Fetching Indian stocks list from backend...');
        const response = await api.getIndianStocks();
        console.log('Indian stocks loaded:', response.stocks);
        setIndianStocksList(response.stocks || []);
      } catch (err) {
        console.error('Failed to load Indian stocks list:', err);
        // Fallback to hardcoded list if API fails
        setIndianStocksList([
          'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'HINDUNILVR', 'ICICIBANK', 
          'KOTAKBANK', 'SBIN', 'BHARTIARTL', 'ITC', 'AXISBANK', 'LT', 
          'ASIANPAINT', 'MARUTI', 'BAJFINANCE', 'WIPRO', 'TITAN', 'ULTRACEMCO',
          'NESTLEIND', 'SUNPHARMA', 'ONGC', 'NTPC', 'POWERGRID', 'M&M', 
          'TECHM', 'TATASTEEL', 'BAJAJFINSV', 'HCLTECH', 'ADANIPORTS'
        ]);
      }
    };
    loadIndianStocks();
  }, []);

  // Fetch stock data when symbol changes
  useEffect(() => {
    if (indianStocksList.length > 0) {
      fetchStockData();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [symbol, indianStocksList]);

  // Auto-dismiss error after 10 seconds
  useEffect(() => {
    if (error && showError) {
      const timer = setTimeout(() => {
        setShowError(false);
      }, 10000);
      return () => clearTimeout(timer);
    }
  }, [error, showError]);

  const fetchStockData = async () => {
    try {
      setLoading(true);
      setError(null);
      setShowError(true); // Reset error visibility
      
      // Check if the symbol is an Indian stock
      const isIndian = indianStocksList.includes(symbol.toUpperCase());
      setIsIndianStock(isIndian);
      
      let data;
      if (isIndian) {
        // Fetch Indian stock data
        console.log(`Fetching Indian stock data for ${symbol}`);
        data = await api.getIndianStockData(symbol, 30);
      } else {
        // Fetch US stock data
        console.log(`Fetching US stock data for ${symbol}`);
        data = await api.getStockData(symbol, 30);
      }
      
      setStockData(data);
      // Clear any previous errors on success
      setError(null);
      setShowError(false);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Unknown error';
      setError(`Failed to fetch stock data: ${errorMessage}`);
      setShowError(true);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSymbolChange = (e) => {
    setSymbol(e.target.value.toUpperCase());
    // Clear error when user starts typing
    if (error) {
      setShowError(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      fetchStockData();
    }
  };

  const dismissError = () => {
    setShowError(false);
  };

  return (
    <div className="dashboard-container">
      <div className="search-container">
        <input
          type="text"
          placeholder="Enter stock symbol (e.g., AAPL, TCS, RELIANCE)"
          value={symbol}
          onChange={handleSymbolChange}
          onKeyPress={handleKeyPress}
          className="search-input"
        />
        <button onClick={fetchStockData} className="search-button" disabled={loading}>
          {loading ? 'Loading...' : 'Search'}
        </button>
        {isIndianStock && (
          <span className="stock-type-badge indian">🇮🇳 Indian Stock</span>
        )}
        {!isIndianStock && stockData && (
          <span className="stock-type-badge us">🇺🇸 US Stock</span>
        )}
        {indianStocksList.length > 0 && (
          <span className="stocks-loaded">
            ({indianStocksList.length} Indian stocks loaded)
          </span>
        )}
      </div>

      {error && showError && (
        <div className="error-message">
          <span className="error-text">{error}</span>
          <button className="dismiss-button" onClick={dismissError}>✕</button>
        </div>
      )}

      {loading && <div className="loading-message">Loading stock data...</div>}

      <div className="dashboard-grid">
        <div className="section-full">
          <StockChart symbol={symbol} data={stockData} isIndianStock={isIndianStock} />
        </div>
        <div className="section">
          <Indicators 
            symbol={symbol} 
            isIndianStock={isIndianStock} 
            stockDataLoaded={!!stockData} 
            key={`${symbol}-${stockData ? 'loaded' : 'empty'}`}
          />
        </div>
        <div className="section">
          <MLPrediction symbol={symbol} isIndianStock={isIndianStock} />
        </div>
        <div className="section-full">
          <Portfolio />
        </div>
      </div>
    </div>
  );
}

export default Dashboard;