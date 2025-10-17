import React, { useState } from 'react';
import { Search } from 'lucide-react';
import api from '../services/api';

function StockSearch({ onSelectStock }) {
  const [symbol, setSymbol] = useState('');
  const [stock, setStock] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      const response = await api.getLatestPrice(symbol);
      setStock(response);
      onSelectStock(symbol);
    } catch (err) {
      setError('Stock not found');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="search-container">
      <h1>📈 Stock AI Technical Analyst</h1>
      <form onSubmit={handleSearch} className="search-form">
        <div className="search-input-group">
          <Search className="search-icon" />
          <input
            type="text"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value.toUpperCase())}
            placeholder="Enter stock symbol (e.g., AAPL, TCS)"
            className="search-input"
          />
          <button type="submit" className="search-btn" disabled={loading}>
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>
      </form>

      {error && <div className="error">{error}</div>}

      {stock && (
        <div className="stock-card">
          <h2>{stock.symbol}</h2>
          <div className="stock-info">
            <div className="info-item">
              <span className="label">Price:</span>
              <span className="value">${stock.price}</span>
            </div>
            <div className="info-item">
              <span className="label">Currency:</span>
              <span className="value">{stock.currency}</span>
            </div>
            {stock.name && (
              <div className="info-item">
                <span className="label">Name:</span>
                <span className="value">{stock.name}</span>
              </div>
            )}
            {stock.sector && (
              <div className="info-item">
                <span className="label">Sector:</span>
                <span className="value">{stock.sector}</span>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default StockSearch;
