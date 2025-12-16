import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

class TimeSeriesAnalyzer:
    """Analyze return patterns and volatility over time"""
    
    def __init__(self, returns_df):
        self.returns_df = returns_df
        
    def rolling_performance(self, window=12):
        """Calculate rolling returns and volatility"""
        # Aggregate to portfolio level
        portfolio_returns = self.returns_df.groupby('Date')['Monthly_Return'].mean()
        
        rolling_mean = portfolio_returns.rolling(window=window).mean()
        rolling_std = portfolio_returns.rolling(window=window).std()
        rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(12)
        
        return pd.DataFrame({
            'Rolling_Return': rolling_mean,
            'Rolling_Volatility': rolling_std,
            'Rolling_Sharpe': rolling_sharpe
        })
    
    def decompose_returns(self):
        """Decompose returns into trend, seasonal, and residual"""
        from statsmodels.tsa.seasonal import seasonal_decompose
        
        portfolio_returns = self.returns_df.groupby('Date')['Monthly_Return'].mean()
        
        # Requires at least 2 full cycles
        if len(portfolio_returns) >= 24:
            decomposition = seasonal_decompose(
                portfolio_returns, 
                model='additive', 
                period=12
            )
            
            return {
                'trend': decomposition.trend,
                'seasonal': decomposition.seasonal,
                'residual': decomposition.resid
            }
        return None
    
    def test_stationarity(self):
        """Test for stationarity using Augmented Dickey-Fuller test"""
        portfolio_returns = self.returns_df.groupby('Date')['Monthly_Return'].mean()
        
        result = adfuller(portfolio_returns.dropna())
        
        return {
            'adf_statistic': result[0],
            'p_value': result[1],
            'is_stationary': bool(result[1] < 0.05),  # NEW - Added bool()
            'critical_values': result[4]
        }

# Usage
if __name__ == "__main__":
    portfolio_df = pd.read_csv('mif_portfolio_returns.csv')
    portfolio_df['Date'] = pd.to_datetime(portfolio_df['Date'])
    
    analyzer = TimeSeriesAnalyzer(portfolio_df)
    
    # Rolling metrics
    rolling = analyzer.rolling_performance(window=12)
    print("\nRolling Performance (12-month window):")
    print(rolling.tail())
    
    # Stationarity test
    stationarity = analyzer.test_stationarity()
    print(f"\nStationarity Test:")
    print(f"  ADF Statistic: {stationarity['adf_statistic']:.4f}")
    print(f"  P-value: {stationarity['p_value']:.4f}")
    print(f"  Is Stationary: {stationarity['is_stationary']}")