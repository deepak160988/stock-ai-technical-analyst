// API methods

export const getStockData = async (symbol) => {
    // ...implementation
};

export const getMarketData = async () => {
    // ...implementation
};

export const getHistoricalData = async (symbol, range) => {
    // ...implementation
};

export const getNewsData = async (symbol) => {
    // ...implementation
};

export const getCompanyProfile = async (symbol) => {
    // ...implementation
};

export const getRecommendations = async (symbol) => {
    // ...implementation
};

export const getEarningsData = async (symbol) => {
    // ...implementation
};

export const getDividendsData = async (symbol) => {
    // ...implementation
};

export const getTechnicalIndicators = async (symbol) => {
    // ...implementation
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