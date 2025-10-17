import axios from 'axios';

const apiClient = axios.create({
    baseURL: 'https://api.example.com', // replace with your API base URL
    timeout: 1000,
});

const api = {
    async getStockData(stockSymbol) {
        try {
            const response = await apiClient.get(`/stocks/${stockSymbol}`);
            return response.data;
        } catch (error) {
            console.error('Error fetching stock data:', error);
            throw error;
        }
    },

    async getLatestPrice(stockSymbol) {
        try {
            const response = await apiClient.get(`/stocks/${stockSymbol}/latest-price`);
            return response.data;
        } catch (error) {
            console.error('Error fetching latest price:', error);
            throw error;
        }
    },

    async getIndicators(stockSymbol) {
        try {
            const response = await apiClient.get(`/stocks/${stockSymbol}/indicators`);
            return response.data;
        } catch (error) {
            console.error('Error fetching indicators:', error);
            throw error;
        }
    },

    async getRSI(stockSymbol) {
        try {
            const response = await apiClient.get(`/stocks/${stockSymbol}/rsi`);
            return response.data;
        } catch (error) {
            console.error('Error fetching RSI:', error);
            throw error;
        }
    },

    async getMACD(stockSymbol) {
        try {
            const response = await apiClient.get(`/stocks/${stockSymbol}/macd`);
            return response.data;
        } catch (error) {
            console.error('Error fetching MACD:', error);
            throw error;
        }
    },

    async getSignals(stockSymbol) {
        try {
            const response = await apiClient.get(`/stocks/${stockSymbol}/signals`);
            return response.data;
        } catch (error) {
            console.error('Error fetching signals:', error);
            throw error;
        }
    },

    async getPortfolio(userId) {
        try {
            const response = await apiClient.get(`/users/${userId}/portfolio`);
            return response.data;
        } catch (error) {
            console.error('Error fetching portfolio:', error);
            throw error;
        }
    },

    async getIndianStocks() {
        try {
            const response = await apiClient.get('/stocks/indian');
            return response.data;
        } catch (error) {
            console.error('Error fetching Indian stocks:', error);
            throw error;
        }
    },

    async getMLPrediction(data) {
        try {
            const response = await apiClient.post('/ml/predict', data);
            return response.data;
        } catch (error) {
            console.error('Error fetching ML prediction:', error);
            throw error;
        }
    },
};

export default api;