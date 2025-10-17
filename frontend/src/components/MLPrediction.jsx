import React, { useState } from 'react';

function MLPrediction({ symbol, isIndianStock }) {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const getCurrencyDisplay = () => {
    if (isIndianStock) {
      return { symbol: '₹', label: 'INR' };
    } else {
      return { symbol: '$', label: 'USD' };
    }
  };

  const currency = getCurrencyDisplay();

  const handlePredict = async () => {
    setLoading(true);
    // Simulate prediction
    setTimeout(() => {
      setPrediction({
        nextDay: Math.random() * 100 + 100,
        confidence: Math.random() * 30 + 70
      });
      setLoading(false);
    }, 1000);
  };

  return (
    <div className="section">
      <h3>🤖 ML Prediction - {symbol}</h3>
      <button onClick={handlePredict} disabled={loading} className="predict-button">
        {loading ? 'Predicting...' : 'Generate Prediction'}
      </button>
      
      {prediction && (
        <div className="prediction-result">
          <p>
            <strong>Next Day Prediction:</strong> {currency.symbol}{prediction.nextDay.toFixed(2)} {currency.label}
          </p>
          <p>
            <strong>Confidence:</strong> {prediction.confidence.toFixed(1)}%
          </p>
          <p className="currency-note">
            <small>💱 Currency: {isIndianStock ? 'Indian Rupee (₹)' : 'US Dollar ($)'}</small>
          </p>
        </div>
      )}
    </div>
  );
}

export default MLPrediction;