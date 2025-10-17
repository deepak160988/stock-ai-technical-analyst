const isCodespaces = window.location.hostname.endsWith('.app.github.dev');
const baseURL = isCodespaces ? 'http://localhost:8000' : 'http://localhost:3000';

const api = {
    getStockData: async (symbol) => {
        try {
            const response = await fetch(`${baseURL}/stock/${symbol}`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching stock data:', error);
            throw error;
        }
    },
    getLatestPrice: async (symbol) => {
        try {
            const response = await fetch(`${baseURL}/stock/${symbol}/latest`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching latest price:', error);
            throw error;
        }
    },
    getIndicators: async (symbol) => {
        try {
            const response = await fetch(`${baseURL}/stock/${symbol}/indicators`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching indicators:', error);
            throw error;
        }
    },
    getRSI: async (symbol) => {
        try {
            const response = await fetch(`${baseURL}/stock/${symbol}/rsi`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching RSI:', error);
            throw error;
        }
    },
    getMACD: async (symbol) => {
        try {
            const response = await fetch(`${baseURL}/stock/${symbol}/macd`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching MACD:', error);
            throw error;
        }
    },
    getSignals: async (symbol) => {
        try {
            const response = await fetch(`${baseURL}/stock/${symbol}/signals`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching signals:', error);
            throw error;
        }
    },
    getPortfolio: async () => {
        try {
            const response = await fetch(`${baseURL}/portfolio`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching portfolio:', error);
            throw error;
        }
    },
    getIndianStocks: async () => {
        try {
            const response = await fetch(`${baseURL}/indian-stocks`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching Indian stocks:', error);
            throw error;
        }
    },
    getMLPrediction: async (data) => {
        try {
            const response = await fetch(`${baseURL}/ml/predict`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            return await response.json();
        } catch (error) {
            console.error('Error fetching ML prediction:', error);
            throw error;
        }
    }
};

export default api;