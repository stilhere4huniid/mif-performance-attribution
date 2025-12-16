# MIF Sectoral Investment Performance Attribution Model

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Power BI](https://img.shields.io/badge/Power%20BI-Desktop-yellow.svg)
![Status](https://img.shields.io/badge/Status-Complete-success.svg)

A comprehensive financial analytics project demonstrating portfolio performance analysis, risk-adjusted returns, and Brinson-Fachler attribution methodology for Mutapa Investment Fund's multi-sector portfolio.

## 📊 Project Overview

This project implements a sophisticated performance attribution system for analyzing investment returns across 8 sectors (Mining, Energy, ICT, Transport, Agriculture, Financials, Real Estate, Manufacturing) with **$375.98 billion** in assets under management.

**Note:** This is an independent project using simulated data for demonstration purposes. It serves as a tribute to Mutapa Investment Fund and showcases financial data science capabilities.

## 🎯 Key Features

- **Brinson-Fachler Performance Attribution Model**
  - Allocation Effect Analysis
  - Selection Effect Analysis
  - Interaction Effect Decomposition

- **Risk-Adjusted Performance Metrics**
  - Sharpe Ratios by Sector
  - Volatility Analysis
  - Risk-Return Profiles

- **Time Series Analysis**
  - Rolling Performance Windows
  - Stationarity Testing
  - Trend Decomposition

- **Scenario Analysis**
  - Commodity Price Shock Simulations
  - Market Downturn Scenarios
  - Monte Carlo Simulations

- **Interactive Power BI Dashboard**
  - Executive Overview
  - Performance Attribution Breakdown
  - Sector Deep Dive
  - Market Context Analysis

## 🛠️ Technical Stack

**Programming Languages:**
- Python 3.9+ (Data Processing & Analysis)
- DAX (Power BI Measures)
- SQL (Data Relationships)

**Libraries & Tools:**
- **Data Analysis:** Pandas, NumPy
- **Statistical Modeling:** Statsmodels, SciPy
- **Visualization:** Matplotlib, Seaborn, Power BI
- **Testing:** Pytest

**Development Environment:**
- Jupyter Notebook
- Power BI Desktop
- Git/GitHub

## 📁 Project Structure
```
├── data/                      # Simulated portfolio and market data
├── python_scripts/            # Core Python modules
├── notebooks/                 # Jupyter analysis notebooks
├── powerbi/                   # Power BI dashboard files
├── tests/                     # Unit tests
├── screenshots/               # Dashboard visualizations
└── requirements.txt           # Python dependencies
```

## 🚀 Getting Started

### Prerequisites
```bash
Python 3.9+
Power BI Desktop
Jupyter Notebook
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YourUsername/mif-performance-attribution.git
cd mif-performance-attribution
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Generate data:
```bash
python python_scripts/generate_portfolio_data.py
python python_scripts/fetch_zse_data.py
python python_scripts/fetch_commodity_prices.py
```

5. Run analysis:
```bash
jupyter notebook notebooks/MIF_Performance_Dashboard.ipynb
```

6. Open Power BI Dashboard:
- Open `powerbi/MIF_Dashboard.pbix` in Power BI Desktop

## 📈 Key Results

- **Portfolio Annualized Return:** 12.4%
- **Portfolio Sharpe Ratio:** 0.892
- **Total Active Return:** 2.5%
- **Best Performing Sector:** ICT (15% annualized)
- **Largest Allocation:** Mining (30.14%)

## 📊 Dashboard Screenshots

### Executive Overview
![Executive Overview](screenshots/executive_overview.png)

### Performance Attribution
![Performance Attribution](screenshots/performance_attribution.png)

### Sector Deep Dive
![Sector Deep Dive](screenshots/sector_deep_dive.png)

### Market Context
![Market Context](screenshots/market_context.png)

## 🧪 Testing

Run unit tests:
```bash
python -m pytest tests/test_attribution.py -v
```

## 📚 Methodology

### Brinson-Fachler Attribution

The performance attribution follows the Brinson-Fachler methodology:
```
Total Active Return = Allocation Effect + Selection Effect + Interaction Effect

Where:
- Allocation Effect = (Portfolio Weight - Benchmark Weight) × Benchmark Return
- Selection Effect = Benchmark Weight × (Portfolio Return - Benchmark Return)
- Interaction Effect = (Portfolio Weight - Benchmark Weight) × (Portfolio Return - Benchmark Return)
```

### Data Generation

This project uses simulated data with realistic characteristics:
- **5 years** of monthly data (2020-2024)
- **8 sectors** with distinct risk-return profiles
- **23 companies** across the portfolio
- **Commodity price correlations** for Mining sector
- **Zimbabwe Stock Exchange** benchmark data

**Disclaimer:** All data is simulated for demonstration purposes and does not represent actual MIF holdings or performance.

## ⚠️ Limitations & Disclaimers

1. **Simulated Data:** This project uses synthetically generated data and does not reflect actual Mutapa Investment Fund performance or holdings.

2. **Educational Purpose:** Created as an independent project to demonstrate financial data science skills.

3. **Not Financial Advice:** This analysis is for educational and portfolio demonstration purposes only.

4. **Simplified Assumptions:** Real-world factors such as transaction costs, taxes, and liquidity constraints are not modeled.

## 🎓 Skills Demonstrated

- Financial Data Analysis
- Portfolio Performance Attribution
- Risk Management & Metrics
- Time Series Analysis
- Statistical Modeling
- Data Visualization
- Business Intelligence (Power BI)
- Python Programming
- SQL Database Design
- Unit Testing & Validation

## 📝 Future Enhancements

- [ ] Machine learning-based return predictions
- [ ] Real-time data integration
- [ ] Additional factor models (Fama-French 5-factor)
- [ ] Web-based interactive dashboard
- [ ] Automated report generation

## 👤 Author

**Adonis Chiruka**
- LinkedIn: [linkedin.com/in/adonis-chiruka-70b265323](https://www.linkedin.com/in/adonis-chiruka-70b265323)
- Email: chirukakatakudzwa61@gmail.com
- GitHub: [@stilhere4huniid](https://github.com/stilhere4huniid)

## 🙏 Acknowledgments

- Inspired by Mutapa Investment Fund's multi-sector investment approach
- Brinson-Fachler methodology for performance attribution
- Zimbabwe financial markets context

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Note:** This is an independent educational project and is not affiliated with, endorsed by, or representing the Mutapa Investment Fund.
