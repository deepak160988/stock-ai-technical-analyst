import React, { useState, useEffect } from 'react';
import api from '../services/api';
import './Indicators.css';

function Indicators({ symbol, isIndianStock, stockDataLoaded }) {
  const [indicators, setIndicators] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [errorType, setErrorType] = useState(null);

  useEffect(() => {
    if (symbol && stockDataLoaded) {
      fetchIndicators();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [symbol, isIndianStock, stockDataLoaded]);

  const fetchIndicators = async () => {
    try {
      setLoading(true);
      setError(null);
      setErrorType(null);
      
      let data;
      if (isIndianStock) {
        console.log(`Fetching Indian stock indicators for ${symbol}`);
        data = await api.getIndianIndicators(symbol, 30);
      } else {
        console.log(`Fetching US stock indicators for ${symbol}`);
        data = await api.getIndicators(symbol, 30);
      }
      
      setIndicators(data);
    } catch (err) {
      console.error('Indicators error:', err);
      
      if (err.response?.status === 503) {
        setErrorType('service');
        setError({
          title: 'Service Unavailable',
          message: 'The technical indicators service is currently unavailable. This usually happens when the backend service has not started properly.',
          suggestions: [
            'Check if the backend server is running on port 8000',
            'Verify that all required Python packages are installed',
            'Check the backend logs for service initialization errors'
          ]
        });
      } else if (err.response?.status === 404) {
        setErrorType('notfound');
        setError({
          title: 'Stock Not Found',
          message: `Unable to find data for "${symbol}". This stock symbol may not exist or is not supported.`,
          suggestions: [
            'Check if the stock symbol is spelled correctly',
            isIndianStock 
              ? 'Verify that this is a valid NSE (National Stock Exchange) symbol'
              : 'Verify that this is a valid US stock ticker symbol',
            'Try searching for a different stock symbol',
            'Common examples: ' + (isIndianStock ? 'TCS, RELIANCE, INFY' : 'AAPL, GOOGL, MSFT')
          ]
        });
      } else if (err.code === 'ERR_NETWORK' || err.message.includes('Network Error')) {
        setErrorType('network');
        setError({
          title: 'Network Connection Error',
          message: 'Unable to connect to the backend API. Please check your network connection.',
          suggestions: [
            'Verify your internet connection is working',
            'Check if the backend server is accessible',
            'Ensure port 8000 is not blocked by firewall',
            'In GitHub Codespaces, make sure port 8000 is set to PUBLIC'
          ]
        });
      } else if (err.response?.status === 500) {
        setErrorType('server');
        setError({
          title: 'Server Error',
          message: 'An internal server error occurred while calculating indicators.',
          suggestions: [
            'This is likely a temporary issue',
            'Check the backend logs for detailed error information',
            'Try refreshing the page',
            'If the problem persists, contact support'
          ]
        });
      } else {
        setErrorType('unknown');
        const errorMessage = err.response?.data?.detail || err.message || 'Unknown error';
        setError({
          title: 'Unexpected Error',
          message: errorMessage,
          suggestions: [
            'Try refreshing the page',
            'Check your browser console for more details',
            'If the problem persists, please report this issue'
          ]
        });
      }
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

  const formatNumber = (value) => {
    if (value === null || value === undefined || isNaN(value)) {
      return 'N/A';
    }
    return parseFloat(value).toFixed(2);
  };

  const getRSISignal = (rsi) => {
    if (!rsi) return { text: 'N/A', color: 'neutral' };
    if (rsi > 70) return { text: 'Overbought', color: 'danger' };
    if (rsi < 30) return { text: 'Oversold', color: 'success' };
    return { text: 'Neutral', color: 'neutral' };
  };

  const getMACDSignal = (macd) => {
    if (!macd) return { text: 'N/A', color: 'neutral' };
    if (macd > 0) return { text: 'Bullish', color: 'success' };
    return { text: 'Bearish', color: 'danger' };
  };

  const getErrorIcon = () => {
    switch (errorType) {
      case 'notfound':
        return '🔍';
      case 'service':
        return '⚙️';
      case 'network':
        return '📡';
      case 'server':
        return '🔥';
      default:
        return '⚠️';
    }
  };

  if (!stockDataLoaded) {
    return (
      <div className="section indicators-section">
        <h3>📈 Technical Indicators</h3>
        <div className="waiting-container">
          <div className="waiting-icon">⏳</div>
          <p className="waiting-text">Waiting for stock data...</p>
          <p className="waiting-subtext">Indicators will load automatically once stock data is available</p>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="section indicators-section">
        <h3>📈 Technical Indicators</h3>
        <div className="indicators-loading">
          <div className="spinner"></div>
          <p className="loading-text">Calculating indicators for {symbol}...</p>
          <p className="loading-subtext">This may take a few seconds</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="section indicators-section">
        <h3>📈 Technical Indicators</h3>
        <div className={`error-container error-type-${errorType}`}>
          <div className="error-icon-large">{getErrorIcon()}</div>
          <div className="error-content">
            <h4 className="error-title">{error.title}</h4>
            <p className="error-message">{error.message}</p>
            
            {error.suggestions && error.suggestions.length > 0 && (
              <div className="error-suggestions">
                <p className="suggestions-title">💡 Suggestions:</p>
                <ul className="suggestions-list">
                  {error.suggestions.map((suggestion, index) => (
                    <li key={index}>{suggestion}</li>
                  ))}
                </ul>
              </div>
            )}

            <div className="error-actions">
              <button onClick={fetchIndicators} className="retry-button">
                🔄 Retry
              </button>
              {errorType === 'notfound' && (
                <button 
                  onClick={() => window.location.reload()} 
                  className="secondary-button"
                >
                  🏠 Go Back
                </button>
              )}
            </div>

            <div className="error-tech-details">
              <details>
                <summary>Technical Details</summary>
                <div className="tech-info">
                  <p><strong>Symbol:</strong> {symbol}</p>
                  <p><strong>Stock Type:</strong> {isIndianStock ? 'Indian (NSE)' : 'US Stock'}</p>
                  <p><strong>Error Type:</strong> {errorType}</p>
                  <p><strong>Timestamp:</strong> {new Date().toLocaleString()}</p>
                </div>
              </details>
            </div>
          </div>
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
          <p className="no-data-text">No indicator data available for {symbol}</p>
          <p className="no-data-subtext">Click the button below to fetch indicators</p>
          <button onClick={fetchIndicators} className="fetch-button">
            📈 Fetch Indicators
          </button>
        </div>
      </div>
    );
  }

  const currencySymbol = getCurrencySymbol();
  const ind = indicators.indicators;
  const rsiSignal = getRSISignal(ind.rsi);
  const macdSignal = getMACDSignal(ind.macd);

  return (
    <div className="section indicators-section">
      {/* Header */}
      <div className="indicators-header">
        <div className="header-left">
          <h3>📈 Technical Indicators</h3>
          <span className="symbol-badge">{symbol}</span>
        </div>
        <div className="header-right">
          <span className={`country-flag ${isIndianStock ? 'indian' : 'us'}`}>
            {isIndianStock ? '🇮🇳 INR' : '🇺🇸 USD'}
          </span>
        </div>
      </div>

      {/* Main Indicators Grid */}
      <div className="main-indicators">
        {/* RSI Card */}
        <div className={`main-card rsi-card ${rsiSignal.color}`}>
          <div className="card-header">
            <span className="card-icon">📊</span>
            <span className="card-title">RSI (14)</span>
          </div>
          <div className="card-value">{formatNumber(ind.rsi)}</div>
          <div className="card-footer">
            <span className={`signal-badge ${rsiSignal.color}`}>
              {rsiSignal.text}
            </span>
            <span className="card-description">Relative Strength Index</span>
          </div>
          <div className="rsi-meter">
            <div className="meter-bar">
              <div 
                className="meter-fill" 
                style={{ width: `${Math.min(ind.rsi || 0, 100)}%` }}
              ></div>
              <div className="meter-marker oversold" style={{ left: '30%' }}>30</div>
              <div className="meter-marker overbought" style={{ left: '70%' }}>70</div>
            </div>
          </div>
        </div>

        {/* MACD Card */}
        <div className={`main-card macd-card ${macdSignal.color}`}>
          <div className="card-header">
            <span className="card-icon">📉</span>
            <span className="card-title">MACD</span>
          </div>
          <div className="card-value">{formatNumber(ind.macd)}</div>
          <div className="card-footer">
            <span className={`signal-badge ${macdSignal.color}`}>
              {macdSignal.text}
            </span>
            <span className="card-description">Trend Momentum</span>
          </div>
          <div className="macd-details">
            <div className="detail-row">
              <span className="detail-label">Signal:</span>
              <span className="detail-value">{formatNumber(ind.macd_signal)}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Histogram:</span>
              <span className="detail-value">{formatNumber(ind.macd_histogram)}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Moving Averages Section */}
      <div className="section-title">
        <span className="title-icon">📍</span>
        <span>Moving Averages</span>
      </div>
      <div className="indicators-grid-2col">
        <div className="indicator-box">
          <div className="box-label">SMA (20)</div>
          <div className="box-value">{formatValue(ind.sma_20, currencySymbol)}</div>
          <div className="box-subtitle">Simple Moving Average</div>
        </div>

        <div className="indicator-box">
          <div className="box-label">SMA (50)</div>
          <div className="box-value">{formatValue(ind.sma_50, currencySymbol)}</div>
          <div className="box-subtitle">Simple Moving Average</div>
        </div>

        <div className="indicator-box">
          <div className="box-label">EMA (20)</div>
          <div className="box-value">{formatValue(ind.ema_20, currencySymbol)}</div>
          <div className="box-subtitle">Exponential Moving Average</div>
        </div>

        <div className="indicator-box">
          <div className="box-label">EMA (50)</div>
          <div className="box-value">{formatValue(ind.ema_50, currencySymbol)}</div>
          <div className="box-subtitle">Exponential Moving Average</div>
        </div>
      </div>

      {/* Bollinger Bands Section */}
      <div className="section-title">
        <span className="title-icon">📏</span>
        <span>Bollinger Bands</span>
      </div>
      <div className="indicators-grid-3col">
        <div className="indicator-box bb-upper">
          <div className="box-label">Upper Band</div>
          <div className="box-value">{formatValue(ind.bb_upper, currencySymbol)}</div>
        </div>

        <div className="indicator-box bb-middle">
          <div className="box-label">Middle Band</div>
          <div className="box-value">{formatValue(ind.bb_middle, currencySymbol)}</div>
        </div>

        <div className="indicator-box bb-lower">
          <div className="box-label">Lower Band</div>
          <div className="box-value">{formatValue(ind.bb_lower, currencySymbol)}</div>
        </div>
      </div>

      {/* Additional Indicators Section */}
      <div className="section-title">
        <span className="title-icon">📐</span>
        <span>Other Indicators</span>
      </div>
      <div className="indicators-grid-3col">
        <div className="indicator-box">
          <div className="box-label">Stochastic %K</div>
          <div className="box-value">{formatNumber(ind.stochastic_k)}</div>
        </div>

        <div className="indicator-box">
          <div className="box-label">Stochastic %D</div>
          <div className="box-value">{formatNumber(ind.stochastic_d)}</div>
        </div>

        <div className="indicator-box">
          <div className="box-label">ATR (14)</div>
          <div className="box-value">{formatNumber(ind.atr)}</div>
        </div>
      </div>

      {/* Footer Info */}
      <div className="indicators-footer">
        <div className="footer-info">
          <span className="info-icon">📊</span>
          <span>{indicators.data_points || 'N/A'} data points analyzed</span>
        </div>
        <div className="footer-info">
          <span className="info-icon">💱</span>
          <span>Currency: {isIndianStock ? 'Indian Rupee (₹)' : 'US Dollar ($)'}</span>
        </div>
      </div>
    </div>
  );
}

export default Indicators;