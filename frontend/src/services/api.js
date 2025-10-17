import axios from 'axios';

// Detect if we are in a Codespaces environment
const isCodespaces = Boolean(process.env.CODESPACES);

// Base URL configuration
const baseURL = isCodespaces ? 'https://api.codespaces.example.com' : 'https://api.production.example.com';

// Create an API client
const apiClient = axios.create({
    baseURL,
    timeout: 10000, // 10 seconds timeout
});

// Request/Response Interceptors
apiClient.interceptors.request.use(config => {
    console.log('Making request to:', config.url);
    return config;
}, error => {
    console.error('Request error:', error);
    return Promise.reject(error);
});

apiClient.interceptors.response.use(response => {
    console.log('Response received:', response);
    return response;
}, error => {
    console.error('Response error:', error);
    return Promise.reject(error);
});

// API methods
export const getStockData = (symbol) => apiClient.get(`/stocks/${symbol}`);
export const getLatestPrice = (symbol) => apiClient.get(`/stocks/${symbol}/price`);
export const getIndicators = (symbol) => apiClient.get(`/stocks/${symbol}/indicators`);
export const getRSI = (symbol) => apiClient.get(`/stocks/${symbol}/rsi`);
export const getMACD = (symbol) => apiClient.get(`/stocks/${symbol}/macd`);
export const getSignals = (symbol) => apiClient.get(`/stocks/${symbol}/signals`);
export const getPortfolio = () => apiClient.get(`/portfolio`);
export const getIndianStocks = () => apiClient.get(`/stocks/indian`);
export const getMLPrediction = (data) => apiClient.post(`/ml/predict`, data);

// Default export
export default apiClient;