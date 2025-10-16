import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = {
  // Stock Data
  getStockData: async (symbol, days = 30) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/stocks/${symbol}?days=${days}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching stock data:', error);
      throw error;
    }
  },

  getLatestPrice: async (symbol) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/stocks/${symbol}/latest`);
      return response.data;
    } catch (error) {
      console.error('Error fetching latest price:', error);
      throw error;
    }
  },

  // Indicators
  getIndicators: async (symbol, days = 30) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/indicators/${symbol}?days=${days}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching indicators:', error);
      throw error;
    }
  },

  getRSI: async (symbol) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/indicators/${symbol}/rsi`);
      return response.data;
    } catch (error) {
      console.error('Error fetching RSI:', error);
      throw error;
    }
  },

  getMACD: async (symbol) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/indicators/${symbol}/macd`);
      return response.data;
    } catch (error) {
      console.error('Error fetching MACD:', error);
      throw error;
    }
  },

  // Signals
  getSignals: async (symbol) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/signals/${symbol}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching signals:', error);
      throw error;
    }
  },

  // Portfolio
  getPortfolio: async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/portfolio/`);
      return response.data;
    } catch (error) {
      console.error('Error fetching portfolio:', error);
      throw error;
    }
  },

  // Indian Stocks
  getIndianStocks: async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/indian/stocks/list`);
      return response.data;
    } catch (error) {
      console.error('Error fetching Indian stocks:', error);
      throw error;
    }
  },
};

export default api;
