#!/usr/bin/env python3
"""
Data Analysis Script for Pollinator-Integrated Vegetable Farming

This script processes and analyzes data on pollinator integration in vegetable farming.
It generates visualizations, summary statistics, and comparative analyses.

Usage:
    python data_analysis.py

Requirements:
    pandas, matplotlib, seaborn, numpy
    
    Install with: pip install -r requirements.txt
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Set style for plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


class PollinatorAnalysis:
    """Analyze pollinator farming integration data."""
    
    def __init__(self, data_dir='data'):
        """Initialize with data directory path."""
        self.data_dir = Path(data_dir)
        self.results_dir = Path('analysis/results')
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.data = {}
        
    def load_data(self):
        """Load all CSV data files."""
        try:
            self.data['economic'] = pd.read_csv(
                self.data_dir / 'economic_benefits.csv'
            )
            self.data['crops'] = pd.read_csv(
                self.data_dir / 'crop_dependency.csv'
            )
            self.data['pollinators'] = pd.read_csv(
                self.data_dir / 'pollinator_comparison.csv'
            )
            print("✅ All data files loaded successfully")
            return True
        except FileNotFoundError as e:
            print(f"❌ Error loading data: {e}")
            print(f"Make sure CSV files exist in '{self.data_dir}' directory")
            return False
    
    def display_data_summary(self):
        """Display summary of loaded data."""
        print("\n" + "="*60)
        print("DATA SUMMARY")
        print("="*60)
        
        if 'economic' in self.data:
            print("\n📊 Economic Benefits Data:")
            print(f"  Records: {len(self.data['economic'])}")
            print(f"  Columns: {', '.join(self.data['economic'].columns.tolist())}")
        
        if 'crops' in self.data:
            print("\n🌽 Crop Dependency Data:")
            print(f"  Records: {len(self.data['crops'])}")
            print(f"  Crops: {', '.join(self.data['crops']['Crop Type'].tolist())}")
        
        if 'pollinators' in self.data:
            print("\n🐝 Pollinator Comparison Data:")
            print(f"  Records: {len(self.data['pollinators'])}")
            print(f"  Types: {', '.join(self.data['pollinators']['Pollinator Type'].tolist())}")
    
    def analyze_economic_benefits(self):
        """Analyze economic benefits data."""
        print("\n" + "="*60)
        print("ECONOMIC ANALYSIS")
        print("="*60)
        
        if 'economic' not in self.data:
            print("❌ Economic data not loaded")
            return
        
        df = self.data['economic']
        print("\nEconomic Benefits Summary:")
        print("-" * 60)
        for idx, row in df.iterrows():
            print(f"\n{row['Benefit Type']}:")
            print(f"  Value: {row['Value']}")
            print(f"  Description: {row['Description']}")
    
    def analyze_crop_dependency(self):
        """Analyze crop pollination dependency."""
        print("\n" + "="*60)
        print("CROP POLLINATION DEPENDENCY ANALYSIS")
        print("="*60)
        
        if 'crops' not in self.data:
            print("❌ Crop data not loaded")
            return
        
        df = self.data['crops']
        
        # Dependency breakdown
        dependency_counts = df['Pollination Dependency'].value_counts()
        print("\nPollination Dependency Distribution:")
        print("-" * 60)
        for dep, count in dependency_counts.items():
            percentage = (count / len(df)) * 100
            print(f"  {dep}: {count} crops ({percentage:.1f}%)")
        
        # Yield impact analysis
        print("\nYield Impact Distribution:")
        print("-" * 60)
        yield_counts = df['Yield Impact'].value_counts()
        for impact, count in yield_counts.items():
            percentage = (count / len(df)) * 100
            print(f"  {impact}: {count} crops ({percentage:.1f}%)")
    
    def analyze_pollinator_comparison(self):
        """Analyze pollinator type comparisons."""
        print("\n" + "="*60)
        print("POLLINATOR COMPARISON ANALYSIS")
        print("="*60)
        
        if 'pollinators' not in self.data:
            print("❌ Pollinator data not loaded")
            return
        
        df = self.data['pollinators']
        print("\nManaged Pollinator Types Comparison:")
        print("-" * 60)
        print(df.to_string(index=False))
        
        # Efficiency analysis
        print("\n\nManagement Level Ranking:")
        print("-" * 60)
        management_map = {
            'High': 3,
            'Medium': 2,
            'Low': 1,
            'Habitat-based': 1.5
        }
        df_sorted = df.copy()
        df_sorted['Management_Level_Score'] = df_sorted['Management Level'].map(management_map)
        df_sorted = df_sorted.sort_values('Management_Level_Score', ascending=False)
        for idx, row in df_sorted.iterrows():
            print(f"  {row['Pollinator Type']}: {row['Management Level']}")
    
    def create_crop_dependency_chart(self):
        """Create visualization of crop pollination dependency."""
        if 'crops' not in self.data:
            print("❌ Cannot create crop chart: data not loaded")
            return
        
        df = self.data['crops']
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Dependency distribution
        dependency_counts = df['Pollination Dependency'].value_counts()
        colors = ['#FF6B6B', '#FFA500', '#4ECDC4']
        axes[0].bar(dependency_counts.index, dependency_counts.values, color=colors)
        axes[0].set_title('Crop Distribution by Pollination Dependency', fontsize=12, fontweight='bold')
        axes[0].set_ylabel('Number of Crops')
        axes[0].set_xlabel('Dependency Level')
        
        # Yield impact distribution
        yield_counts = df['Yield Impact'].value_counts()
        colors_yield = ['#FF6B6B', '#4ECDC4', '#FFA500']
        axes[1].bar(yield_counts.index, yield_counts.values, color=colors_yield)
        axes[1].set_title('Crop Distribution by Yield Impact', fontsize=12, fontweight='bold')
        axes[1].set_ylabel('Number of Crops')
        axes[1].set_xlabel('Yield Impact Category')
        
        plt.tight_layout()
        filename = self.results_dir / 'crop_dependency_analysis.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✅ Chart saved: {filename}")
        plt.close()
    
    def create_pollinator_comparison_chart(self):
        """Create comparison chart of different pollinator types."""
        if 'pollinators' not in self.data:
            print("❌ Cannot create pollinator chart: data not loaded")
            return
        
        df = self.data['pollinators']
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Extract numeric management level values
        management_map = {
            'High': 3,
            'Medium': 2,
            'Low': 1,
            'Habitat-based': 1.5
        }
        
        management_scores = df['Management Level'].map(management_map)
        
        # Create grouped bar chart
        x = np.arange(len(df))
        width = 0.35
        
        ax.bar(x - width/2, management_scores, width, label='Management Level', color='#FF6B6B', alpha=0.8)
        
        plt.xlabel('Pollinator Type', fontweight='bold')
        plt.ylabel('Score', fontweight='bold')
        plt.title('Pollinator Management Complexity by Type', fontsize=14, fontweight='bold')
        plt.xticks(x, df['Pollinator Type'], rotation=45, ha='right')
        plt.legend()
        
        plt.tight_layout()
        filename = self.results_dir / 'pollinator_comparison.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✅ Chart saved: {filename}")
        plt.close()
    
    def generate_statistics_report(self):
        """Generate a comprehensive statistics report."""
        report_path = self.results_dir / 'statistics_report.txt'
        
        with open(report_path, 'w') as f:
            f.write("="*70 + "\n")
            f.write("POLLINATOR-INTEGRATED VEGETABLE FARMING - STATISTICS REPORT\n")
            f.write("="*70 + "\n\n")
            
            # Economic data
            if 'economic' in self.data:
                f.write("ECONOMIC BENEFITS\n")
                f.write("-"*70 + "\n")
                df = self.data['economic']
                for idx, row in df.iterrows():
                    f.write(f"{row['Benefit Type']}\n")
                    f.write(f"  Value: {row['Value']}\n")
                    f.write(f"  Description: {row['Description']}\n\n")
            
            # Crop data
            if 'crops' in self.data:
                f.write("\nCROP POLLINATION DEPENDENCY\n")
                f.write("-"*70 + "\n")
                df = self.data['crops']
                f.write(f"Total crops analyzed: {len(df)}\n")
                f.write(f"\nDependency distribution:\n")
                for dep, count in df['Pollination Dependency'].value_counts().items():
                    f.write(f"  {dep}: {count} ({count/len(df)*100:.1f}%)\n")
            
            # Pollinator data
            if 'pollinators' in self.data:
                f.write("\n\nPOLLINATOR TYPES ANALYZED\n")
                f.write("-"*70 + "\n")
                df = self.data['pollinators']
                f.write(f"Number of pollinator types: {len(df)}\n")
                f.write(f"Types: {', '.join(df['Pollinator Type'].tolist())}\n")
            
            f.write("\n" + "="*70 + "\n")
            f.write("Report generated for Pollinator-Integrated Vegetable Farming project\n")
            f.write("="*70 + "\n")
        
        print(f"✅ Report saved: {report_path}")
    
    def run_analysis(self):
        """Run complete analysis pipeline."""
        print("\n" + "🐝 "*30)
        print("POLLINATOR-INTEGRATED VEGETABLE FARMING - DATA ANALYSIS")
        print("🐝 "*30 + "\n")
        
        # Load data
        if not self.load_data():
            return
        
        # Display summaries
        self.display_data_summary()
        self.analyze_economic_benefits()
        self.analyze_crop_dependency()
        self.analyze_pollinator_comparison()
        
        # Create visualizations
        print("\n" + "="*60)
        print("GENERATING VISUALIZATIONS")
        print("="*60)
        self.create_crop_dependency_chart()
        self.create_pollinator_comparison_chart()
        self.generate_statistics_report()
        
        print("\n" + "="*60)
        print("✅ ANALYSIS COMPLETE")
        print("="*60)
        print(f"\nResults saved to: {self.results_dir}")
        print("\nGenerated files:")
        print("  - crop_dependency_analysis.png")
        print("  - pollinator_comparison.png")
        print("  - statistics_report.txt")


def main():
    """Main entry point."""
    analyzer = PollinatorAnalysis()
    analyzer.run_analysis()


if __name__ == '__main__':
    main()
