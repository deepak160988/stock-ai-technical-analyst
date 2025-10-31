import React from 'react';
import './TimeframeSelector.css';

/**
 * TimeframeSelector component - allows users to select a timeframe for stock data
 * @param {Object} props
 * @param {string} props.value - Currently selected timeframe
 * @param {function} props.onChange - Callback when timeframe changes
 * @param {boolean} props.disabled - Whether the selector is disabled
 */
function TimeframeSelector({ value = '1mo', onChange, disabled = false }) {
  const timeframes = [
    { value: '1d', label: '1D' },
    { value: '5d', label: '5D' },
    { value: '1mo', label: '1M' },
    { value: '3mo', label: '3M' },
    { value: '6mo', label: '6M' },
    { value: '1y', label: '1Y' },
    { value: '5y', label: '5Y' },
    { value: 'max', label: 'Max' }
  ];

  const handleChange = (newValue) => {
    if (!disabled && onChange) {
      onChange(newValue);
    }
  };

  return (
    <div className="timeframe-selector">
      <label className="timeframe-label">Timeframe:</label>
      <div className="timeframe-buttons">
        {timeframes.map((tf) => (
          <button
            key={tf.value}
            className={`timeframe-button ${value === tf.value ? 'active' : ''} ${disabled ? 'disabled' : ''}`}
            onClick={() => handleChange(tf.value)}
            disabled={disabled}
            title={`View ${tf.label} data`}
          >
            {tf.label}
          </button>
        ))}
      </div>
    </div>
  );
}

export default TimeframeSelector;
