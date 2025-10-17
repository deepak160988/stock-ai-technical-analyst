import axios from 'axios';

// Detect if we're running in GitHub Codespaces
const isCodespaces = window.location.hostname.endsWith('.app.github.dev');

// Construct the correct base URL
const getBaseURL = () => {
  if (isCodespaces) {
    // Extract the Codespaces URL base and construct the backend URL
    // Replace the port 3000 with 8000 in the current hostname
    const backendHost = window.location.hostname.replace('-3000.', '-8000.');
    return `${window.location.protocol}//${backendHost}`;
  }
  // For local development
  return 'http://localhost:8000';
};

const baseURL = getBaseURL();

// Create axios instance with base configuration
const axiosInstance = axios.create({
  baseURL: baseURL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
  // REMOVED: withCredentials: true to fix CORS wildcard issue
});

// Add request interceptor for logging
axiosInstance.interceptors.request.use(
  (config) => {
    console.log(`Making request to: ${config.baseURL}${config.url}`);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

const api = {
  // ============== US STOCKS API ==============
  
  // Get historical stock data
  getStockData: async (symbol, days = 30) => {
    try {
      const response = await axiosInstance.get(`/api/stocks/${symbol}`, {
        params: { days }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching stock data:', error);
      throw error;
    }
  },

  // Get latest stock price
  getLatestPrice: async (symbol) => {
    try {
      const response = await axiosInstance.get(`/api/stocks/${symbol}/latest`);
      return response.data;
    } catch (error) {
      console.error('Error fetching latest price:', error);
      throw error;
    }
  },

  // ============== TECHNICAL INDICATORS API ==============
  
  // Get all technical indicators
  getIndicators: async (symbol, days = 30) => {
    try {
      const response = await axiosInstance.get(`/api/indicators/${symbol}`, {
        params: { days }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching indicators:', error);
      throw error;
    }
  },

  // Get RSI indicator
  getRSI: async (symbol, days = 30, period = 14) => {
    try {
      const response = await axiosInstance.get(`/api/indicators/${symbol}/rsi`, {
        params: { days, window: period }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching RSI:', error);
      throw error;
    }
  },

  // Get MACD indicator
  getMACD: async (symbol, days = 30) => {
    try {
      const response = await axiosInstance.get(`/api/indicators/${symbol}/macd`, {
        params: { days }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching MACD:', error);
      throw error;
    }
  },

  // Get Bollinger Bands
  getBollingerBands: async (symbol, days = 30, window = 20) => {
    try {
      const response = await axiosInstance.get(`/api/indicators/${symbol}/bollinger-bands`, {
        params: { days, window }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching Bollinger Bands:', error);
      throw error;
    }
  },

  // ============== TRADING SIGNALS API ==============
  
  // Get trading signals
  getSignals: async (symbol, days = 30) => {
    try {
      const response = await axiosInstance.get(`/api/signals/${symbol}`, {
        params: { days }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching signals:', error);
      throw error;
    }
  },

  // ============== PORTFOLIO API ==============
  
  // Get portfolio data
  getPortfolio: async () => {
    try {
      const response = await axiosInstance.get('/api/portfolio/');
      return response.data;
    } catch (error) {
      console.error('Error fetching portfolio:', error);
      throw error;
    }
  },

  // Add stock to portfolio
  addToPortfolio: async (symbol, quantity, purchasePrice) => {
    try {
      const response = await axiosInstance.post('/api/portfolio/add', null, {
        params: {
          symbol,
          quantity,
          buy_price: purchasePrice
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error adding to portfolio:', error);
      throw error;
    }
  },

  // Remove stock from portfolio
  removeFromPortfolio: async (symbol) => {
    try {
      const response = await axiosInstance.delete(`/api/portfolio/${symbol}`);
      return response.data;
    } catch (error) {
      console.error('Error removing from portfolio:', error);
      throw error;
    }
  },

  // Get portfolio metrics
  getPortfolioMetrics: async () => {
    try {
      const response = await axiosInstance.get('/api/portfolio/metrics/summary');
      return response.data;
    } catch (error) {
      console.error('Error fetching portfolio metrics:', error);
      throw error;
    }
  },

  // ============== INDIAN STOCKS API ==============
  
  // Get list of all Indian stocks
  getIndianStocks: async () => {
    try {
      const response = await axiosInstance.get('/api/indian/stocks/list');
      return response.data;
    } catch (error) {
      console.error('Error fetching Indian stocks list:', error);
      throw error;
    }
  },

  // Get Indian stock historical data
  getIndianStockData: async (symbol, days = 30) => {
    try {
      const response = await axiosInstance.get(`/api/indian/stocks/${symbol}`, {
        params: { days }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching Indian stock data:', error);
      throw error;
    }
  },

  // Get Indian stock latest price
  getIndianStockLatestPrice: async (symbol) => {
    try {
      const response = await axiosInstance.get(`/api/indian/stocks/${symbol}/latest`);
      return response.data;
    } catch (error) {
      console.error('Error fetching Indian stock latest price:', error);
      throw error;
    }
  },

  // ============== NEW: INDIAN STOCK INDICATORS ==============
  
  // Get technical indicators for Indian stocks
  getIndianIndicators: async (symbol, days = 30) => {
    try {
      const response = await axiosInstance.get(`/api/indian/indicators/${symbol}`, {
        params: { days }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching Indian stock indicators:', error);
      throw error;
    }
  },

  // ============== AI & ML API ==============

  // AI Query
  aiQuery: async (question, symbol = null) => {
    try {
      const response = await axiosInstance.post('/api/ai/query', null, {
        params: { question, symbol }
      });
      return response.data;
    } catch (error) {
      console.error('Error with AI query:', error);
      throw error;
    }
  },

  // ML Prediction (if you add this endpoint later)
  getMLPrediction: async (data) => {
    try {
      const response = await axiosInstance.post('/api/ml/predict', data);
      return response.data;
    } catch (error) {
      console.error('Error fetching ML prediction:', error);
      throw error;
    }
  },

  // ============== UTILITY API ==============
  
  // Health check
  healthCheck: async () => {
    try {
      const response = await axiosInstance.get('/health');
      return response.data;
    } catch (error) {
      console.error('Error checking API health:', error);
      throw error;
    }
  }
};

export default api;

// Export the base URL for debugging
export { baseURL };