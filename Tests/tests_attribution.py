import unittest
import pandas as pd
import numpy as np
from attribution_model import PerformanceAttributionModel

class TestPerformanceAttribution(unittest.TestCase):
    """Test suite for performance attribution model"""
    
    def setUp(self):
        """Set up test data"""
        # Create sample portfolio data
        dates = pd.date_range('2024-01-01', '2024-12-31', freq='ME') # Changed M to ME
        
        data = []
        for date in dates:
            for sector in ['Mining', 'Energy']:
                data.append({
                    'Date': date,
                    'Sector': sector,
                    'Company': f'{sector}_Co',
                    'Monthly_Return': np.random.normal(0.01, 0.02),
                    'Asset_Value': 100e6
                })
        
        self.portfolio_df = pd.DataFrame(data)
        
        # Create benchmark data
        bench_data = []
        for date in dates:
            bench_data.append({
                'Date': date,
                'ZSE_AllShare': 100 * (1 + np.random.normal(0.005, 0.02)),
                'Monthly_Return': np.random.normal(0.005, 0.02)
            })
        
        self.benchmark_df = pd.DataFrame(bench_data)
        
        # Sector weights
        self.sector_weights = pd.Series({'Mining': 0.6, 'Energy': 0.4})
        
        # Initialize model
        self.model = PerformanceAttributionModel(
            self.portfolio_df,
            self.benchmark_df,
            self.sector_weights
        )
    
    def test_attribution_components_sum(self):
        """Test that attribution components sum to total active return"""
        results = self.model.calculate_attribution('2024-01-01', '2024-12-31')
        
        total_calculated = (
            results['allocation_effect'] + 
            results['selection_effect'] + 
            results['interaction_effect']
        )
        
        self.assertAlmostEqual(
            total_calculated,
            results['total_active_return'],
            places=6,
            msg="Attribution components should sum to total active return"
        )
    
    def test_weights_sum_to_one(self):
        """Test that portfolio weights sum to 1"""
        results = self.model.calculate_attribution('2024-01-01', '2024-12-31')
        sector_details = results['sector_details']
        
        weight_sum = sector_details['Portfolio_Weight'].sum()
        
        self.assertAlmostEqual(
            weight_sum,
            1.0,
            places=6,
            msg="Portfolio weights should sum to 1"
        )
    
    def test_sharpe_calculation(self):
        """Test Sharpe ratio calculation"""
        risk_metrics = self.model.risk_adjusted_attribution()
        
        # Sharpe ratio should be a finite number
        self.assertIsInstance(risk_metrics['portfolio_sharpe'], float)
        self.assertTrue(np.isfinite(risk_metrics['portfolio_sharpe']))
    
    def test_date_range_filtering(self):
        """Test that date range filtering works correctly"""
        results = self.model.calculate_attribution('2024-06-01', '2024-12-31')
        
        # Should only include data from specified range
        sector_details = results['sector_details']
        self.assertIsNotNone(sector_details)
        self.assertTrue(len(sector_details) > 0)
    
    def test_sector_returns_calculation(self):
        """Test sector returns are calculated correctly"""
        results = self.model.calculate_attribution('2024-01-01', '2024-12-31')
        sector_details = results['sector_details']
        
        # Each sector should have a return
        for _, row in sector_details.iterrows():
            self.assertTrue(np.isfinite(row['Monthly_Return']))
            self.assertTrue(isinstance(row['Sector'], str))

class TestTimeSeriesAnalysis(unittest.TestCase):
    """Test suite for time series analysis"""
    
    def setUp(self):
        """Set up test data"""
        from time_series_analysis import TimeSeriesAnalyzer
        
        dates = pd.date_range('2020-01-01', '2024-12-31', freq='ME') # Changed M to ME
        data = []
        
        for date in dates:
            data.append({
                'Date': date,
                'Sector': 'Mining',
                'Company': 'Mining_Co',
                'Monthly_Return': np.random.normal(0.01, 0.02),
                'Asset_Value': 100e6
            })
        
        self.returns_df = pd.DataFrame(data)
        self.analyzer = TimeSeriesAnalyzer(self.returns_df)
    
    def test_rolling_performance(self):
        """Test rolling performance calculation"""
        rolling = self.analyzer.rolling_performance(window=12)
        
        # Should return DataFrame with correct columns
        self.assertIsInstance(rolling, pd.DataFrame)
        self.assertIn('Rolling_Return', rolling.columns)
        self.assertIn('Rolling_Volatility', rolling.columns)
        self.assertIn('Rolling_Sharpe', rolling.columns)
    
    def test_stationarity_test(self):
        """Test stationarity test execution"""
        result = self.analyzer.test_stationarity()
        
        # Should return dictionary with required keys
        self.assertIn('adf_statistic', result)
        self.assertIn('p_value', result)
        self.assertIn('is_stationary', result)
        self.assertIsInstance(result['is_stationary'], bool)

class TestScenarioAnalysis(unittest.TestCase):
    """Test suite for scenario analysis"""
    
    def setUp(self):
        """Set up test data"""
        from scenario_analysis import ScenarioAnalysis
        
        dates = pd.date_range('2024-01-01', '2024-12-31', freq='ME') # Changed M to ME
        data = []
        
        for date in dates:
            for sector in ['Mining', 'Energy']:
                data.append({
                    'Date': date,
                    'Sector': sector,
                    'Company': f'{sector}_Co',
                    'Monthly_Return': np.random.normal(0.01, 0.02),
                    'Asset_Value': 100e6
                })
        
        self.portfolio_df = pd.DataFrame(data)
        
        bench_data = []
        for date in dates:
            bench_data.append({
                'Date': date,
                'ZSE_AllShare': 100,
                'Monthly_Return': 0.005
            })
        
        self.benchmark_df = pd.DataFrame(bench_data)
        
        self.analyzer = ScenarioAnalysis(self.portfolio_df, self.benchmark_df)
    
    def test_commodity_shock(self):
        """Test commodity shock scenario"""
        result = self.analyzer.commodity_shock_scenario({
            'Gold': -0.20,
            'Platinum': -0.15
        })
        
        # Should return proper structure
        self.assertIn('scenario_name', result)
        self.assertIn('original_return', result)
        self.assertIn('scenario_return', result)
        self.assertIn('impact', result)
        
        # Impact should be negative for negative shock
        self.assertLess(result['impact'], 0)
    
    def test_monte_carlo(self):
        """Test Monte Carlo simulation"""
        mc_results = self.analyzer.run_monte_carlo(num_simulations=100)
        
        # Should return statistics
        self.assertIn('mean', mc_results)
        self.assertIn('std', mc_results)
        self.assertIn('var_95', mc_results)
        
        # Should have correct number of simulations
        self.assertEqual(len(mc_results['returns']), 100)

if __name__ == '__main__':
    unittest.main()