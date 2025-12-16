import pandas as pd
import numpy as np
from attribution_model import PerformanceAttributionModel

class ResultValidator:
    """Validate model results for accuracy and consistency"""
    
    def __init__(self, portfolio_df, benchmark_df):
        self.portfolio_df = portfolio_df
        self.benchmark_df = benchmark_df
        
    def validate_all(self):
        """Run all validation checks"""
        print("="*60)
        print("VALIDATION REPORT")
        print("="*60 + "\n")
        
        checks = [
            self.check_data_quality(),
            self.check_attribution_consistency(),
            self.check_return_calculations(),
            self.check_risk_metrics(),
            self.check_sector_coverage()
        ]
        
        passed = sum(checks)
        total = len(checks)
        
        print(f"\n{'='*60}")
        print(f"VALIDATION SUMMARY: {passed}/{total} checks passed")
        print(f"{'='*60}\n")
        
        return passed == total
    
    def check_data_quality(self):
        """Validate data quality"""
        print("1. Data Quality Check...")
        
        issues = []
        
        # Check for missing values
        if self.portfolio_df.isnull().any().any():
            issues.append("Missing values found in portfolio data")
        
        # Check for negative asset values
        if (self.portfolio_df['Asset_Value'] < 0).any():
            issues.append("Negative asset values found")
        
        # Check for extreme returns (>100% or <-100% monthly)
        extreme_returns = (
            (self.portfolio_df['Monthly_Return'] > 1) | 
            (self.portfolio_df['Monthly_Return'] < -1)
        )
        if extreme_returns.any():
            issues.append(f"Extreme returns found: {extreme_returns.sum()} records")
        
        # Check date continuity
        dates = self.portfolio_df['Date'].sort_values().unique()
        date_diffs = pd.Series(dates).diff().dropna()
        expected_diff = pd.Timedelta(days=28)  # Approximately monthly
        
        if not all((date_diffs >= expected_diff) & (date_diffs <= pd.Timedelta(days=31))):
            issues.append("Date continuity issues detected")
        
        if issues:
            print("  ❌ FAILED")
            for issue in issues:
                print(f"    - {issue}")
            return False
        else:
            print("  ✓ PASSED")
            return True
    
    def check_attribution_consistency(self):
        """Validate attribution calculation consistency"""
        print("2. Attribution Consistency Check...")
        
        sector_weights = self.portfolio_df.groupby('Sector')['Asset_Value'].sum()
        sector_weights = sector_weights / sector_weights.sum()
        
        model = PerformanceAttributionModel(
            self.portfolio_df,
            self.benchmark_df,
            sector_weights
        )
        
        results = model.calculate_attribution('2024-01-01', '2024-12-31')
        
        # Check components sum correctly
        total_calculated = (
            results['allocation_effect'] + 
            results['selection_effect'] + 
            results['interaction_effect']
        )
        
        diff = abs(total_calculated - results['total_active_return'])
        
        if diff > 1e-6:
            print("  ❌ FAILED")
            print(f"    - Attribution components don't sum correctly (diff: {diff})")
            return False
        
        # Check weights sum to 1
        weight_sum = results['sector_details']['Portfolio_Weight'].sum()
        if abs(weight_sum - 1.0) > 1e-6:
            print("  ❌ FAILED")
            print(f"    - Portfolio weights don't sum to 1 (sum: {weight_sum})")
            return False
        
        print("  ✓ PASSED")
        return True
    
    def check_return_calculations(self):
        """Validate return calculations"""
        print("3. Return Calculation Check...")
        
        issues = []
        
        # Calculate portfolio-level returns manually
        portfolio_returns = self.portfolio_df.groupby('Date').apply(
            lambda x: (x['Monthly_Return'] * x['Asset_Value']).sum() / x['Asset_Value'].sum()
        )
        
        # Check for finite values
        if not portfolio_returns.apply(np.isfinite).all():
            issues.append("Non-finite values in return calculations")
        
        # Check annualized return is reasonable (-100% to +500%)
        annual_return = (1 + portfolio_returns.mean()) ** 12 - 1
        if not (-1 <= annual_return <= 5):
            issues.append(f"Unrealistic annualized return: {annual_return*100:.2f}%")
        
        if issues:
            print("  ❌ FAILED")
            for issue in issues:
                print(f"    - {issue}")
            return False
        else:
            print("  ✓ PASSED")
            return True
    
    def check_risk_metrics(self):
        """Validate risk metric calculations"""
        print("4. Risk Metrics Check...")
        
        sector_weights = self.portfolio_df.groupby('Sector')['Asset_Value'].sum()
        sector_weights = sector_weights / sector_weights.sum()
        
        model = PerformanceAttributionModel(
            self.portfolio_df,
            self.benchmark_df,
            sector_weights
        )
        
        risk_metrics = model.risk_adjusted_attribution()
        
        issues = []
        
        # Check Sharpe ratio is finite
        if not np.isfinite(risk_metrics['portfolio_sharpe']):
            issues.append("Portfolio Sharpe ratio is not finite")
        
        # Check sector Sharpe ratios
        for sector, sharpe in risk_metrics['sector_sharpes'].items():
            if not np.isfinite(sharpe):
                issues.append(f"Sharpe ratio for {sector} is not finite")
        
        if issues:
            print("  ❌ FAILED")
            for issue in issues:
                print(f"    - {issue}")
            return False
        else:
            print("  ✓ PASSED")
            return True
    
    def check_sector_coverage(self):
        """Validate sector coverage"""
        print("5. Sector Coverage Check...")
        
        expected_sectors = ['Mining', 'Energy', 'ICT', 'Transport', 
                          'Agriculture', 'Financials', 'Real Estate', 'Manufacturing']
        
        actual_sectors = self.portfolio_df['Sector'].unique()
        
        missing_sectors = set(expected_sectors) - set(actual_sectors)
        
        if missing_sectors:
            print("  ⚠ WARNING")
            print(f"    - Missing sectors: {missing_sectors}")
            return True  # Warning, not failure
        else:
            print("  ✓ PASSED")
            return True

# Usage
if __name__ == "__main__":
    portfolio_df = pd.read_csv('mif_portfolio_returns.csv', parse_dates=['Date'])
    benchmark_df = pd.read_csv('zse_benchmark_data.csv', parse_dates=['Date'])
    
    validator = ResultValidator(portfolio_df, benchmark_df)
    all_passed = validator.validate_all()
    
    if all_passed:
        print("✓ All validation checks passed! Ready for production.")
    else:
        print("✗ Some validation checks failed. Please review and fix issues.")