import axios from 'axios';

// Detect if running in GitHub Codespaces
const isCodespaces = window.location.hostname.endsWith('.app.github.dev');
const BASE_URL = isCodespaces ? 'http://localhost:8000' : 'http://localhost:3000';

// Axios instance
const apiClient = axios.create({
    baseURL: BASE_URL,
});

// Axios interceptors for logging request/response
apiClient.interceptors.request.use(request => {
    console.log('Starting Request', request);
    return request;
});

apiClient.interceptors.response.use(response => {
    console.log('Response:', response);
    return response;
});

// Function to get stock data
export const getStockData = async (symbol) => {
    const response = await apiClient.get(`/stocks/${symbol}`);
    return response.data;
};

// Function to get the latest price
export const getLatestPrice = async (symbol) => {
    const response = await apiClient.get(`/stocks/${symbol}/latest-price`);
    return response.data;
};

// Function to get indicators
export const getIndicators = async (symbol) => {
    const response = await apiClient.get(`/stocks/${symbol}/indicators`);
    return response.data;
};

// Function to get RSI
export const getRSI = async (symbol) => {
    const response = await apiClient.get(`/stocks/${symbol}/rsi`);
    return response.data;
};

// Function to get MACD
export const getMACD = async (symbol) => {
    const response = await apiClient.get(`/stocks/${symbol}/macd`);
    return response.data;
};

// Function to get signals
export const getSignals = async (symbol) => {
    const response = await apiClient.get(`/stocks/${symbol}/signals`);
    return response.data;
};

// Function to get portfolio
export const getPortfolio = async () => {
    const response = await apiClient.get('/portfolio');
    return response.data;
};

// Function to get Indian stocks
export const getIndianStocks = async () => {
    const response = await apiClient.get('/stocks/indian');
    return response.data;
};

// Function to get machine learning predictions
export const getMLPrediction = async (data) => {
    const response = await apiClient.post('/ml/predict', data);
    return response.data;
};
