import pandas as pd
import numpy as np
from attribution_model import PerformanceAttributionModel

class ScenarioAnalysis:
    """Perform what-if scenario analysis on portfolio performance"""
    
    def __init__(self, portfolio_df, benchmark_df):
        self.portfolio_df = portfolio_df.copy()
        self.benchmark_df = benchmark_df
        
    def commodity_shock_scenario(self, commodity_change_pct):
        """
        Simulate impact of commodity price shock on Mining sector
        commodity_change_pct: dictionary like {'Gold': -0.20, 'Platinum': -0.15}
        """
        scenario_df = self.portfolio_df.copy()
        
        # Apply shock to mining sector
        mining_mask = scenario_df['Sector'] == 'Mining'
        
        # Assume 50% correlation between commodity prices and mining returns
        avg_commodity_impact = np.mean(list(commodity_change_pct.values())) * 0.5
        
        scenario_df.loc[mining_mask, 'Monthly_Return'] = (
            scenario_df.loc[mining_mask, 'Monthly_Return'] * (1 + avg_commodity_impact)
        )
        
        return self._calculate_scenario_impact(scenario_df, "Commodity Price Shock")
    
    def sector_reallocation_scenario(self, new_weights):
        """
        Simulate different sector allocation
        new_weights: dictionary like {'Mining': 0.30, 'Energy': 0.20, ...}
        """
        scenario_df = self.portfolio_df.copy()
        
        # Recalculate asset values based on new weights
        total_value = scenario_df['Asset_Value'].sum()
        
        for sector, weight in new_weights.items():
            sector_mask = scenario_df['Sector'] == sector
            sector_count = sector_mask.sum()
            scenario_df.loc[sector_mask, 'Asset_Value'] = (
                total_value * weight / sector_count
            )
        
        return self._calculate_scenario_impact(scenario_df, "Sector Reallocation")
    
    def market_downturn_scenario(self, market_decline_pct=-0.30):
        """
        Simulate market downturn scenario
        """
        scenario_df = self.portfolio_df.copy()
        
        # Apply market decline with sector-specific betas
        sector_betas = {
            'Mining': 1.3,
            'Financials': 1.2,
            'Real Estate': 0.9,
            'Energy': 1.1,
            'ICT': 1.15,
            'Transport': 1.0,
            'Agriculture': 0.8,
            'Manufacturing': 1.05
        }
        
        for sector, beta in sector_betas.items():
            sector_mask = scenario_df['Sector'] == sector
            scenario_df.loc[sector_mask, 'Monthly_Return'] = (
                scenario_df.loc[sector_mask, 'Monthly_Return'] + 
                (market_decline_pct / 12) * beta
            )
        
        return self._calculate_scenario_impact(scenario_df, "Market Downturn")
    
    def _calculate_scenario_impact(self, scenario_df, scenario_name):
        """Calculate impact of scenario"""
        # Original performance
        original_return = self.portfolio_df.groupby('Date')['Monthly_Return'].mean().mean() * 12
        
        # Scenario performance
        scenario_return = scenario_df.groupby('Date')['Monthly_Return'].mean().mean() * 12
        
        # Impact
        impact = scenario_return - original_return
        
        return {
            'scenario_name': scenario_name,
            'original_return': original_return,
            'scenario_return': scenario_return,
            'impact': impact,
            'scenario_data': scenario_df
        }
    
    def run_monte_carlo(self, num_simulations=1000):
        """Run Monte Carlo simulation for portfolio returns"""
        portfolio_returns = self.portfolio_df.groupby('Date')['Monthly_Return'].mean()
        
        # Estimate parameters
        mean_return = portfolio_returns.mean()
        std_return = portfolio_returns.std()
        
        # Run simulations
        simulated_returns = np.random.normal(
            mean_return, 
            std_return, 
            size=(num_simulations, 12)
        )
        
        # Calculate annual returns
        annual_returns = (1 + simulated_returns).prod(axis=1) - 1
        
        return {
            'mean': annual_returns.mean(),
            'median': np.median(annual_returns),
            'std': annual_returns.std(),
            'percentile_5': np.percentile(annual_returns, 5),
            'percentile_95': np.percentile(annual_returns, 95),
            'var_95': -np.percentile(annual_returns, 5),  # Value at Risk
            'returns': annual_returns
        }

# Usage
if __name__ == "__main__":
    portfolio_df = pd.read_csv('mif_portfolio_returns.csv', parse_dates=['Date'])
    benchmark_df = pd.read_csv('zse_benchmark_data.csv', parse_dates=['Date'])
    
    analyzer = ScenarioAnalysis(portfolio_df, benchmark_df)
    
    # Scenario 1: Commodity shock
    print("\n=== SCENARIO 1: Commodity Price Decline ===")
    commodity_shock = analyzer.commodity_shock_scenario({
        'Gold': -0.20,
        'Platinum': -0.15,
        'Lithium': -0.30
    })
    print(f"Original Return: {commodity_shock['original_return']*100:.2f}%")
    print(f"Scenario Return: {commodity_shock['scenario_return']*100:.2f}%")
    print(f"Impact: {commodity_shock['impact']*100:.2f}%")
    
    # Scenario 2: Market downturn
    print("\n=== SCENARIO 2: Market Downturn (-30%) ===")
    downturn = analyzer.market_downturn_scenario(-0.30)
    print(f"Original Return: {downturn['original_return']*100:.2f}%")
    print(f"Scenario Return: {downturn['scenario_return']*100:.2f}%")
    print(f"Impact: {downturn['impact']*100:.2f}%")
    
    # Monte Carlo
    print("\n=== MONTE CARLO SIMULATION (1000 runs) ===")
    mc_results = analyzer.run_monte_carlo(1000)
    print(f"Expected Return: {mc_results['mean']*100:.2f}%")
    print(f"Median Return: {mc_results['median']*100:.2f}%")
    print(f"Standard Deviation: {mc_results['std']*100:.2f}%")
    print(f"5th Percentile: {mc_results['percentile_5']*100:.2f}%")
    print(f"95th Percentile: {mc_results['percentile_95']*100:.2f}%")
    print(f"Value at Risk (95%): {mc_results['var_95']*100:.2f}%")