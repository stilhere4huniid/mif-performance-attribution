"""
Quick script to fix the frequency deprecation warnings
Run this to regenerate data with correct frequency
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Regenerate data with 'ME' instead of 'M'
print("Regenerating data files with correct frequency...")

# 1. Portfolio data
np.random.seed(42)
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

start_date = datetime(2020, 1, 1)
end_date = datetime(2024, 12, 31)
dates = pd.date_range(start_date, end_date, freq='ME')  # ← FIXED

data = []
for date in dates:
    for sector, info in sectors.items():
        for company_num in range(info['companies']):
            base_return = info['base_return'] / 12
            volatility = info['volatility'] / np.sqrt(12)
            market_factor = np.random.normal(0, 0.02)
            company_specific = np.random.normal(0, volatility)
            monthly_return = base_return + market_factor + company_specific
            
            data.append({
                'Date': date,
                'Sector': sector,
                'Company': f'{sector}_Company_{company_num+1}',
                'Monthly_Return': monthly_return,
                'Asset_Value': np.random.uniform(50, 500) * 1e6
            })

portfolio_df = pd.DataFrame(data)
portfolio_df.to_csv('mif_portfolio_returns.csv', index=False)
print(f"✓ Portfolio data: {len(portfolio_df)} records")

# 2. ZSE data
dates = pd.date_range('2020-01-01', '2024-12-31', freq='ME')  # ← FIXED
zse_values = []
current_value = 100

for date in dates:
    monthly_change = np.random.normal(0.005, 0.08)
    current_value = current_value * (1 + monthly_change)
    zse_values.append({
        'Date': date,
        'ZSE_AllShare': current_value,
        'Monthly_Return': monthly_change
    })

zse_df = pd.DataFrame(zse_values)
zse_df.to_csv('zse_benchmark_data.csv', index=False)
print(f"✓ ZSE data: {len(zse_df)} records")

# 3. Commodity data
dates = pd.date_range('2020-01-01', '2024-12-31', freq='ME')  # ← FIXED
commodities = {
    'Gold': {'start': 1500, 'volatility': 0.03, 'trend': 0.001},
    'Platinum': {'start': 900, 'volatility': 0.05, 'trend': -0.0005},
    'Lithium': {'start': 10000, 'volatility': 0.12, 'trend': 0.008},
    'Nickel': {'start': 14000, 'volatility': 0.07, 'trend': 0.002},
    'Chrome': {'start': 300, 'volatility': 0.06, 'trend': 0.0015}
}

data = []
for date_idx, date in enumerate(dates):
    for commodity, params in commodities.items():
        price = params['start']
        for _ in range(date_idx):
            price = price * (1 + params['trend'] + np.random.normal(0, params['volatility']))
        
        data.append({
            'Date': date,
            'Commodity': commodity,
            'Price': max(price, params['start'] * 0.5),
            'Unit': 'troy_oz' if commodity in ['Gold', 'Platinum'] else 'ton'
        })

commodity_df = pd.DataFrame(data)
commodity_df.to_csv('commodity_prices.csv', index=False)
print(f"✓ Commodity data: {len(commodity_df)} records")

print("\n✓ All data files regenerated with 'ME' frequency!")