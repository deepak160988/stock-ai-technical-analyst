import axios from 'axios';

// Detect environment and set base URL
const hostname = window.location.hostname;
const isCodespace = Boolean(process.env.CODESPACE_NAME);
const baseURL = isCodespace ? `https://${hostname}:8000` : `http://${hostname}:3000`;

const axiosInstance = axios.create({
    baseURL: baseURL,
    timeout: 10000, // 10 seconds timeout
});

// Logging interceptor for request
axiosInstance.interceptors.request.use((config) => {
    console.log(`Making request to: ${config.url}`);
    return config;
}, (error) => {
    return Promise.reject(error);
});

// API methods
const apiMethods = {
    getMethod1: () => axiosInstance.get('/method1'),
    getMethod2: () => axiosInstance.get('/method2'),
    postMethod1: (data) => axiosInstance.post('/method1', data),
    postMethod2: (data) => axiosInstance.post('/method2', data),
    putMethod1: (data) => axiosInstance.put('/method1', data),
    deleteMethod1: (id) => axiosInstance.delete(`/method1/${id}`),
    getMethod3: () => axiosInstance.get('/method3'),
    getMethod4: () => axiosInstance.get('/method4'),
    getMethod5: () => axiosInstance.get('/method5'),
};

export default apiMethods;