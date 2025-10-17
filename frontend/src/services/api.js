import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
    baseURL: '/api',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// API methods
export const getStockData = async (symbol, days = 365) => {
    const response = await api.get(`/stocks/${symbol}`, {
        params: { days },
    });
    return response.data;
};

export const getMarketData = async () => {
    const response = await api.get('/market/overview');
    return response.data;
};

export const getHistoricalData = async (symbol, range = 365) => {
    const response = await api.get(`/stocks/${symbol}`, {
        params: { days: range },
    });
    return response.data;
};

export const getNewsData = async (symbol) => {
    const response = await api.get(`/news/${symbol}`);
    return response.data;
};

export const getCompanyProfile = async (symbol) => {
    const response = await api.get(`/stocks/${symbol}/profile`);
    return response.data;
};

export const getRecommendations = async (symbol) => {
    const response = await api.get(`/recommendations/${symbol}`);
    return response.data;
};

export const getEarningsData = async (symbol) => {
    const response = await api.get(`/earnings/${symbol}`);
    return response.data;
};

export const getDividendsData = async (symbol) => {
    const response = await api.get(`/dividends/${symbol}`);
    return response.data;
};

export const getTechnicalIndicators = async (symbol) => {
    const response = await api.get(`/indicators/${symbol}`);
    return response.data;
};

// Default export for compatibility with Dashboard.jsx
const apiMethods = {
    getStockData,
    getMarketData,
    getHistoricalData,
    getNewsData,
    getCompanyProfile,
    getRecommendations,
    getEarningsData,
    getDividendsData,
    getTechnicalIndicators,
};

export default apiMethods;