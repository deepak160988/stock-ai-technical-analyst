// src/services/api.js
import axios from 'axios';

// Use environment variable if provided (Codespaces forwarded URL), otherwise default to relative path for proxy
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || '/api';

const api = {
  // Stock Data
  getStockData: async (symbol, days = 30) => {
    try {
      const url = `${API_BASE_URL}/stocks/${symbol}?days=${days}`;
      const response = await axios.get(url);
      return response.data;
    } catch (error) {
      console.error('Error fetching stock data:', error);
      throw error;
    }
  },

  getLatestPrice: async (symbol) => {
    try {
      const url = `${API_BASE_URL}/stocks/${symbol}/latest`;
      const response = await axios.get(url);
      return response.data;
    } catch (error) {
      console.error('Error fetching latest price:', error);
      throw error;
    }
  },

  // Indicators
  getIndicators: async (symbol, days = 30) => {
    try {
      const url = `${API_BASE_URL}/indicators/${symbol}?days=${days}`;
      const response = await axios.get(url);
      return response.data;
    } catch (error) {
      console.error('Error fetching indicators:', error);
      throw error;
    }
  },

  getRSI: async (symbol, window = 14, days = 30) => {
    try {
      const url = `${API_BASE_URL}/indicators/${symbol}/rsi?window=${window}&days=${days}`;
      const response = await axios.get(url);
      return response.data;
    } catch (error) {
      console.error('Error fetching RSI:', error);
      throw error;
    }
  },

  getMACD: async (symbol, days = 30) => {
    try {
      const url = `${API_BASE_URL}/indicators/${symbol}/macd?days=${days}`;
      const response = await axios.get(url);
      return response.data;
    } catch (error) {
      console.error('Error fetching MACD:', error);
      throw error;
    }
  },

  // Signals
  getSignals: async (symbol, days = 30) => {
    try {
      const url = `${API_BASE_URL}/signals/${symbol}?days=${days}`;
      const response = await axios.get(url);
      return response.data;
    } catch (error) {
      console.error('Error fetching signals:', error);
      throw error;
    }
  },

  // Portfolio
  getPortfolio: async () => {
    try {
      const url = `${API_BASE_URL}/portfolio/`;
      const response = await axios.get(url);
      return response.data;
    } catch (error) {
      console.error('Error fetching portfolio:', error);
      throw error;
    }
  },

  // Indian Stocks
  getIndianStocks: async () => {
    try {
      const url = `${API_BASE_URL}/indian/stocks/list`;
      const response = await axios.get(url);
      return response.data;
    } catch (error) {
      console.error('Error fetching Indian stocks:', error);
      throw error;
    }
  },

  // ML Prediction
  getMLPrediction: async (symbol, days = 7) => {
    try {
      const url = `${API_BASE_URL}/ml/predict?symbol=${symbol}&days=${days}`;
      const response = await axios.get(url);
      return response.data;
    } catch (error) {
      console.error('Error fetching ML prediction:', error);
      throw error;
    }
  }
};

export default api;