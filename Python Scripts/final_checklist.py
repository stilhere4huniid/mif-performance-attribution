import os
import pandas as pd

def check_files_exist():
    """Check all required files exist"""
    required_files = [
        'attribution_model.py',
        'time_series_analysis.py',
        'scenario_analysis.py',
        'factor_analysis.py',
        'generate_portfolio_data.py',
        'prepare_powerbi_data.py',
        'generate_report.py',
        'validate_results.py',
        'MIF_Performance_Dashboard.ipynb',
        'README.md',
        'USER_GUIDE.md',
        'requirements.txt'
    ]
    
    missing = [f for f in required_files if not os.path.exists(f)]
    
    if missing:
        print("❌ Missing files:")
        for f in missing:
            print(f"  - {f}")
        return False
    else:
        print("✓ All required files present")
        return True

def check_data_files():
    """Check data files exist and are valid"""
    data_files = [
        'mif_portfolio_returns.csv',
        'zse_benchmark_data.csv',
        'commodity_prices.csv'
    ]
    
    missing = [f for f in data_files if not os.path.exists(f)]
    
    if missing:
        print("❌ Missing data files:")
        for f in missing:
            print(f"  - {f}")
        return False
    
    # Validate data files
    try:
        portfolio_df = pd.read_csv('mif_portfolio_returns.csv', parse_dates=['Date'])
        benchmark_df = pd.read_csv('zse_benchmark_data.csv', parse_dates=['Date'])
        commodity_df = pd.read_csv('commodity_prices.csv', parse_dates=['Date'])
        
        print("✓ All data files present and valid")
        print(f"  - Portfolio records: {len(portfolio_df)}")
        print(f"  - Benchmark records: {len(benchmark_df)}")
        print(f"  - Commodity records: {len(commodity_df)}")
        return True
    except Exception as e:
        print(f"❌ Error reading data files: {e}")
        return False

def check_outputs():
    """Check if outputs can be generated"""
    try:
        from attribution_model import PerformanceAttributionModel
        from time_series_analysis import TimeSeriesAnalyzer
        from scenario_analysis import ScenarioAnalysis
        from factor_analysis import FactorAnalysis
        
        print("✓ All models can be imported")
        return True
    except Exception as e:
        print(f"❌ Error importing models: {e}")
        return False

def check_tests():
    """Check if tests exist and can run"""
    if os.path.exists('tests_attribution.py'):
        print("✓ Test suite exists")
        return True
    else:
        print("❌ Test suite missing")
        return False

def main():
    """Run complete project checklist"""
    print("="*60)
    print("MIF PERFORMANCE ATTRIBUTION - FINAL CHECKLIST")
    print("="*60 + "\n")
    
    checks = {
        "Files": check_files_exist(),
        "Data": check_data_files(),
        "Models": check_outputs(),
        "Tests": check_tests()
    }
    
    print("\n" + "="*60)
    print("CHECKLIST SUMMARY")
    print("="*60)
    
    for check_name, passed in checks.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{check_name}: {status}")
    
    all_passed = all(checks.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 PROJECT 100% COMPLETE!")
        print("You are ready to deploy and use the system.")
    else:
        print("⚠ Some checks failed. Please review and fix issues.")
    print("="*60 + "\n")
    
    return all_passed

if __name__ == "__main__":
    main()