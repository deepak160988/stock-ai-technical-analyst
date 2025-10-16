import React from 'react';

function Indicators({ symbol }) {
  return (
    <div className="section">
      <h3>📈 Technical Indicators</h3>
      <p>Symbol: {symbol}</p>
      <ul>
        <li>RSI: Loading...</li>
        <li>MACD: Loading...</li>
        <li>Bollinger Bands: Loading...</li>
      </ul>
    </div>
  );
}

export default Indicators;
