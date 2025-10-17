import React, { useState, useEffect } from 'react';
import { TrendingUp } from 'lucide-react';
import api from '../services/api';

function IndianStocks() {
  const [stocks, setStocks] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStocks = async () => {
      try {
        const response = await api.getIndianStocksList();
        setStocks(response.stocks || []);
      } catch (err) {
        console.error('Error fetching Indian stocks:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchStocks();
  }, []);

  const handleSearch = async (query) => {
    setSearchQuery(query);
    if (!query) {
      const response = await api.getIndianStocksList();
      setStocks(response.stocks || []);
    } else {
      // Filter stocks locally for search
      const response = await api.getIndianStocksList();
      const filtered = response.stocks.filter(stock => 
        stock.toLowerCase().includes(query.toLowerCase())
      );
      setStocks(filtered);
    }
  };

  return (
    <div className="indian-stocks">
      <h1>🇮🇳 Indian Stocks - NSE</h1>
      
      <div className="search-container">
        <input
          type="text"
          placeholder="Search Indian stocks (e.g., TCS, RELIANCE)..."
          value={searchQuery}
          onChange={(e) => handleSearch(e.target.value)}
          className="search-input"
        />
      </div>

      {loading ? (
        <div className="loading">Loading stocks...</div>
      ) : (
        <div className="stocks-grid">
          {stocks.map((stock, idx) => (
            <div key={idx} className="stock-badge">
              <TrendingUp className="icon" />
              <span>{stock}</span>
            </div>
          ))}
        </div>
      )}

      {stocks.length === 0 && !loading && (
        <div className="empty-state">No stocks found</div>
      )}
    </div>
  );
}

export default IndianStocks;
