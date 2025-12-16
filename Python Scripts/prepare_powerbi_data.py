import pandas as pd
import numpy as np

# Load all data
portfolio_df = pd.read_csv('mif_portfolio_returns.csv', parse_dates=['Date'])
benchmark_df = pd.read_csv('zse_benchmark_data.csv', parse_dates=['Date'])
commodity_df = pd.read_csv('commodity_prices.csv', parse_dates=['Date'])

# Create Power BI optimized tables

# 1. Fact Table: Portfolio Performance
fact_performance = portfolio_df.copy()
fact_performance['Year'] = fact_performance['Date'].dt.year
fact_performance['Month'] = fact_performance['Date'].dt.month
fact_performance['Quarter'] = fact_performance['Date'].dt.quarter
fact_performance['YearMonth'] = fact_performance['Date'].dt.to_period('M').astype(str)
fact_performance.to_csv('powerbi_fact_performance.csv', index=False)

# 2. Dimension Table: Sectors
dim_sectors = portfolio_df.groupby('Sector').agg({
    'Asset_Value': 'sum',
    'Company': 'nunique'
}).reset_index()
dim_sectors.columns = ['Sector', 'Total_Value', 'Number_of_Companies']
dim_sectors['Sector_ID'] = range(1, len(dim_sectors) + 1)
dim_sectors.to_csv('powerbi_dim_sectors.csv', index=False)

# 3. Dimension Table: Companies
dim_companies = portfolio_df[['Sector', 'Company']].drop_duplicates()
dim_companies['Company_ID'] = range(1, len(dim_companies) + 1)
dim_companies.to_csv('powerbi_dim_companies.csv', index=False)

# 4. Fact Table: Attribution Results
from attribution_model import PerformanceAttributionModel

sector_weights = portfolio_df.groupby('Sector')['Asset_Value'].sum()
sector_weights = sector_weights / sector_weights.sum()
model = PerformanceAttributionModel(portfolio_df, benchmark_df, sector_weights)

attribution_data = []
for year in portfolio_df['Date'].dt.year.unique():
    for quarter in [1, 2, 3, 4]:
        start_month = (quarter - 1) * 3 + 1
        end_month = quarter * 3
        start_date = f'{year}-{start_month:02d}-01'
        end_date = f'{year}-{end_month:02d}-28'
        
        try:
            results = model.calculate_attribution(start_date, end_date)
            
            attribution_data.append({
                'Year': year,
                'Quarter': quarter,
                'Period': f'{year} Q{quarter}',
                'Allocation_Effect': results['allocation_effect'],
                'Selection_Effect': results['selection_effect'],
                'Interaction_Effect': results['interaction_effect'],
                'Total_Active_Return': results['total_active_return']
            })
        except:
            continue

fact_attribution = pd.DataFrame(attribution_data)
fact_attribution.to_csv('powerbi_fact_attribution.csv', index=False)

# 5. Fact Table: Commodity Prices
fact_commodities = commodity_df.copy()
fact_commodities['Year'] = fact_commodities['Date'].dt.year
fact_commodities['Month'] = fact_commodities['Date'].dt.month
fact_commodities.to_csv('powerbi_fact_commodities.csv', index=False)

# 6. Calculate KPIs for Power BI
kpis = []

# Portfolio-level KPIs
portfolio_returns = portfolio_df.groupby('Date')['Monthly_Return'].mean()
kpis.append({
    'KPI_Name': 'Portfolio_Annualized_Return',
    'Value': (1 + portfolio_returns.mean()) ** 12 - 1,
    'Format': 'Percentage'
})

kpis.append({
    'KPI_Name': 'Portfolio_Volatility',
    'Value': portfolio_returns.std() * np.sqrt(12),
    'Format': 'Percentage'
})

kpis.append({
    'KPI_Name': 'Portfolio_Sharpe_Ratio',
    'Value': (portfolio_returns.mean() - 0.02/12) / portfolio_returns.std(),
    'Format': 'Number'
})

# Sector-level KPIs
for sector in portfolio_df['Sector'].unique():
    sector_data = portfolio_df[portfolio_df['Sector'] == sector]
    sector_returns = sector_data.groupby('Date')['Monthly_Return'].mean()
    
    kpis.append({
        'KPI_Name': f'{sector}_Return',
        'Value': (1 + sector_returns.mean()) ** 12 - 1,
        'Format': 'Percentage'
    })

kpi_df = pd.DataFrame(kpis)
kpi_df.to_csv('powerbi_kpis.csv', index=False)

print("Power BI data preparation complete!")
print("\nFiles created:")
print("  - powerbi_fact_performance.csv")
print("  - powerbi_dim_sectors.csv")
print("  - powerbi_dim_companies.csv")
print("  - powerbi_fact_attribution.csv")
print("  - powerbi_fact_commodities.csv")
print("  - powerbi_kpis.csv")