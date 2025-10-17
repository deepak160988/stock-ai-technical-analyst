import React from 'react';

function StockChart({ symbol, data, isIndianStock }) {
  if (!data || !data.prices) {
    return (
      <div className="section-full">
        <h3>📊 Stock Chart - {symbol}</h3>
        <p>Loading chart data...</p>
      </div>
    );
  }

  // Determine currency symbol and label based on stock type
  const getCurrencyDisplay = () => {
    if (isIndianStock) {
      return {
        symbol: '₹',
        label: 'INR',
        price: data.current_price_inr || data.current_price
      };
    } else {
      return {
        symbol: '$',
        label: 'USD',
        price: data.current_price
      };
    }
  };

  const currency = getCurrencyDisplay();

  return (
    <div className="section-full">
      <h3>📊 Stock Chart - {symbol}</h3>
      <div className="stock-info">
        <p className="current-price">
          <strong>Current Price:</strong> {currency.symbol}{currency.price?.toFixed(2)} {currency.label}
        </p>
        <p>
          <strong>Exchange:</strong> {isIndianStock ? '🇮🇳 NSE' : '🇺🇸 NASDAQ/NYSE'}
        </p>
        <p>
          <strong>Data Points:</strong> {data.data_points}
        </p>
        {data.last_updated && (
          <p className="last-updated">
            <strong>Last Updated:</strong> {new Date(data.last_updated).toLocaleString()}
          </p>
        )}
      </div>
      {/* Chart will be rendered here with recharts */}
    </div>
  );
}

export default StockChart;