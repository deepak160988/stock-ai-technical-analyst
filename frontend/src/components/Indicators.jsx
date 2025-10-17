import React, { useState, useEffect } from 'react';
import api from '../services/api';
import './Indicators.css';

function Indicators({ symbol, isIndianStock }) {
  const [indicators, setIndicators] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (symbol) {
      fetchIndicators();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [symbol, isIndianStock]);

  const fetchIndicators = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Fetch indicators - backend should handle both US and Indian stocks
      const data = await api.getIndicators(symbol, 30);
      setIndicators(data);
    } catch (err) {
      // Check if it's a 503 Service Unavailable error
      if (err.response?.status === 503) {
        setError('Technical indicators service is currently unavailable. Please try again later.');
      } else {
        const errorMessage = err.response?.data?.detail || err.message || 'Unknown error';
        setError(`Failed to fetch indicators: ${errorMessage}`);
      }
      console.error('Indicators error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getCurrencySymbol = () => {
    return isIndianStock ? '₹' : '$';
  };

  const formatValue = (value, prefix = '') => {
    if (value === null || value === undefined || isNaN(value)) {
      return 'N/A';
    }
    return `${prefix}${parseFloat(value).toFixed(2)}`;
  };

  if (loading) {
    return (
      <div className="section indicators-section">
        <h3>📈 Technical Indicators</h3>
        <div className="indicators-loading">
          <div className="spinner"></div>
          <p>Calculating indicators...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="section indicators-section">
        <h3>📈 Technical Indicators</h3>
        <div className="error-container">
          <div className="error-icon">⚠️</div>
          <p className="error-text">{error}</p>
          <button onClick={fetchIndicators} className="retry-button">
            🔄 Retry
          </button>
        </div>
      </div>
    );
  }

  if (!indicators || !indicators.indicators) {
    return (
      <div className="section indicators-section">
        <h3>📈 Technical Indicators - {symbol}</h3>
        <div className="no-data">
          <div className="no-data-icon">📊</div>
          <p>No indicator data available for {symbol}</p>
          <button onClick={fetchIndicators} className="fetch-button">
            📈 Fetch Indicators
          </button>
        </div>
      </div>
    );
  }

  const currencySymbol = getCurrencySymbol();
  const ind = indicators.indicators;

  return (
    <div className="section indicators-section">
      <h3>📈 Technical Indicators</h3>
      <div className="symbol-header">
        <span className="symbol-name">{symbol}</span>
        <span className={`stock-flag ${isIndianStock ? 'indian-flag' : 'us-flag'}`}>
          {isIndianStock ? '🇮🇳' : '🇺🇸'}
        </span>
      </div>

      <div className="indicators-grid">
        {/* RSI Indicator */}
        <div className="indicator-card rsi-card">
          <div className="indicator-header">
            <span className="indicator-icon">📊</span>
            <span className="indicator-label">RSI</span>
          </div>
          <div className="indicator-value">
            {formatValue(ind.rsi)}
          </div>
          <div className="indicator-status">
            {ind.rsi > 70 ? (
              <span className="status-badge overbought">🔥 Overbought</span>
            ) : ind.rsi < 30 ? (
              <span className="status-badge oversold">❄️ Oversold</span>
            ) : (
              <span className="status-badge neutral">✅ Neutral</span>
            )}
          </div>
        </div>

        {/* MACD Indicator */}
        <div className="indicator-card macd-card">
          <div className="indicator-header">
            <span className="indicator-icon">📉</span>
            <span className="indicator-label">MACD</span>
          </div>
          <div className="indicator-value">
            {formatValue(ind.macd)}
          </div>
          <div className="indicator-status">
            {ind.macd > 0 ? (
              <span className="status-badge bullish">📈 Bullish</span>
            ) : (
              <span className="status-badge bearish">📉 Bearish</span>
            )}
          </div>
        </div>

        {/* SMA 20 */}
        <div className="indicator-card sma-card">
          <div className="indicator-header">
            <span className="indicator-icon">📍</span>
            <span className="indicator-label">SMA (20)</span>
          </div>
          <div className="indicator-value">
            {formatValue(ind.sma_20, currencySymbol)}
          </div>
          <div className="indicator-description">
            Simple Moving Average
          </div>
        </div>

        {/* EMA 20 */}
        <div className="indicator-card ema-card">
          <div className="indicator-header">
            <span className="indicator-icon">📌</span>
            <span className="indicator-label">EMA (20)</span>
          </div>
          <div className="indicator-value">
            {formatValue(ind.ema_20, currencySymbol)}
          </div>
          <div className="indicator-description">
            Exponential Moving Average
          </div>
        </div>

        {/* Bollinger Upper */}
        <div className="indicator-card bb-upper-card">
          <div className="indicator-header">
            <span className="indicator-icon">⬆️</span>
            <span className="indicator-label">BB Upper</span>
          </div>
          <div className="indicator-value">
            {formatValue(ind.bb_upper, currencySymbol)}
          </div>
          <div className="indicator-description">
            Bollinger Band Upper
          </div>
        </div>

        {/* Bollinger Lower */}
        <div className="indicator-card bb-lower-card">
          <div className="indicator-header">
            <span className="indicator-icon">⬇️</span>
            <span className="indicator-label">BB Lower</span>
          </div>
          <div className="indicator-value">
            {formatValue(ind.bb_lower, currencySymbol)}
          </div>
          <div className="indicator-description">
            Bollinger Band Lower
          </div>
        </div>
      </div>

      <div className="indicators-footer">
        <p className="data-info">
          <span className="currency-badge-small">
            💱 {isIndianStock ? 'INR (₹)' : 'USD ($)'}
          </span>
        </p>
        <p className="data-points">
          📊 {indicators.data_points || 'N/A'} data points analyzed
        </p>
      </div>
    </div>
  );
}

export default Indicators;