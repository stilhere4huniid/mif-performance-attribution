import pandas as pd
import numpy as np
from scipy import stats

class PerformanceAttributionModel:
    """
    Brinson-Fachler Performance Attribution Model
    Decomposes portfolio returns into:
    1. Asset Allocation Effect
    2. Stock Selection Effect  
    3. Interaction Effect
    """
    
    def __init__(self, portfolio_returns, benchmark_returns, sector_weights):
        self.portfolio_returns = portfolio_returns
        self.benchmark_returns = benchmark_returns
        self.sector_weights = sector_weights
        
    def calculate_attribution(self, start_date, end_date):
        """Main attribution calculation"""
        
        # Filter data by date range
        port_data = self.portfolio_returns[
            (self.portfolio_returns['Date'] >= start_date) & 
            (self.portfolio_returns['Date'] <= end_date)
        ].copy()
        
        # Calculate portfolio returns by sector
        sector_returns = port_data.groupby('Sector').agg({
            'Monthly_Return': 'mean',
            'Asset_Value': 'sum'
        }).reset_index()
        
        # Calculate portfolio weights
        total_value = sector_returns['Asset_Value'].sum()
        sector_returns['Portfolio_Weight'] = sector_returns['Asset_Value'] / total_value
        
        # Get benchmark weights (assuming equal weight for simulation)
        sector_returns['Benchmark_Weight'] = 1 / len(sector_returns)
        
        # Calculate benchmark returns (simulate sector-specific benchmarks)
        sector_returns['Benchmark_Return'] = self._calculate_sector_benchmarks(
            sector_returns['Sector'].tolist(), start_date, end_date
        )
        
        # Brinson-Fachler Attribution Components
        results = {}
        
        # 1. Allocation Effect = (Portfolio Weight - Benchmark Weight) × Benchmark Return
        sector_returns['Allocation_Effect'] = (
            (sector_returns['Portfolio_Weight'] - sector_returns['Benchmark_Weight']) * 
            sector_returns['Benchmark_Return']
        )
        
        # 2. Selection Effect = Benchmark Weight × (Portfolio Return - Benchmark Return)
        sector_returns['Selection_Effect'] = (
            sector_returns['Benchmark_Weight'] * 
            (sector_returns['Monthly_Return'] - sector_returns['Benchmark_Return'])
        )
        
        # 3. Interaction Effect = (Portfolio Weight - Benchmark Weight) × 
        #                         (Portfolio Return - Benchmark Return)
        sector_returns['Interaction_Effect'] = (
            (sector_returns['Portfolio_Weight'] - sector_returns['Benchmark_Weight']) * 
            (sector_returns['Monthly_Return'] - sector_returns['Benchmark_Return'])
        )
        
        # Total Attribution
        results['allocation_effect'] = sector_returns['Allocation_Effect'].sum()
        results['selection_effect'] = sector_returns['Selection_Effect'].sum()
        results['interaction_effect'] = sector_returns['Interaction_Effect'].sum()
        results['total_active_return'] = (
            results['allocation_effect'] + 
            results['selection_effect'] + 
            results['interaction_effect']
        )
        
        results['sector_details'] = sector_returns
        
        return results
    
    def _calculate_sector_benchmarks(self, sectors, start_date, end_date):
        """Calculate sector-specific benchmark returns"""
        # Simulate sector benchmarks based on ZSE and commodity prices
        bench_returns = []
        
        for sector in sectors:
            if sector == 'Mining':
                # Mining correlated with commodity prices
                bench_return = np.random.normal(0.01, 0.04)
            elif sector == 'Financials':
                # Financials correlated with ZSE financial index
                bench_return = np.random.normal(0.008, 0.03)
            elif sector == 'Energy':
                # Energy has different dynamics
                bench_return = np.random.normal(0.006, 0.035)
            else:
                # Other sectors use general market
                bench_return = np.random.normal(0.007, 0.032)
            
            bench_returns.append(bench_return)
        
        return bench_returns
    
    def risk_adjusted_attribution(self):
        """Calculate Sharpe ratios and risk-adjusted attribution"""
        # Calculate portfolio Sharpe ratio
        port_returns = self.portfolio_returns.groupby('Date')['Monthly_Return'].mean()
        port_sharpe = self._calculate_sharpe(port_returns)
        
        # Calculate sector Sharpe ratios
        sector_sharpes = {}
        for sector in self.portfolio_returns['Sector'].unique():
            sector_data = self.portfolio_returns[
                self.portfolio_returns['Sector'] == sector
            ]
            sector_returns = sector_data.groupby('Date')['Monthly_Return'].mean()
            sector_sharpes[sector] = self._calculate_sharpe(sector_returns)
        
        return {
            'portfolio_sharpe': port_sharpe,
            'sector_sharpes': sector_sharpes
        }
    
    def _calculate_sharpe(self, returns, risk_free_rate=0.02/12):
        """Calculate Sharpe ratio"""
        excess_returns = returns - risk_free_rate
        if excess_returns.std() == 0:
            return 0
        return excess_returns.mean() / excess_returns.std()
    
    def factor_attribution(self):
        """Multi-factor performance attribution"""
        # Factors: Market, Sector Momentum, Commodity Prices
        
        results = {
            'market_factor': {},
            'commodity_factor': {},
            'sector_momentum': {}
        }
        
        # This would include regression analysis against factors
        # Simplified for this implementation
        
        return results


# Usage example
if __name__ == "__main__":
    # Load data
    portfolio_df = pd.read_csv('mif_portfolio_returns.csv')
    portfolio_df['Date'] = pd.to_datetime(portfolio_df['Date'])
    
    benchmark_df = pd.read_csv('zse_benchmark_data.csv')
    benchmark_df['Date'] = pd.to_datetime(benchmark_df['Date'])
    
    # Calculate sector weights
    sector_weights = portfolio_df.groupby('Sector')['Asset_Value'].sum()
    sector_weights = sector_weights / sector_weights.sum()
    
    # Create model
    model = PerformanceAttributionModel(
        portfolio_df, 
        benchmark_df, 
        sector_weights
    )
    
    # Run attribution
    results = model.calculate_attribution('2024-01-01', '2024-12-31')
    
    print("\n=== PERFORMANCE ATTRIBUTION RESULTS ===\n")
    print(f"Allocation Effect: {results['allocation_effect']:.4f} ({results['allocation_effect']*100:.2f}%)")
    print(f"Selection Effect: {results['selection_effect']:.4f} ({results['selection_effect']*100:.2f}%)")
    print(f"Interaction Effect: {results['interaction_effect']:.4f} ({results['interaction_effect']*100:.2f}%)")
    print(f"Total Active Return: {results['total_active_return']:.4f} ({results['total_active_return']*100:.2f}%)")
    
    print("\n=== SECTOR BREAKDOWN ===\n")
    print(results['sector_details'][['Sector', 'Portfolio_Weight', 'Monthly_Return', 
                                      'Allocation_Effect', 'Selection_Effect']])
    
    # Risk-adjusted metrics
    risk_metrics = model.risk_adjusted_attribution()
    print(f"\n=== RISK METRICS ===\n")
    print(f"Portfolio Sharpe Ratio: {risk_metrics['portfolio_sharpe']:.3f}")
    print("\nSector Sharpe Ratios:")
    for sector, sharpe in risk_metrics['sector_sharpes'].items():
        print(f"  {sector}: {sharpe:.3f}")