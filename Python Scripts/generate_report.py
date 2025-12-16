from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
from attribution_model import PerformanceAttributionModel

class MIFPerformanceReport:
    """Generate professional PDF report for MIF performance attribution"""
    
    def __init__(self, output_filename='MIF_Performance_Report.pdf'):
        self.output_filename = output_filename
        self.doc = SimpleDocTemplate(output_filename, pagesize=letter,
                                     rightMargin=72, leftMargin=72,
                                     topMargin=72, bottomMargin=18)
        self.styles = getSampleStyleSheet()
        self.story = []
        
        # Custom styles
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=12,
            spaceBefore=12
        )
        
    def add_title_page(self):
        """Create title page"""
        # Title
        title = Paragraph("Mutapa Investment Fund", self.title_style)
        subtitle = Paragraph("Sectoral Investment Performance Attribution Report", 
                           self.styles['Heading2'])
        
        # Date
        report_date = Paragraph(
            f"Report Date: {datetime.now().strftime('%B %d, %Y')}", 
            self.styles['Normal']
        )
        
        # Add to story
        self.story.append(Spacer(1, 2*inch))
        self.story.append(title)
        self.story.append(Spacer(1, 0.3*inch))
        self.story.append(subtitle)
        self.story.append(Spacer(1, 0.5*inch))
        self.story.append(report_date)
        self.story.append(PageBreak())
        
    def add_executive_summary(self, portfolio_df, attribution_results):
        """Add executive summary section"""
        self.story.append(Paragraph("Executive Summary", self.heading_style))
        
        # Calculate key metrics
        portfolio_returns = portfolio_df.groupby('Date')['Monthly_Return'].mean()
        annualized_return = (1 + portfolio_returns.mean()) ** 12 - 1
        volatility = portfolio_returns.std() * np.sqrt(12)
        sharpe = (portfolio_returns.mean() - 0.02/12) / portfolio_returns.std()
        
        total_value = portfolio_df['Asset_Value'].sum()
        num_companies = portfolio_df['Company'].nunique()
        
        summary_text = f"""
        This report presents a comprehensive performance attribution analysis of the Mutapa 
        Investment Fund portfolio for the period under review. The portfolio consists of 
        {num_companies} companies across 8 sectors with a total asset value of 
        ${total_value/1e9:.2f} billion.
        <br/><br/>
        <b>Key Performance Metrics:</b><br/>
        • Annualized Return: {annualized_return*100:.2f}%<br/>
        • Annualized Volatility: {volatility*100:.2f}%<br/>
        • Sharpe Ratio: {sharpe:.3f}<br/>
        • Total Active Return: {attribution_results['total_active_return']*100:.2f}%<br/>
        <br/>
        The performance attribution analysis reveals that {abs(attribution_results['allocation_effect']*100):.2f}% 
        of active returns were {'generated' if attribution_results['allocation_effect'] > 0 else 'lost'} 
        through sector allocation decisions, while {abs(attribution_results['selection_effect']*100):.2f}% 
        were {'generated' if attribution_results['selection_effect'] > 0 else 'lost'} through 
        stock selection within sectors.
        """
        
        self.story.append(Paragraph(summary_text, self.styles['Normal']))
        self.story.append(Spacer(1, 0.3*inch))
        
    def add_portfolio_composition(self, portfolio_df):
        """Add portfolio composition section"""
        self.story.append(Paragraph("Portfolio Composition", self.heading_style))
        
        # Calculate sector weights
        sector_summary = portfolio_df.groupby('Sector').agg({
            'Asset_Value': 'sum',
            'Monthly_Return': 'mean',
            'Company': 'nunique'
        }).reset_index()
        
        sector_summary['Weight'] = sector_summary['Asset_Value'] / sector_summary['Asset_Value'].sum()
        sector_summary['Annualized_Return'] = (1 + sector_summary['Monthly_Return']) ** 12 - 1
        
        # Create table
        data = [['Sector', 'Weight', 'Value (USD M)', '# Companies', 'Ann. Return']]
        
        for _, row in sector_summary.sort_values('Weight', ascending=False).iterrows():
            data.append([
                row['Sector'],
                f"{row['Weight']*100:.1f}%",
                f"${row['Asset_Value']/1e6:.0f}",
                str(int(row['Company'])),
                f"{row['Annualized_Return']*100:.1f}%"
            ])
        
        table = Table(data, colWidths=[2*inch, 1*inch, 1.2*inch, 1*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.3*inch))
        
    def add_attribution_analysis(self, attribution_results):
        """Add performance attribution section"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("Performance Attribution Analysis", self.heading_style))
        
        attribution_text = f"""
        The Brinson-Fachler performance attribution model was applied to decompose the portfolio's 
        active returns into three components:
        <br/><br/>
        <b>1. Allocation Effect ({attribution_results['allocation_effect']*100:.3f}%):</b><br/>
        Returns generated from overweighting or underweighting sectors relative to the benchmark.
        <br/><br/>
        <b>2. Selection Effect ({attribution_results['selection_effect']*100:.3f}%):</b><br/>
        Returns generated from selecting securities that outperform or underperform their sector benchmark.
        <br/><br/>
        <b>3. Interaction Effect ({attribution_results['interaction_effect']*100:.3f}%):</b><br/>
        Returns from the interaction between allocation and selection decisions.
        <br/><br/>
        <b>Total Active Return: {attribution_results['total_active_return']*100:.3f}%</b>
        """
        
        self.story.append(Paragraph(attribution_text, self.styles['Normal']))
        self.story.append(Spacer(1, 0.2*inch))
        
        # Sector-level attribution table
        sector_details = attribution_results['sector_details']
        
        data = [['Sector', 'Portfolio Wt.', 'Return', 'Allocation', 'Selection']]
        
        for _, row in sector_details.iterrows():
            data.append([
                row['Sector'],
                f"{row['Portfolio_Weight']*100:.1f}%",
                f"{row['Monthly_Return']*100:.2f}%",
                f"{row['Allocation_Effect']*100:.3f}%",
                f"{row['Selection_Effect']*100:.3f}%"
            ])
        
        table = Table(data, colWidths=[1.8*inch, 1.2*inch, 1*inch, 1.2*inch, 1.2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        self.story.append(table)
        
    def add_visualizations(self):
        """Add charts and visualizations"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("Performance Visualizations", self.heading_style))
        
        # Note: In production, you would save matplotlib figures and include them
        viz_text = """
        The following visualizations are included in the interactive dashboard:
        <br/><br/>
        • Sector allocation pie chart<br/>
        • Historical performance line chart<br/>
        • Risk-return scatter plot<br/>
        • Attribution waterfall chart<br/>
        • Rolling Sharpe ratio<br/>
        • Commodity price correlations<br/>
        <br/>
        Please refer to the Power BI dashboard or Jupyter Notebook for interactive visualizations.
        """
        
        self.story.append(Paragraph(viz_text, self.styles['Normal']))
        
    def add_conclusions(self):
        """Add conclusions and recommendations"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("Conclusions & Recommendations", self.heading_style))
        
        conclusions = """
        <b>Key Findings:</b><br/>
        1. The portfolio demonstrates strong diversification across sectors<br/>
        2. Mining sector shows highest correlation with commodity price movements<br/>
        3. Sector allocation decisions have been the primary driver of active returns<br/>
        4. Stock selection within sectors has opportunities for improvement<br/>
        <br/>
        <b>Recommendations:</b><br/>
        1. Continue monitoring commodity price exposure in Mining sector<br/>
        2. Review underperforming assets within high-allocation sectors<br/>
        3. Consider rebalancing to capitalize on emerging sector opportunities<br/>
        4. Enhance stock selection processes to capture additional alpha<br/>
        5. Implement more sophisticated risk management for volatile sectors<br/>
        """
        
        self.story.append(Paragraph(conclusions, self.styles['Normal']))
        
    def generate(self, portfolio_df, attribution_results):
        """Generate complete report"""
        self.add_title_page()
        self.add_executive_summary(portfolio_df, attribution_results)
        self.add_portfolio_composition(portfolio_df)
        self.add_attribution_analysis(attribution_results)
        self.add_visualizations()
        self.add_conclusions()
        
        self.doc.build(self.story)
        print(f"Report generated: {self.output_filename}")

# Usage
if __name__ == "__main__":
    # Load data
    portfolio_df = pd.read_csv('mif_portfolio_returns.csv', parse_dates=['Date'])
    benchmark_df = pd.read_csv('zse_benchmark_data.csv', parse_dates=['Date'])
    
    # Run attribution
    sector_weights = portfolio_df.groupby('Sector')['Asset_Value'].sum()
    sector_weights = sector_weights / sector_weights.sum()
    
    model = PerformanceAttributionModel(portfolio_df, benchmark_df, sector_weights)
    attribution_results = model.calculate_attribution('2024-01-01', '2024-12-31')
    
    # Generate report
    report = MIFPerformanceReport('MIF_Performance_Attribution_Report.pdf')
    report.generate(portfolio_df, attribution_results)