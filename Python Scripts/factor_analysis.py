import pandas as pd
import numpy as np
from statsmodels.regression.linear_model import OLS
import statsmodels.api as sm

class FactorAnalysis:
    """Multi-factor regression analysis for return attribution"""
    
    def __init__(self, portfolio_df, market_df, commodity_df):
        self.portfolio_df = portfolio_df
        self.market_df = market_df
        self.commodity_df = commodity_df
        
    def run_factor_regression(self, sector=None):
        """
        Run multi-factor regression:
        Returns = α + β1*Market + β2*Commodity + β3*Sector_Momentum + ε
        """
        # Prepare returns
        if sector:
            returns = self.portfolio_df[
                self.portfolio_df['Sector'] == sector
            ].groupby('Date')['Monthly_Return'].mean()
        else:
            returns = self.portfolio_df.groupby('Date')['Monthly_Return'].mean()
        
        # Prepare factors
        factors_df = pd.DataFrame(index=returns.index)
        
        # Factor 1: Market returns
        market_returns = self.market_df.set_index('Date')['Monthly_Return']
        factors_df['Market_Factor'] = market_returns.reindex(returns.index)
        
        # Factor 2: Commodity factor (for Mining-heavy portfolio)
        commodity_returns = self._calculate_commodity_factor()
        factors_df['Commodity_Factor'] = commodity_returns.reindex(returns.index)
        
        # Factor 3: Momentum factor
        factors_df['Momentum_Factor'] = returns.rolling(window=3).mean().shift(1)
        
        # Remove NaN
        combined = pd.concat([returns, factors_df], axis=1).dropna()
        y = combined.iloc[:, 0]  # Returns
        X = combined.iloc[:, 1:]  # Factors
        
        # Add constant
        X = sm.add_constant(X)
        
        # Run regression
        model = OLS(y, X).fit()
        
        return {
            'model': model,
            'alpha': model.params['const'],
            'beta_market': model.params['Market_Factor'],
            'beta_commodity': model.params['Commodity_Factor'],
            'beta_momentum': model.params['Momentum_Factor'],
            'r_squared': model.rsquared,
            'adj_r_squared': model.rsquared_adj,
            'summary': model.summary()
        }
    
    def _calculate_commodity_factor(self):
        """Calculate composite commodity factor"""
        # Weight by MIF's mining exposure
        commodity_weights = {
            'Gold': 0.35,
            'Platinum': 0.30,
            'Lithium': 0.20,
            'Nickel': 0.10,
            'Chrome': 0.05
        }
        
        commodity_returns = {}
        
        for commodity in commodity_weights.keys():
            comm_data = self.commodity_df[
                self.commodity_df['Commodity'] == commodity
            ].set_index('Date')['Price']
            
            comm_returns = comm_data.pct_change()
            commodity_returns[commodity] = comm_returns
        
        # Combine into weighted factor
        factor_df = pd.DataFrame(commodity_returns)
        weighted_factor = (factor_df * pd.Series(commodity_weights)).sum(axis=1)
        
        return weighted_factor
    
    def fama_french_style_analysis(self):
        """
        Implement Fama-French style factor analysis
        Returns = α + β_Market*MKT + β_Size*SMB + β_Value*HML + ε
        
        For MIF context:
        - MKT = Market factor (ZSE)
        - SMB = Small vs Large cap (company size within portfolio)
        - HML = High vs Low performing sectors
        """
        
        # Portfolio returns
        portfolio_returns = self.portfolio_df.groupby('Date')['Monthly_Return'].mean()
        
        # Prepare factors
        factors_df = pd.DataFrame(index=portfolio_returns.index)
        
        # Market factor
        factors_df['MKT'] = self.market_df.set_index('Date')['Monthly_Return']
        
        # SMB (Small Minus Big) - based on asset values
        smb = self._calculate_smb_factor()
        factors_df['SMB'] = smb
        
        # HML (High Minus Low) - based on sector performance
        hml = self._calculate_hml_factor()
        factors_df['HML'] = hml
        
        # Clean data
        combined = pd.concat([portfolio_returns, factors_df], axis=1).dropna()
        y = combined.iloc[:, 0]
        X = sm.add_constant(combined.iloc[:, 1:])
        
        # Run regression
        model = OLS(y, X).fit()
        
        return {
            'alpha': model.params['const'],
            'beta_market': model.params['MKT'],
            'beta_size': model.params['SMB'],
            'beta_value': model.params['HML'],
            'r_squared': model.rsquared,
            'model': model
        }
    
    def _calculate_smb_factor(self):
        """Calculate Size factor (Small Minus Big)"""
        # Split companies by median asset value
        median_value = self.portfolio_df['Asset_Value'].median()
        
        small_returns = self.portfolio_df[
            self.portfolio_df['Asset_Value'] <= median_value
        ].groupby('Date')['Monthly_Return'].mean()
        
        big_returns = self.portfolio_df[
            self.portfolio_df['Asset_Value'] > median_value
        ].groupby('Date')['Monthly_Return'].mean()
        
        return small_returns - big_returns
    
    def _calculate_hml_factor(self):
        """Calculate Value factor (High Minus Low performing sectors)"""
        # Calculate sector performance over rolling window
        sector_perf = self.portfolio_df.groupby(['Date', 'Sector'])['Monthly_Return'].mean().unstack()
        
        # Identify high and low performers each period
        high_perf = sector_perf.apply(lambda x: x.nlargest(3).mean(), axis=1)
        low_perf = sector_perf.apply(lambda x: x.nsmallest(3).mean(), axis=1)
        
        return high_perf - low_perf
    
    def sector_specific_regression(self):
        """Run factor regression for each sector"""
        results = {}
        
        for sector in self.portfolio_df['Sector'].unique():
            sector_results = self.run_factor_regression(sector=sector)
            results[sector] = {
                'alpha': sector_results['alpha'],
                'beta_market': sector_results['beta_market'],
                'beta_commodity': sector_results['beta_commodity'],
                'r_squared': sector_results['r_squared']
            }
        
        return pd.DataFrame(results).T

# Usage
if __name__ == "__main__":
    portfolio_df = pd.read_csv('mif_portfolio_returns.csv', parse_dates=['Date'])
    benchmark_df = pd.read_csv('zse_benchmark_data.csv', parse_dates=['Date'])
    commodity_df = pd.read_csv('commodity_prices.csv', parse_dates=['Date'])
    
    analyzer = FactorAnalysis(portfolio_df, benchmark_df, commodity_df)
    
    # Portfolio-level factor regression
    print("\n=== PORTFOLIO FACTOR REGRESSION ===")
    portfolio_regression = analyzer.run_factor_regression()
    print(f"\nAlpha (Manager Skill): {portfolio_regression['alpha']*100:.3f}%")
    print(f"Market Beta: {portfolio_regression['beta_market']:.3f}")
    print(f"Commodity Beta: {portfolio_regression['beta_commodity']:.3f}")
    print(f"Momentum Beta: {portfolio_regression['beta_momentum']:.3f}")
    print(f"R-squared: {portfolio_regression['r_squared']:.3f}")
    
    # Fama-French style analysis
    print("\n=== FAMA-FRENCH STYLE ANALYSIS ===")
    ff_results = analyzer.fama_french_style_analysis()
    print(f"\nAlpha: {ff_results['alpha']*100:.3f}%")
    print(f"Market Beta: {ff_results['beta_market']:.3f}")
    print(f"Size Beta: {ff_results['beta_size']:.3f}")
    print(f"Value Beta: {ff_results['beta_value']:.3f}")
    print(f"R-squared: {ff_results['r_squared']:.3f}")
    
    # Sector-specific regressions
    print("\n=== SECTOR-SPECIFIC FACTOR ANALYSIS ===")
    sector_results = analyzer.sector_specific_regression()
    print(sector_results)