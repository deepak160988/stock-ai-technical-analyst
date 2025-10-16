import React from 'react';

function MLPrediction({ symbol }) {
  return (
    <div className="section">
      <h3>🤖 ML Price Prediction</h3>
      <p>Symbol: {symbol}</p>
      <p>Next 7 Days Forecast</p>
      <p style={{ fontSize: '24px', fontWeight: 'bold' }}>Loading predictions...</p>
    </div>
  );
}

export default MLPrediction;
