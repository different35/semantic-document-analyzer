import streamlit as st
import json
import pandas as pd
import numpy as np
from core.sports_analytics import SportsAnalytics
from core.visualizations import AnalyticsVisualizer

st.set_page_config(
    page_title="Football Sports Analytics ⚽", 
    page_icon="⚽", 
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analytics' not in st.session_state:
    st.session_state.analytics = SportsAnalytics()
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False

# Header
st.markdown('<p class="main-header">⚽ Football Sports Analytics - Advanced Correlation Engine</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Autonomous Multi-Model Analysis with Mind Vortex Technology</p>', unsafe_allow_html=True)

# Sidebar for data upload and configuration
with st.sidebar:
    st.header("📁 Data Upload")
    uploaded_files = st.file_uploader(
        "Upload JSON Data File(s)", 
        type=['json'],
        accept_multiple_files=True,
        help="Upload one or more JSON files with football statistics or sports data"
    )
    
    if uploaded_files is not None and len(uploaded_files) > 0:
        try:
            # Load all JSON files
            if len(uploaded_files) == 1:
                # Single file - load normally
                json_data = json.load(uploaded_files[0])
            else:
                # Multiple files - load all and combine
                json_data = []
                for uploaded_file in uploaded_files:
                    file_data = json.load(uploaded_file)
                    json_data.append(file_data)
            
            st.session_state.analytics.load_json_data(json_data)
            st.session_state.data_loaded = True
            
            if len(uploaded_files) == 1:
                st.success(f"✅ Data loaded successfully from 1 file!")
            else:
                st.success(f"✅ Data loaded successfully from {len(uploaded_files)} files!")
            
            # Show data preview
            st.subheader("Data Preview")
            st.dataframe(st.session_state.analytics.data.head(), use_container_width=True)
            
            # Data info
            st.info(f"📊 Shape: {st.session_state.analytics.data.shape[0]} rows × {st.session_state.analytics.data.shape[1]} columns")
            
        except Exception as e:
            st.error(f"❌ Error loading data: {str(e)}")
    
    st.divider()
    
    st.header("⚙️ Analysis Configuration")
    
    if st.session_state.data_loaded:
        numeric_cols = st.session_state.analytics.data.select_dtypes(include=[np.number]).columns.tolist()
        all_cols = st.session_state.analytics.data.columns.tolist()
        
        target_column = st.selectbox(
            "Select Target Variable",
            options=numeric_cols,
            help="The variable you want to predict or analyze"
        )
        
        feature_columns = st.multiselect(
            "Select Feature Variables (optional)",
            options=[col for col in numeric_cols if col != target_column],
            help="Leave empty to use all available features"
        )
        
        cv_folds = st.slider("Cross-Validation Folds", 3, 10, 5)
        
        st.divider()
        
        # Analysis techniques selection
        st.subheader("📈 Analysis Techniques")
        run_pearson = st.checkbox("Pearson Correlation", value=True)
        run_regression = st.checkbox("Regression Models", value=True)
        run_decision_trees = st.checkbox("Decision Trees & Logistic Regression", value=True)
        run_time_series = st.checkbox("Time Series Analysis", value=False)
        run_deep_learning = st.checkbox("Deep Learning Correlation", value=True)
        run_mind_vortex = st.checkbox("🌀 Mind Vortex Evaluation", value=True)

# Main content area
if st.session_state.data_loaded:
    
    # Start Analysis Button
    if st.button("🚀 Start Autonomous Analysis", type="primary", use_container_width=True):
        
        with st.spinner("🔄 Running comprehensive analysis..."):
            results_container = st.container()
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            total_steps = sum([run_pearson, run_regression, run_decision_trees, 
                             run_time_series, run_deep_learning, run_mind_vortex])
            current_step = 0
            
            # Run selected analyses
            if run_pearson:
                status_text.text("🔍 Computing Pearson Correlations...")
                st.session_state.analytics.pearson_correlation_analysis(target_column)
                current_step += 1
                progress_bar.progress(current_step / total_steps)
            
            if run_regression:
                status_text.text("📊 Training Regression Models...")
                st.session_state.analytics.regression_models_analysis(
                    target_column, 
                    feature_columns if feature_columns else None,
                    cv_folds=cv_folds
                )
                current_step += 1
                progress_bar.progress(current_step / total_steps)
            
            if run_decision_trees:
                status_text.text("🌳 Building Decision Trees...")
                st.session_state.analytics.decision_tree_analysis(
                    target_column,
                    feature_columns if feature_columns else None,
                    task='regression',
                    cv_folds=cv_folds
                )
                current_step += 1
                progress_bar.progress(current_step / total_steps)
            
            if run_time_series:
                status_text.text("📈 Analyzing Time Series...")
                st.session_state.analytics.time_series_analysis(target_column)
                current_step += 1
                progress_bar.progress(current_step / total_steps)
            
            if run_deep_learning:
                status_text.text("🧠 Training Deep Learning Model...")
                st.session_state.analytics.deep_learning_correlation(
                    target_column,
                    feature_columns if feature_columns else None,
                    epochs=50
                )
                current_step += 1
                progress_bar.progress(current_step / total_steps)
            
            if run_mind_vortex:
                status_text.text("🌀 Activating Mind Vortex...")
                st.session_state.analytics.mind_vortex_evaluation(
                    target_column,
                    feature_columns if feature_columns else None
                )
                current_step += 1
                progress_bar.progress(current_step / total_steps)
            
            status_text.text("✅ Analysis Complete!")
            st.session_state.analysis_complete = True
        
        st.success("🎉 Analysis completed successfully!")
        st.balloons()
    
    # Display Results
    if st.session_state.analysis_complete:
        st.divider()
        st.header("📊 Analysis Results")
        
        # Create tabs for different views
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🌀 Mind Vortex", 
            "📈 Correlations", 
            "🤖 Model Performance",
            "📊 Visualizations",
            "📋 Detailed Results"
        ])
        
        with tab1:
            st.subheader("🌀 Mind Vortex: Multi-Model Evaluation")
            
            if 'mind_vortex' in st.session_state.analytics.results:
                vortex_results = st.session_state.analytics.results['mind_vortex']
                
                # Key metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(
                        "Total Variations Tested",
                        vortex_results['comparative_metrics']['total_variations_tested']
                    )
                with col2:
                    st.metric(
                        "Best R² Score",
                        f"{vortex_results['comparative_metrics']['best_r2_score']:.4f}"
                    )
                with col3:
                    st.metric(
                        "Average R² Score",
                        f"{vortex_results['comparative_metrics']['average_r2_score']:.4f}"
                    )
                
                # Mind Vortex visualization
                vortex_fig = AnalyticsVisualizer.create_mind_vortex_visualization(vortex_results)
                if vortex_fig:
                    st.plotly_chart(vortex_fig, use_container_width=True)
                
                # Metrics comparison table
                metrics_table = AnalyticsVisualizer.create_metrics_comparison_table(vortex_results)
                if metrics_table:
                    st.plotly_chart(metrics_table, use_container_width=True)
                
                # Best model info
                if vortex_results['best_model']:
                    st.success(f"🏆 Best Model: **{vortex_results['best_model'][0]}** (R² = {vortex_results['best_model'][1].get('r2_score', 0):.4f})")
        
        with tab2:
            st.subheader("📈 Correlation Analysis")
            
            if 'pearson_correlation' in st.session_state.analytics.results:
                corr_results = st.session_state.analytics.results['pearson_correlation']
                
                # Correlation heatmap
                if 'correlation_matrix' in corr_results:
                    corr_fig = AnalyticsVisualizer.create_correlation_heatmap(
                        corr_results['correlation_matrix']
                    )
                    st.plotly_chart(corr_fig, use_container_width=True)
                
                # Top correlations
                st.subheader("Top Correlations")
                if corr_results.get('top_correlations'):
                    top_corr_df = pd.DataFrame(corr_results['top_correlations'][:10])
                    st.dataframe(
                        top_corr_df[['feature1', 'feature2', 'correlation']],
                        use_container_width=True
                    )
                
                # Target correlations
                if corr_results.get('target_correlations'):
                    st.subheader(f"Correlations with Target: {target_column}")
                    target_corr_df = pd.DataFrame([
                        {'Feature': k, 'Correlation': v}
                        for k, v in list(corr_results['target_correlations'].items())[:10]
                    ])
                    st.dataframe(target_corr_df, use_container_width=True)
        
        with tab3:
            st.subheader("🤖 Model Performance Comparison")
            
            if 'regression_models' in st.session_state.analytics.results:
                reg_results = st.session_state.analytics.results['regression_models']
                
                # Model comparison chart
                model_fig = AnalyticsVisualizer.create_model_comparison_chart(reg_results)
                st.plotly_chart(model_fig, use_container_width=True)
                
                # Detailed metrics
                st.subheader("Detailed Model Metrics")
                for model_name, metrics in reg_results.items():
                    with st.expander(f"📊 {model_name}"):
                        col1, col2, col3, col4 = st.columns(4)
                        col1.metric("R² Score", f"{metrics.get('r2_score', 0):.4f}")
                        col2.metric("RMSE", f"{metrics.get('rmse', 0):.4f}")
                        col3.metric("CV Mean", f"{metrics.get('cv_mean', 0):.4f}")
                        col4.metric("AIC", f"{metrics.get('aic', 0):.2f}")
                        
                        if 'feature_importance' in metrics:
                            st.write("**Feature Importance:**")
                            feat_imp_fig = AnalyticsVisualizer.create_feature_importance_chart(
                                metrics['feature_importance']
                            )
                            st.plotly_chart(feat_imp_fig, use_container_width=True)
        
        with tab4:
            st.subheader("📊 Comprehensive Visualizations")
            
            # Contribution dashboard
            contribution_summary = st.session_state.analytics.generate_contribution_summary()
            contrib_fig = AnalyticsVisualizer.create_contribution_dashboard(contribution_summary)
            st.plotly_chart(contrib_fig, use_container_width=True)
            
            # Time series if available
            if 'time_series_analysis' in st.session_state.analytics.results:
                ts_results = st.session_state.analytics.results['time_series_analysis']
                if 'forecast' in ts_results and 'error' not in ts_results:
                    st.subheader("Time Series Forecast")
                    historical = st.session_state.analytics.data[target_column].values
                    forecast = ts_results['forecast']
                    ts_fig = AnalyticsVisualizer.create_time_series_forecast_plot(
                        historical, forecast
                    )
                    st.plotly_chart(ts_fig, use_container_width=True)
            
            # Deep learning training history
            if 'deep_learning_correlation' in st.session_state.analytics.results:
                dl_results = st.session_state.analytics.results['deep_learning_correlation']
                if 'training_history' in dl_results:
                    st.subheader("Deep Learning Training History")
                    history_df = pd.DataFrame({
                        'Epoch': range(len(dl_results['training_history']['loss'])),
                        'Training Loss': dl_results['training_history']['loss'],
                        'Validation Loss': dl_results['training_history']['val_loss']
                    })
                    st.line_chart(history_df.set_index('Epoch'))
        
        with tab5:
            st.subheader("📋 Detailed Results (JSON)")
            
            all_results = st.session_state.analytics.get_all_results()
            
            # Filter results
            selected_analysis = st.selectbox(
                "Select Analysis",
                options=list(all_results.keys())
            )
            
            if selected_analysis:
                st.json(all_results[selected_analysis])
        
        # Download results
        st.divider()
        col1, col2 = st.columns(2)
        
        with col1:
            # Download all results as JSON
            all_results_json = json.dumps(
                st.session_state.analytics.get_all_results(),
                indent=2
            )
            st.download_button(
                label="📥 Download Results (JSON)",
                data=all_results_json,
                file_name="sports_analytics_results.json",
                mime="application/json"
            )
        
        with col2:
            # Download contribution summary
            contrib_summary_json = json.dumps(
                st.session_state.analytics.generate_contribution_summary(),
                indent=2
            )
            st.download_button(
                label="📥 Download Contribution Summary (JSON)",
                data=contrib_summary_json,
                file_name="contribution_summary.json",
                mime="application/json"
            )

else:
    # Initial state - no data loaded
    st.info("👈 Please upload one or more JSON data files from the sidebar to begin analysis")
    
    # Sample data format
    with st.expander("📖 Sample Data Format"):
        st.markdown("""
        **Expected JSON Format:**
        
        You can upload single or multiple JSON files. Each file should contain:
        
        ```json
        [
            {
                "team": "Team A",
                "goals": 2.5,
                "shots": 15,
                "possession": 58.3,
                "passes": 450,
                "tackles": 18,
                "wins": 1
            },
            {
                "team": "Team B",
                "goals": 1.8,
                "shots": 12,
                "possession": 52.1,
                "passes": 380,
                "tackles": 22,
                "wins": 0
            }
        ]
        ```
        
        Or as a dictionary with lists:
        
        ```json
        {
            "team": ["Team A", "Team B"],
            "goals": [2.5, 1.8],
            "shots": [15, 12],
            "possession": [58.3, 52.1]
        }
        ```
        """)
    
    # Features overview
    with st.expander("✨ Features Overview"):
        st.markdown("""
        ### Advanced Analytics Techniques
        
        1. **Pearson Correlation Analysis**: Identify linear relationships between variables
        2. **Multiple Regression Models**: Linear, Ridge, Lasso, Random Forest, Gradient Boosting
        3. **Decision Trees & Logistic Regression**: Classification and feature importance
        4. **Time Series Analysis**: ARIMA-based forecasting
        5. **Deep Learning Correlation**: Neural network-based predictions
        6. **🌀 Mind Vortex**: Comprehensive multi-model evaluation system
        
        ### Key Capabilities
        
        - 🤖 **Autonomous Operation**: Minimal user input required
        - 📊 **Interactive Visualizations**: Explore results with interactive charts
        - 🔍 **Cross-Validation**: Robust model evaluation
        - 📈 **Predictive Power Analysis**: Compare model effectiveness
        - 💡 **Feature Importance**: Understand key drivers
        - 🎯 **Multi-Model Comparison**: R², Accuracy, AIC, Loss metrics
        """)
