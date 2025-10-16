import React from 'react';

function StockChart({ symbol, data }) {
  if (!data || !data.prices) {
    return (
      <div className="section-full">
        <h3>📊 Stock Chart - {symbol}</h3>
        <p>Loading chart data...</p>
      </div>
    );
  }

  return (
    <div className="section-full">
      <h3>📊 Stock Chart - {symbol}</h3>
      <p>Current Price: ${data.current_price?.toFixed(2)}</p>
      <p>Data Points: {data.data_points}</p>
      {/* Chart will be rendered here with recharts */}
    </div>
  );
}

export default StockChart;
