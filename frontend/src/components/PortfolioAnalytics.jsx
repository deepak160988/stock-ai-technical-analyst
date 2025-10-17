import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import api from '../services/api';

const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff7c7c', '#a4de6c'];

function PortfolioAnalytics() {
  const [portfolio, setPortfolio] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [sectorData, setSectorData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const portfolioRes = await api.getPortfolio();
        setPortfolio(portfolioRes);
        
        // Only fetch analytics if the endpoint exists
        try {
          const analyticsRes = await api.getPortfolioMetrics();
          setAnalytics(analyticsRes);
        } catch (err) {
          console.log('Analytics endpoint not available:', err);
        }
        
        // Sector data would need a separate endpoint - skipping for now
      } catch (err) {
        console.error('Error fetching portfolio data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div className="loading">Loading portfolio...</div>;

  return (
    <div className="portfolio-analytics">
      <h1>💼 Portfolio Analytics</h1>

      <div className="metrics-grid">
        {analytics && (
          <>
            <div className="metric-card">
              <h3>Sharpe Ratio</h3>
              <div className="value">{analytics.sharpe_ratio?.toFixed(2) || 'N/A'}</div>
              <p>Risk-adjusted return</p>
            </div>

            <div className="metric-card">
              <h3>Sortino Ratio</h3>
              <div className="value">{analytics.sortino_ratio?.toFixed(2) || 'N/A'}</div>
              <p>Downside risk adjusted</p>
            </div>

            <div className="metric-card">
              <h3>Max Drawdown</h3>
              <div className="value">{(analytics.max_drawdown * 100)?.toFixed(2) || 'N/A'}%</div>
              <p>Largest peak-to-trough</p>
            </div>

            <div className="metric-card">
              <h3>Value at Risk (95%)</h3>
              <div className="value">{(analytics.var_95 * 100)?.toFixed(2) || 'N/A'}%</div>
              <p>Potential loss</p>
            </div>
          </>
        )}
      </div>

      <div className="charts-grid">
        {sectorData && sectorData.length > 0 && (
          <div className="chart-container">
            <h2>Sector Allocation</h2>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={sectorData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value.toFixed(1)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {sectorData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => `${value.toFixed(2)}%`} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        )}

        {portfolio && (
          <div className="chart-container">
            <h2>Holdings Summary</h2>
            <div className="holdings-list">
              {portfolio.positions?.map((pos, idx) => (
                <div key={idx} className="holding-item">
                  <span className="symbol">{pos.symbol}</span>
                  <span className="value">₹{pos.current_value?.toFixed(2) || 'N/A'}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default PortfolioAnalytics;
