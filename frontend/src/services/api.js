// Environment detection logic
const isDevelopment = window.location.hostname === 'localhost';

// Function to detect if the stock is Indian
function isIndianStock(stockSymbol) {
    // Assuming Indian stocks are represented by their corresponding indices
    const indianStockIndices = ['NSE', 'BSE']; // Add more indices if needed
    return indianStockIndices.some(index => stockSymbol.includes(index));
}

// Function to route stocks correctly based on the environment
function routeStock(stockSymbol) {
    if (isDevelopment) {
        // Logic for development environment
        console.log(`Routing for development: ${stockSymbol}`);
        return `/dev/stocks/${stockSymbol}`;
    } else {
        // Logic for production environment
        console.log(`Routing for production: ${stockSymbol}`);
        return `/prod/stocks/${stockSymbol}`;
    }
}

// Sample usage
const stockSymbol = 'NSE:RELIANCE'; // Example stock symbol
if (isIndianStock(stockSymbol)) {
    const route = routeStock(stockSymbol);
    console.log(`Stock route: ${route}`);
} else {
    console.log(`Stock ${stockSymbol} is not an Indian stock.`);
}