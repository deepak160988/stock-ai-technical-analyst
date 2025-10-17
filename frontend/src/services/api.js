import axios from 'axios';

const INDIAN_STOCKS = [
    'RELIANCE', 'TCS', 'HDFC', 'INFY', 'HINDUNILVR',
    'ICICIBANK', 'SBIN', 'HCLTECH', 'ITC'
];

export const isIndianStock = (symbol) => {
    return INDIAN_STOCKS.includes(symbol);
};

export const getApiBaseUrl = () => {
    return 'https://api.example.com'; // Replace with actual base URL
};

const api = {
    async getStockData(symbol) {
        try {
            const response = await axios.get(`${getApiBaseUrl()}/stocks/${symbol}`);
            return response.data;
        } catch (error) {
            console.error('Error fetching stock data:', error);
            throw error;
        }
    },

    async getLatestPrice(symbol) {
        try {
            const response = await axios.get(`${getApiBaseUrl()}/stocks/${symbol}/price`);
            return response.data;
        } catch (error) {
            console.error('Error fetching latest price:', error);
            throw error;
        }
    },

    async getIndicators(symbol) {
        try {
            const response = await axios.get(`${getApiBaseUrl()}/stocks/${symbol}/indicators`);
            return response.data;
        } catch (error) {
            console.error('Error fetching indicators:', error);
            throw error;
        }
    },

    async getRSI(symbol) {
        try {
            const response = await axios.get(`${getApiBaseUrl()}/stocks/${symbol}/rsi`);
            return response.data;
        } catch (error) {
            console.error('Error fetching RSI:', error);
            throw error;
        }
    },

    async getMACD(symbol) {
        try {
            const response = await axios.get(`${getApiBaseUrl()}/stocks/${symbol}/macd`);
            return response.data;
        } catch (error) {
            console.error('Error fetching MACD:', error);
            throw error;
        }
    },

    async getSignals(symbol) {
        try {
            const response = await axios.get(`${getApiBaseUrl()}/stocks/${symbol}/signals`);
            return response.data;
        } catch (error) {
            console.error('Error fetching signals:', error);
            throw error;
        }
    },

    async getPortfolio(userId) {
        try {
            const response = await axios.get(`${getApiBaseUrl()}/users/${userId}/portfolio`);
            return response.data;
        } catch (error) {
            console.error('Error fetching portfolio:', error);
            throw error;
        }
    },

    async getIndianStocks() {
        try {
            return INDIAN_STOCKS;
        } catch (error) {
            console.error('Error fetching Indian stocks:', error);
            throw error;
        }
    },

    async getMLPrediction(data) {
        try {
            const response = await axios.post(`${getApiBaseUrl()}/ml/predict`, data);
            return response.data;
        } catch (error) {
            console.error('Error fetching ML prediction:', error);
            throw error;
        }
    }
};

export default api;