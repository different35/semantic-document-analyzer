import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

class AnalyticsVisualizer:
    """Create interactive visualizations for sports analytics results"""
    
    @staticmethod
    def create_correlation_heatmap(corr_matrix_dict):
        """Create interactive correlation heatmap"""
        df = pd.DataFrame(corr_matrix_dict)
        
        fig = go.Figure(data=go.Heatmap(
            z=df.values,
            x=df.columns.tolist(),
            y=df.columns.tolist(),
            colorscale='RdBu_r',
            zmid=0,
            text=np.round(df.values, 2),
            texttemplate='%{text}',
            textfont={"size": 10},
            colorbar=dict(title="Correlation")
        ))
        
        fig.update_layout(
            title='Correlation Matrix Heatmap',
            width=800,
            height=700,
            xaxis={'side': 'bottom'},
            yaxis={'side': 'left'}
        )
        
        return fig
    
    @staticmethod
    def create_model_comparison_chart(model_results):
        """Create bar chart comparing model performances"""
        models = list(model_results.keys())
        r2_scores = [model_results[m].get('r2_score', 0) for m in models]
        cv_scores = [model_results[m].get('cv_mean', 0) for m in models]
        
        fig = go.Figure(data=[
            go.Bar(name='R² Score', x=models, y=r2_scores, marker_color='lightblue'),
            go.Bar(name='CV Mean Score', x=models, y=cv_scores, marker_color='darkblue')
        ])
        
        fig.update_layout(
            title='Model Performance Comparison',
            xaxis_title='Models',
            yaxis_title='Score',
            barmode='group',
            height=500,
            xaxis={'tickangle': -45}
        )
        
        return fig
    
    @staticmethod
    def create_feature_importance_chart(feature_importance_dict):
        """Create horizontal bar chart for feature importance"""
        features = list(feature_importance_dict.keys())[:15]
        importances = [feature_importance_dict[f] for f in features]
        
        fig = go.Figure(go.Bar(
            x=importances,
            y=features,
            orientation='h',
            marker=dict(
                color=importances,
                colorscale='Viridis',
                colorbar=dict(title="Importance")
            )
        ))
        
        fig.update_layout(
            title='Feature Importance',
            xaxis_title='Importance Score',
            yaxis_title='Features',
            height=500,
            yaxis={'autorange': 'reversed'}
        )
        
        return fig
    
    @staticmethod
    def create_time_series_forecast_plot(historical_data, forecast_data, title="Time Series Forecast"):
        """Create time series plot with forecast"""
        fig = go.Figure()
        
        # Historical data
        fig.add_trace(go.Scatter(
            x=list(range(len(historical_data))),
            y=historical_data,
            mode='lines+markers',
            name='Historical Data',
            line=dict(color='blue')
        ))
        
        # Forecast
        forecast_x = list(range(len(historical_data), len(historical_data) + len(forecast_data)))
        fig.add_trace(go.Scatter(
            x=forecast_x,
            y=forecast_data,
            mode='lines+markers',
            name='Forecast',
            line=dict(color='red', dash='dash')
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title='Time',
            yaxis_title='Value',
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_mind_vortex_visualization(vortex_results):
        """Create comprehensive Mind Vortex visualization"""
        ranking = vortex_results.get('predictive_power_ranking', [])
        
        if not ranking:
            return None
        
        models = [r['model'] for r in ranking]
        r2_scores = [r['r2_score'] for r in ranking]
        types = [r['type'] for r in ranking]
        
        # Color map for model types
        color_map = {
            'regression': 'lightblue',
            'tree': 'lightgreen',
            'deep_learning': 'coral'
        }
        colors = [color_map.get(t, 'gray') for t in types]
        
        # Create spiral/vortex effect using polar coordinates
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Predictive Power Ranking', 'Model Type Distribution', 
                          'R² Score Distribution', 'Performance Spiral'),
            specs=[[{'type': 'bar'}, {'type': 'pie'}],
                   [{'type': 'histogram'}, {'type': 'scatterpolar'}]]
        )
        
        # 1. Bar chart of rankings
        fig.add_trace(
            go.Bar(x=models, y=r2_scores, marker_color=colors, name='R² Score'),
            row=1, col=1
        )
        
        # 2. Pie chart of model types
        type_counts = pd.Series(types).value_counts()
        fig.add_trace(
            go.Pie(labels=type_counts.index, values=type_counts.values, name='Model Types'),
            row=1, col=2
        )
        
        # 3. Histogram of R² scores
        fig.add_trace(
            go.Histogram(x=r2_scores, nbinsx=10, marker_color='lightblue', name='R² Distribution'),
            row=2, col=1
        )
        
        # 4. Polar/Spiral visualization (Vortex effect)
        theta = list(range(len(models)))
        fig.add_trace(
            go.Scatterpolar(
                r=r2_scores,
                theta=theta,
                mode='markers+lines',
                marker=dict(size=12, color=r2_scores, colorscale='Viridis', showscale=True),
                line=dict(color='darkblue'),
                name='Vortex Pattern'
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text="🌀 Mind Vortex: Multi-Model Evaluation",
            showlegend=False,
            height=800,
            width=1200
        )
        
        fig.update_xaxes(tickangle=-45, row=1, col=1)
        
        return fig
    
    @staticmethod
    def create_contribution_dashboard(contribution_summary):
        """Create comprehensive contribution visualization dashboard"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Top Correlations', 'Model Performance', 
                          'Feature Importance', 'Predictive Power Gains'),
            specs=[[{'type': 'bar'}, {'type': 'bar'}],
                   [{'type': 'bar'}, {'type': 'scatter'}]]
        )
        
        # 1. Top correlations
        corr_insights = contribution_summary.get('correlation_insights', [])[:5]
        if corr_insights:
            corr_labels = [f"{c['feature1']} vs {c['feature2']}" for c in corr_insights]
            corr_values = [c['correlation'] for c in corr_insights]
            fig.add_trace(
                go.Bar(x=corr_labels, y=corr_values, marker_color='lightcoral', name='Correlation'),
                row=1, col=1
            )
        
        # 2. Model performance
        model_perf = contribution_summary.get('model_performance', [])
        if model_perf:
            models = [m['model'] for m in model_perf]
            r2s = [m['r2_score'] for m in model_perf]
            fig.add_trace(
                go.Bar(x=models, y=r2s, marker_color='lightblue', name='R² Score'),
                row=1, col=2
            )
        
        # 3. Feature importance
        feat_imp = contribution_summary.get('feature_importance_aggregate', {})
        if feat_imp:
            top_features = list(feat_imp.keys())[:10]
            top_importances = [feat_imp[f] for f in top_features]
            fig.add_trace(
                go.Bar(x=top_features, y=top_importances, marker_color='lightgreen', name='Importance'),
                row=2, col=1
            )
        
        # 4. Predictive power gains
        pp_gains = contribution_summary.get('predictive_power_gains', [])
        if pp_gains:
            pp_models = [p['model'] for p in pp_gains]
            pp_values = [p['predictive_power'] for p in pp_gains]
            fig.add_trace(
                go.Scatter(x=pp_models, y=pp_values, mode='lines+markers', 
                          marker=dict(size=10, color=pp_values, colorscale='Viridis'),
                          line=dict(width=2), name='Predictive Power'),
                row=2, col=2
            )
        
        fig.update_layout(
            title_text="📊 Comprehensive Contribution Analysis",
            showlegend=False,
            height=800,
            width=1200
        )
        
        fig.update_xaxes(tickangle=-45, row=1, col=1)
        fig.update_xaxes(tickangle=-45, row=1, col=2)
        fig.update_xaxes(tickangle=-45, row=2, col=1)
        fig.update_xaxes(tickangle=-45, row=2, col=2)
        
        return fig
    
    @staticmethod
    def create_dynamic_impact_visualization(dynamic_impact_data):
        """Create dynamic predictive power impact visualization"""
        feature_impacts = dynamic_impact_data.get('feature_impacts', {})
        
        if not feature_impacts:
            return None
        
        # Prepare data
        features = list(feature_impacts.keys())[:10]  # Top 10
        absolute_impacts = [feature_impacts[f]['absolute_impact'] for f in features]
        percentage_impacts = [feature_impacts[f]['percentage_impact'] for f in features]
        power_contributions = [feature_impacts[f]['predictive_power_contribution'] for f in features]
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Absolute Impact on R² Score', 
                'Percentage Impact (%)', 
                'Predictive Power Contribution',
                'Impact Power Flow'
            ),
            specs=[
                [{'type': 'bar'}, {'type': 'bar'}],
                [{'type': 'bar'}, {'type': 'scatter'}]
            ]
        )
        
        # 1. Absolute Impact
        fig.add_trace(
            go.Bar(
                x=features, 
                y=absolute_impacts,
                marker=dict(
                    color=absolute_impacts,
                    colorscale='RdYlGn',
                    showscale=True,
                    colorbar=dict(title="Impact", x=0.46)
                ),
                name='Absolute Impact'
            ),
            row=1, col=1
        )
        
        # 2. Percentage Impact
        fig.add_trace(
            go.Bar(
                x=features,
                y=percentage_impacts,
                marker=dict(
                    color=percentage_impacts,
                    colorscale='Viridis',
                    showscale=False
                ),
                name='% Impact'
            ),
            row=1, col=2
        )
        
        # 3. Power Contribution
        fig.add_trace(
            go.Bar(
                x=features,
                y=power_contributions,
                marker=dict(
                    color=power_contributions,
                    colorscale='Plasma',
                    showscale=False
                ),
                name='Power Contribution'
            ),
            row=2, col=1
        )
        
        # 4. Impact Flow (Sunburst/Cascade effect)
        cumulative_impact = []
        cumsum = 0
        for impact in absolute_impacts:
            cumsum += impact
            cumulative_impact.append(cumsum)
        
        fig.add_trace(
            go.Scatter(
                x=features,
                y=cumulative_impact,
                mode='lines+markers',
                marker=dict(
                    size=12,
                    color=cumulative_impact,
                    colorscale='Turbo',
                    showscale=False,
                    line=dict(width=2, color='white')
                ),
                line=dict(width=3, color='darkblue'),
                name='Cumulative Impact',
                fill='tozeroy',
                fillcolor='rgba(0,100,200,0.2)'
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text="⚡ Dynamic Predictive Power Impact Analysis",
            showlegend=False,
            height=800,
            width=1200
        )
        
        fig.update_xaxes(tickangle=-45, row=1, col=1)
        fig.update_xaxes(tickangle=-45, row=1, col=2)
        fig.update_xaxes(tickangle=-45, row=2, col=1)
        fig.update_xaxes(tickangle=-45, row=2, col=2)
        
        return fig
    
    @staticmethod
    def create_metrics_comparison_table(vortex_results):
        """Create detailed metrics comparison table"""
        ranking = vortex_results.get('predictive_power_ranking', [])
        
        if not ranking:
            return None
        
        models = [r['model'] for r in ranking]
        types = [r['type'] for r in ranking]
        r2_scores = [f"{r['r2_score']:.4f}" for r in ranking]
        pp = [f"{r['predictive_power']:.2f}%" for r in ranking]
        power_gains = [f"{r.get('power_gain', 0):.2f}%" for r in ranking]
        
        fig = go.Figure(data=[go.Table(
            header=dict(
                values=['Rank', 'Model', 'Type', 'R² Score', 'Predictive Power', 'Power Gain'],
                fill_color='paleturquoise',
                align='left',
                font=dict(size=12, color='black')
            ),
            cells=dict(
                values=[
                    list(range(1, len(models) + 1)),
                    models,
                    types,
                    r2_scores,
                    pp,
                    power_gains
                ],
                fill_color='lavender',
                align='left',
                font=dict(size=11)
            )
        )])
        
        fig.update_layout(
            title='Model Performance Metrics Comparison',
            height=400
        )
        
        return fig
