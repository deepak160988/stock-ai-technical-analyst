// Detect if running in GitHub Codespaces
const isCodespaces = window.location.hostname.endsWith('.app.github.dev');

// In Codespaces, use relative URLs (proxy handles routing to backend)
// In local dev, use localhost:8000
const baseURL = isCodespaces ? '' : 'http://localhost:8000';

const api = {
    getStockData: async (symbol, days = 365) => {
        try {
            const response = await fetch(`${baseURL}/api/stocks/${symbol}?days=${days}`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching stock data:', error);
            throw error;
        }
    },
    getLatestPrice: async (symbol) => {
        try {
            const response = await fetch(`${baseURL}/api/stocks/${symbol}/latest`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching latest price:', error);
            throw error;
        }
    },
    getIndicators: async (symbol, days = 365) => {
        try {
            const response = await fetch(`${baseURL}/api/indicators/${symbol}?days=${days}`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching indicators:', error);
            throw error;
        }
    },
    getRSI: async (symbol, days = 365, window = 14) => {
        try {
            const response = await fetch(`${baseURL}/api/indicators/${symbol}/rsi?days=${days}&window=${window}`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching RSI:', error);
            throw error;
        }
    },
    getMACD: async (symbol, days = 365) => {
        try {
            const response = await fetch(`${baseURL}/api/indicators/${symbol}/macd?days=${days}`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching MACD:', error);
            throw error;
        }
    },
    getBollingerBands: async (symbol, days = 365, window = 20) => {
        try {
            const response = await fetch(`${baseURL}/api/indicators/${symbol}/bollinger-bands?days=${days}&window=${window}`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching Bollinger Bands:', error);
            throw error;
        }
    },
    getSignals: async (symbol, days = 365) => {
        try {
            const response = await fetch(`${baseURL}/api/signals/${symbol}?days=${days}`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching signals:', error);
            throw error;
        }
    },
    getPortfolio: async () => {
        try {
            const response = await fetch(`${baseURL}/api/portfolio/`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching portfolio:', error);
            throw error;
        }
    },
    addPortfolioPosition: async (symbol, quantity, buyPrice) => {
        try {
            const response = await fetch(`${baseURL}/api/portfolio/add?symbol=${symbol}&quantity=${quantity}&buy_price=${buyPrice}`, {
                method: 'POST'
            });
            return await response.json();
        } catch (error) {
            console.error('Error adding portfolio position:', error);
            throw error;
        }
    },
    removePortfolioPosition: async (symbol) => {
        try {
            const response = await fetch(`${baseURL}/api/portfolio/${symbol}`, {
                method: 'DELETE'
            });
            return await response.json();
        } catch (error) {
            console.error('Error removing portfolio position:', error);
            throw error;
        }
    },
    getPortfolioMetrics: async () => {
        try {
            const response = await fetch(`${baseURL}/api/portfolio/metrics/summary`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching portfolio metrics:', error);
            throw error;
        }
    },
    getIndianStocksList: async () => {
        try {
            const response = await fetch(`${baseURL}/api/indian/stocks/list`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching Indian stocks list:', error);
            throw error;
        }
    },
    getIndianStockData: async (symbol, days = 365) => {
        try {
            const response = await fetch(`${baseURL}/api/indian/stocks/${symbol}?days=${days}`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching Indian stock data:', error);
            throw error;
        }
    },
    getIndianStockLatestPrice: async (symbol) => {
        try {
            const response = await fetch(`${baseURL}/api/indian/stocks/${symbol}/latest`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching Indian stock latest price:', error);
            throw error;
        }
    },
    queryAI: async (question, symbol = null) => {
        try {
            const url = symbol 
                ? `${baseURL}/api/ai/query?question=${encodeURIComponent(question)}&symbol=${symbol}`
                : `${baseURL}/api/ai/query?question=${encodeURIComponent(question)}`;
            const response = await fetch(url, { method: 'POST' });
            return await response.json();
        } catch (error) {
            console.error('Error querying AI:', error);
            throw error;
        }
    }
};

export default api;