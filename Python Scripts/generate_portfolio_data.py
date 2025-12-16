import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Define sectors and their characteristics
sectors = {
    'Mining': {'companies': 7, 'volatility': 0.25, 'base_return': 0.12},
    'Energy': {'companies': 2, 'volatility': 0.20, 'base_return': 0.08},
    'ICT': {'companies': 4, 'volatility': 0.22, 'base_return': 0.15},
    'Transport': {'companies': 3, 'volatility': 0.18, 'base_return': 0.06},
    'Agriculture': {'companies': 2, 'volatility': 0.28, 'base_return': 0.10},
    'Financials': {'companies': 2, 'volatility': 0.16, 'base_return': 0.09},
    'Real Estate': {'companies': 1, 'volatility': 0.12, 'base_return': 0.07},
    'Manufacturing': {'companies': 2, 'volatility': 0.19, 'base_return': 0.08}
}

# Generate monthly data for 5 years
start_date = datetime(2020, 1, 1)
end_date = datetime(2024, 12, 31)
dates = pd.date_range(start_date, end_date, freq='ME')

# Create portfolio data
data = []

print("Generating MIF portfolio data...")
print(f"Date range: {start_date.date()} to {end_date.date()}")
print(f"Total months: {len(dates)}")

for date in dates:
    for sector, info in sectors.items():
        for company_num in range(info['companies']):
            # Simulate monthly return with sector characteristics
            base_return = info['base_return'] / 12  # Monthly from annual
            volatility = info['volatility'] / np.sqrt(12)  # Monthly volatility
            
            # Add some autocorrelation and market correlation
            market_factor = np.random.normal(0, 0.02)
            company_specific = np.random.normal(0, volatility)
            monthly_return = base_return + market_factor + company_specific
            
            data.append({
                'Date': date,
                'Sector': sector,
                'Company': f'{sector}_Company_{company_num+1}',
                'Monthly_Return': monthly_return,
                'Asset_Value': np.random.uniform(50, 500) * 1e6  # Millions USD
            })

df = pd.DataFrame(data)
df.to_csv('mif_portfolio_returns.csv', index=False)

print("\n" + "="*60)
print("✓ Portfolio data generated successfully!")
print("="*60)
print(f"\nFile created: mif_portfolio_returns.csv")
print(f"Total records: {len(df):,}")
print(f"Sectors: {df['Sector'].nunique()}")
print(f"Companies: {df['Company'].nunique()}")
print(f"Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")
print("\nSample data:")
print(df.head(10))
print("\nSector summary:")
print(df.groupby('Sector')['Company'].nunique())