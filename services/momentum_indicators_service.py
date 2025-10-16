class MomentumIndicatorsService:
    def calculate_stochastic(self, high_prices, low_prices, close_prices, period=14):
        # Calculate Stochastic Oscillator
        if len(close_prices) < period:
            return None
        lowest_low = min(low_prices[-period:])
        highest_high = max(high_prices[-period:])
        stoch = (close_prices[-1] - lowest_low) / (highest_high - lowest_low) * 100
        return stoch

    def calculate_williams_r(self, high_prices, low_prices, close_prices, period=14):
        # Calculate Williams %R
        if len(close_prices) < period:
            return None
        lowest_low = min(low_prices[-period:])
        highest_high = max(high_prices[-period:])
        williams_r = (highest_high - close_prices[-1]) / (highest_high - lowest_low) * -100
        return williams_r

    def calculate_roc(self, close_prices, period=12):
        # Calculate Rate of Change (ROC)
        if len(close_prices) < period:
            return None
        roc = (close_prices[-1] - close_prices[-(period + 1)]) / close_prices[-(period + 1)] * 100
        return roc

    def calculate_momentum(self, close_prices, period=10):
        # Calculate Momentum
        if len(close_prices) < period:
            return None
        momentum = close_prices[-1] - close_prices[-(period + 1)]
        return momentum

    def calculate_cci(self, typical_prices, period=14):
        # Calculate Commodity Channel Index (CCI)
        if len(typical_prices) < period:
            return None
        sma = sum(typical_prices[-period:]) / period
        mean_deviation = sum(abs(x - sma) for x in typical_prices[-period:]) / period
        cci = (typical_prices[-1] - sma) / (0.015 * mean_deviation)
        return cci
