import React, { useState, useEffect } from 'react';
import api from '../services/api';

function Portfolio() {
  const [portfolio, setPortfolio] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchPortfolio();
  }, []);

  const fetchPortfolio = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getPortfolio();
      setPortfolio(data);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Unknown error';
      setError(`Failed to fetch portfolio: ${errorMessage}`);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (value, currency = 'USD') => {
    const symbol = currency === 'INR' ? '₹' : '$';
    return `${symbol}${value?.toFixed(2) || '0.00'}`;
  };

  const getCurrencySymbol = (currency) => {
    switch(currency) {
      case 'INR':
        return '₹';
      case 'USD':
        return '$';
      case 'EUR':
        return '€';
      case 'GBP':
        return '£';
      case 'JPY':
        return '¥';
      default:
        return '$';
    }
  };

  if (loading) {
    return (
      <div className="section-full">
        <h3>💼 Portfolio</h3>
        <p>Loading portfolio...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="section-full">
        <h3>💼 Portfolio</h3>
        <p className="error-text">{error}</p>
      </div>
    );
  }

  if (!portfolio || !portfolio.positions || portfolio.positions.length === 0) {
    return (
      <div className="section-full">
        <h3>💼 Portfolio</h3>
        <p>No positions in portfolio. Add stocks to get started!</p>
      </div>
    );
  }

  return (
    <div className="section-full">
      <h3>💼 Portfolio</h3>
      
      <div className="portfolio-summary">
        <div className="summary-item">
          <strong>Total Value:</strong> {formatCurrency(portfolio.total_value)}
        </div>
        <div className="summary-item">
          <strong>Total Gain/Loss:</strong>{' '}
          <span className={portfolio.total_gain_loss >= 0 ? 'gain' : 'loss'}>
            {formatCurrency(portfolio.total_gain_loss)}
            {' '}({portfolio.total_gain_loss_percent?.toFixed(2)}%)
          </span>
        </div>
      </div>

      <table className="portfolio-table">
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Quantity</th>
            <th>Buy Price</th>
            <th>Current Price</th>
            <th>Value</th>
            <th>Gain/Loss</th>
            <th>Currency</th>
          </tr>
        </thead>
        <tbody>
          {portfolio.positions.map((position, index) => {
            const currency = position.currency || 'USD';
            const currencySymbol = getCurrencySymbol(currency);
            const gainLoss = position.current_value - position.buy_value;
            const gainLossPercent = ((gainLoss / position.buy_value) * 100).toFixed(2);

            return (
              <tr key={index}>
                <td><strong>{position.symbol}</strong></td>
                <td>{position.quantity}</td>
                <td>{currencySymbol}{position.buy_price?.toFixed(2)}</td>
                <td>{currencySymbol}{position.current_price?.toFixed(2)}</td>
                <td>{currencySymbol}{position.current_value?.toFixed(2)}</td>
                <td className={gainLoss >= 0 ? 'gain' : 'loss'}>
                  {currencySymbol}{gainLoss.toFixed(2)}
                  <br />
                  <small>({gainLossPercent}%)</small>
                </td>
                <td>
                  <span className="currency-badge">
                    {currency === 'INR' ? '🇮🇳 INR' : '🇺🇸 USD'}
                  </span>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default Portfolio;