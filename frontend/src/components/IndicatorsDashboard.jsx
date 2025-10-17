import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import api from '../services/api';

function IndicatorsDashboard({ symbol }) {
  const [indicators, setIndicators] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchIndicators = async () => {
      try {
        setLoading(true);
        const response = await api.getIndicators(symbol);
        setIndicators(response);
      } catch (err) {
        setError('Error fetching indicators');
      } finally {
        setLoading(false);
      }
    };

    fetchIndicators();
  }, [symbol]);

  if (loading) return <div className="loading">Loading indicators...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="indicators-dashboard">
      <h1>Technical Indicators - {symbol}</h1>
      
      {indicators && (
        <div className="indicators-grid">
          <div className="indicator-card">
            <h3>Price Action</h3>
            <div className="chart-container">
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={indicators.indicators?.prices || []}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="close" stroke="#8884d8" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="indicator-card">
            <h3>RSI Indicator</h3>
            <p>Relative Strength Index helps identify overbought/oversold conditions</p>
            <div className="metric">RSI is a momentum oscillator</div>
          </div>

          <div className="indicator-card">
            <h3>MACD</h3>
            <p>Moving Average Convergence Divergence - trend following indicator</p>
            <div className="metric">MACD crosses signal line for trading signals</div>
          </div>

          <div className="indicator-card">
            <h3>Bollinger Bands</h3>
            <p>Volatility and price level indicator</p>
            <div className="metric">Shows support/resistance levels</div>
          </div>
        </div>
      )}
    </div>
  );
}

export default IndicatorsDashboard;
