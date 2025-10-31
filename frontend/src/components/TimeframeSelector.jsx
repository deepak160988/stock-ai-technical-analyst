import React from 'react';
import './TimeframeSelector.css';

const TimeframeSelector = ({ selectedTimeframe, onTimeframeChange }) => {
  const timeframes = [
    { value: '1m', label: '1m' },
    { value: '3m', label: '3m' },
    { value: '5m', label: '5m' },
    { value: '15m', label: '15m' },
    { value: '30m', label: '30m' },
    { value: '1h', label: '1h' },
    { value: '4h', label: '4h' },
    { value: '1d', label: '1d' },
    { value: '1w', label: '1w' },
    { value: '1mo', label: '1mo' }
  ];

  return (
    <div className="timeframe-selector">
      <div className="timeframe-buttons">
        {timeframes.map((tf) => (
          <button
            key={tf.value}
            className={`timeframe-button ${selectedTimeframe === tf.value ? 'active' : ''}`}
            onClick={() => onTimeframeChange(tf.value)}
            title={`Select ${tf.label} timeframe`}
          >
            {tf.label}
          </button>
        ))}
      </div>
    </div>
  );
};

export default TimeframeSelector;
