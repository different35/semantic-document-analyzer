#!/usr/bin/env python3
"""
Demo script for Football Sports Analytics
This demonstrates the complete analysis pipeline
"""

from core.sports_analytics import SportsAnalytics
from core.visualizations import AnalyticsVisualizer
import json
import pandas as pd

def main():
    print("⚽ Football Sports Analytics Demo")
    print("=" * 50)
    
    # Load sample data
    print("\n📁 Loading sample football data...")
    with open('sample_football_data.json', 'r') as f:
        data = json.load(f)
    
    # Initialize analytics
    analytics = SportsAnalytics()
    analytics.load_json_data(data)
    
    print(f"✅ Data loaded: {analytics.data.shape[0]} teams, {analytics.data.shape[1]} features")
    print(f"   Features: {', '.join(analytics.data.columns.tolist())}")
    
    # Run comprehensive analysis
    target = 'points'
    print(f"\n🎯 Target variable: {target}")
    print("\n🔄 Running comprehensive analysis...")
    
    # 1. Pearson Correlation
    print("\n1️⃣  Computing Pearson Correlations...")
    pearson_results = analytics.pearson_correlation_analysis(target)
    top_corr = pearson_results['top_correlations'][0]
    print(f"   Top correlation: {top_corr['feature1']} vs {top_corr['feature2']} = {top_corr['correlation']:.4f}")
    
    # 2. Regression Models
    print("\n2️⃣  Training Regression Models...")
    reg_results = analytics.regression_models_analysis(target, cv_folds=5)
    print("   Model Performance (R² Score):")
    for model, metrics in sorted(reg_results.items(), key=lambda x: x[1]['r2_score'], reverse=True):
        print(f"      {model:25s}: {metrics['r2_score']:.4f}")
    
    # 3. Decision Trees
    print("\n3️⃣  Building Decision Trees...")
    dt_results = analytics.decision_tree_analysis(target, task='regression', cv_folds=5)
    for model, metrics in dt_results.items():
        print(f"   {model}: R²={metrics.get('r2_score', 'N/A'):.4f}")
    
    # 4. Time Series
    print("\n4️⃣  Time Series Analysis...")
    try:
        ts_results = analytics.time_series_analysis(target)
        print(f"   AIC: {ts_results.get('aic', 'N/A'):.2f}")
        print(f"   Forecast (next 10): {ts_results.get('forecast', [])[0]:.2f} ...")
    except Exception as e:
        print(f"   Time series analysis skipped: {str(e)[:50]}")
    
    # 5. Deep Learning
    print("\n5️⃣  Training Deep Learning Model...")
    dl_results = analytics.deep_learning_correlation(target, epochs=30)
    print(f"   Neural Network R²: {dl_results['r2_score']:.4f}")
    print(f"   Final validation loss: {dl_results['final_val_loss']:.4f}")
    
    # 6. Mind Vortex
    print("\n6️⃣  🌀 Activating Mind Vortex Evaluation...")
    vortex_results = analytics.mind_vortex_evaluation(target)
    print(f"   Total variations tested: {vortex_results['comparative_metrics']['total_variations_tested']}")
    print(f"   Best R² score: {vortex_results['comparative_metrics']['best_r2_score']:.4f}")
    print(f"   Average R² score: {vortex_results['comparative_metrics']['average_r2_score']:.4f}")
    
    if vortex_results['best_model']:
        best_name, best_metrics = vortex_results['best_model']
        print(f"\n   🏆 Best Model: {best_name}")
        print(f"      R² Score: {best_metrics.get('r2_score', 0):.4f}")
    
    # Generate contribution summary
    print("\n7️⃣  Generating Contribution Summary...")
    contrib_summary = analytics.generate_contribution_summary()
    
    print("\n   Top Feature Importance:")
    for i, (feature, importance) in enumerate(list(contrib_summary['feature_importance_aggregate'].items())[:5], 1):
        print(f"      {i}. {feature:25s}: {importance:.4f}")
    
    # Dynamic Impact Analysis
    if 'dynamic_impact_analysis' in contrib_summary and contrib_summary['dynamic_impact_analysis']:
        print("\n   ⚡ Dynamic Predictive Power Impact (Top 5):")
        for i, impact_data in enumerate(contrib_summary['dynamic_impact_analysis'][:5], 1):
            print(f"      {i}. {impact_data['feature']:25s}: Contribution = {impact_data['contribution']:.2f}%, Single R² = {impact_data['single_r2']:.4f}")
    
    # Save results
    print("\n💾 Saving results...")
    with open('demo_analysis_results.json', 'w') as f:
        json.dump(analytics.get_all_results(), f, indent=2)
    print("   ✅ Results saved to demo_analysis_results.json")
    
    with open('demo_contribution_summary.json', 'w') as f:
        json.dump(contrib_summary, f, indent=2)
    print("   ✅ Summary saved to demo_contribution_summary.json")
    
    # Display predictive power ranking
    print("\n📊 Predictive Power Ranking:")
    print("-" * 60)
    for i, model_info in enumerate(vortex_results['predictive_power_ranking'][:5], 1):
        print(f"   {i}. {model_info['model']:35s} | R²={model_info['r2_score']:.4f} | Type: {model_info['type']}")
    
    print("\n" + "=" * 50)
    print("✅ Demo completed successfully!")
    print("\nNext steps:")
    print("  1. Run 'streamlit run app.py' to use the interactive UI")
    print("  2. Upload your own JSON data for analysis")
    print("  3. Explore the Mind Vortex visualizations")
    print("=" * 50)

if __name__ == "__main__":
    main()
