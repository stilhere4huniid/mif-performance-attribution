# MIF Performance Attribution - User Guide

## Quick Start

### For Fund Managers

1. **View Latest Performance**
```bash
   jupyter notebook MIF_Performance_Dashboard.ipynb
```
   Navigate to Cell → Run All

2. **Generate Monthly Report**
```bash
   python generate_report.py
```
   PDF will be saved as `MIF_Performance_Attribution_Report.pdf`

3. **Run Scenario Analysis**
```bash
   python scenario_analysis.py
```

### For Analysts

1. **Custom Date Range Analysis**
```python
   from attribution_model import PerformanceAttributionModel
   
   model = PerformanceAttributionModel(portfolio_df, benchmark_df, weights)
   results = model.calculate_attribution('2024-Q1-01', '2024-06-30')
```

2. **Sector-Specific Deep Dive**
```python
   mining_data = portfolio_df[portfolio_df['Sector'] == 'Mining']
   # Analyze specific sector...
```

## Common Tasks

### Task 1: Monthly Performance Review

1. Update data files with latest returns
2. Run attribution model
3. Generate dashboard
4. Export key metrics to Excel
5. Present to investment committee

### Task 2: Quarterly Rebalancing Analysis

1. Run scenario analysis with proposed allocations
2. Compare risk-return profiles
3. Assess impact on attribution
4. Generate recommendation report

### Task 3: Risk Assessment

1. Calculate VaR using Monte Carlo
2. Run stress test scenarios
3. Review sector concentration risks
4. Update risk management policies

## Power BI Dashboard Guide

### Setup
1. Open Power BI Desktop
2. Import `powerbi_*.csv` files
3. Load pre-built template `MIF_Dashboard.pbix`

### Key Pages
- **Executive Summary**: High-level KPIs
- **Attribution Analysis**: Detailed breakdown
- **Sector Performance**: Sector comparisons
- **Risk Metrics**: Risk-adjusted returns

### Filters
- Date range
- Sector
- Company
- Performance threshold

## Troubleshooting

### Issue: "Data not found"
**Solution**: Run data generation scripts first

### Issue: "Attribution doesn't sum"
**Solution**: Check for data quality issues, run validation script

### Issue: "Power BI won't load data"
**Solution**: Verify CSV files are in correct format, check file paths

## Best Practices

1. **Data Updates**: Update portfolio data monthly
2. **Validation**: Run validation script after updates
3. **Backups**: Keep historical data backed up
4. **Documentation**: Log any manual adjustments
5. **Version Control**: Use Git for code changes

## Advanced Features

### Custom Factors
Add your own factors to regression analysis by modifying `factor_analysis.py`

### Custom Scenarios
Create scenarios in `scenario_analysis.py` for specific stress tests

### API Integration
Connect to live data feeds (see documentation in `/docs/api_integration.md`)

## Support

For technical support:
- Email: stillhere4huniid@gmail.com
- Slack: #mif-analytics

## Updates

Check for updates monthly:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```
