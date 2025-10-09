import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score, KFold
from sklearn.linear_model import LinearRegression, Ridge, Lasso, LogisticRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_squared_error, accuracy_score, roc_auc_score
from sklearn.preprocessing import StandardScaler
from scipy.stats import pearsonr
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import warnings
warnings.filterwarnings('ignore')

class SportsAnalytics:
    """Football-focused sports analytics with advanced correlation techniques"""
    
    def __init__(self):
        self.data = None
        self.results = {}
        self.scaler = StandardScaler()
        
    def load_json_data(self, json_data):
        """Load and prepare JSON data for analysis"""
        if isinstance(json_data, dict):
            self.data = pd.DataFrame(json_data)
        elif isinstance(json_data, list):
            self.data = pd.DataFrame(json_data)
        else:
            self.data = pd.read_json(json_data)
        return self.data
    
    def pearson_correlation_analysis(self, target_col=None):
        """Compute Pearson correlation for all numeric columns"""
        numeric_data = self.data.select_dtypes(include=[np.number])
        
        if numeric_data.empty:
            return {"error": "No numeric data found"}
        
        corr_matrix = numeric_data.corr(method='pearson')
        
        results = {
            'correlation_matrix': corr_matrix.to_dict(),
            'top_correlations': [],
            'target_correlations': {}
        }
        
        # Find top correlations
        corr_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                col1, col2 = corr_matrix.columns[i], corr_matrix.columns[j]
                corr_val = corr_matrix.iloc[i, j]
                corr_pairs.append({
                    'feature1': col1,
                    'feature2': col2,
                    'correlation': float(corr_val),
                    'abs_correlation': abs(float(corr_val))
                })
        
        corr_pairs.sort(key=lambda x: x['abs_correlation'], reverse=True)
        results['top_correlations'] = corr_pairs[:10]
        
        # Target-specific correlations
        if target_col and target_col in numeric_data.columns:
            target_corrs = corr_matrix[target_col].drop(target_col).to_dict()
            results['target_correlations'] = {
                k: float(v) for k, v in sorted(
                    target_corrs.items(), 
                    key=lambda x: abs(x[1]), 
                    reverse=True
                )
            }
        
        self.results['pearson_correlation'] = results
        return results
    
    def regression_models_analysis(self, target_col, feature_cols=None, cv_folds=5):
        """Apply multiple regression models with cross-validation"""
        if target_col not in self.data.columns:
            return {"error": f"Target column '{target_col}' not found"}
        
        numeric_data = self.data.select_dtypes(include=[np.number])
        
        if feature_cols is None:
            feature_cols = [col for col in numeric_data.columns if col != target_col]
        
        X = numeric_data[feature_cols].fillna(numeric_data[feature_cols].mean())
        y = numeric_data[target_col].fillna(numeric_data[target_col].mean())
        
        X_scaled = self.scaler.fit_transform(X)
        
        models = {
            'Linear Regression': LinearRegression(),
            'Ridge Regression': Ridge(alpha=1.0),
            'Lasso Regression': Lasso(alpha=1.0),
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42)
        }
        
        results = {}
        
        for name, model in models.items():
            # Cross-validation
            cv_scores = cross_val_score(model, X_scaled, y, cv=cv_folds, 
                                       scoring='r2')
            
            # Fit model
            model.fit(X_scaled, y)
            y_pred = model.predict(X_scaled)
            
            # Metrics
            r2 = r2_score(y, y_pred)
            mse = mean_squared_error(y, y_pred)
            rmse = np.sqrt(mse)
            
            # AIC approximation (for linear models)
            n = len(y)
            k = len(feature_cols) + 1
            aic = n * np.log(mse) + 2 * k if mse > 0 else float('inf')
            
            results[name] = {
                'r2_score': float(r2),
                'rmse': float(rmse),
                'mse': float(mse),
                'aic': float(aic),
                'cv_mean': float(cv_scores.mean()),
                'cv_std': float(cv_scores.std()),
                'predictive_power_increase': float((r2 - cv_scores.mean()) * 100)
            }
            
            # Feature importance for tree-based models
            if hasattr(model, 'feature_importances_'):
                importance = dict(zip(feature_cols, model.feature_importances_))
                results[name]['feature_importance'] = {
                    k: float(v) for k, v in sorted(
                        importance.items(), 
                        key=lambda x: x[1], 
                        reverse=True
                    )[:10]
                }
        
        self.results['regression_models'] = results
        return results
    
    def decision_tree_analysis(self, target_col, feature_cols=None, task='regression', cv_folds=5):
        """Decision tree and logistic regression analysis"""
        if target_col not in self.data.columns:
            return {"error": f"Target column '{target_col}' not found"}
        
        numeric_data = self.data.select_dtypes(include=[np.number])
        
        if feature_cols is None:
            feature_cols = [col for col in numeric_data.columns if col != target_col]
        
        X = numeric_data[feature_cols].fillna(numeric_data[feature_cols].mean())
        y = numeric_data[target_col].fillna(numeric_data[target_col].mean())
        
        X_scaled = self.scaler.fit_transform(X)
        
        results = {}
        
        if task == 'regression':
            dt_model = DecisionTreeRegressor(max_depth=10, random_state=42)
            dt_model.fit(X_scaled, y)
            y_pred = dt_model.predict(X_scaled)
            
            cv_scores = cross_val_score(dt_model, X_scaled, y, cv=cv_folds, scoring='r2')
            
            results['Decision Tree'] = {
                'r2_score': float(r2_score(y, y_pred)),
                'rmse': float(np.sqrt(mean_squared_error(y, y_pred))),
                'cv_mean': float(cv_scores.mean()),
                'cv_std': float(cv_scores.std()),
                'feature_importance': {
                    k: float(v) for k, v in sorted(
                        dict(zip(feature_cols, dt_model.feature_importances_)).items(),
                        key=lambda x: x[1],
                        reverse=True
                    )[:10]
                }
            }
        else:
            # For classification
            dt_model = DecisionTreeClassifier(max_depth=10, random_state=42)
            lr_model = LogisticRegression(max_iter=1000, random_state=42)
            
            # Binarize target for classification
            y_binary = (y > y.median()).astype(int)
            
            dt_model.fit(X_scaled, y_binary)
            lr_model.fit(X_scaled, y_binary)
            
            dt_pred = dt_model.predict(X_scaled)
            lr_pred = lr_model.predict(X_scaled)
            
            results['Decision Tree'] = {
                'accuracy': float(accuracy_score(y_binary, dt_pred)),
                'cv_mean': float(cross_val_score(dt_model, X_scaled, y_binary, cv=cv_folds).mean())
            }
            
            results['Logistic Regression'] = {
                'accuracy': float(accuracy_score(y_binary, lr_pred)),
                'cv_mean': float(cross_val_score(lr_model, X_scaled, y_binary, cv=cv_folds).mean())
            }
        
        self.results['decision_tree_analysis'] = results
        return results
    
    def time_series_analysis(self, target_col, date_col=None, order=(1,1,1)):
        """Time series analysis using ARIMA"""
        if target_col not in self.data.columns:
            return {"error": f"Target column '{target_col}' not found"}
        
        if date_col and date_col in self.data.columns:
            ts_data = self.data.set_index(date_col)[target_col]
        else:
            ts_data = self.data[target_col]
        
        ts_data = ts_data.fillna(method='ffill').fillna(method='bfill')
        
        try:
            # ARIMA model
            model = ARIMA(ts_data, order=order)
            fitted_model = model.fit()
            
            # Forecast
            forecast_steps = min(10, len(ts_data) // 5)
            forecast = fitted_model.forecast(steps=forecast_steps)
            
            results = {
                'aic': float(fitted_model.aic),
                'bic': float(fitted_model.bic),
                'order': order,
                'forecast': forecast.tolist() if hasattr(forecast, 'tolist') else list(forecast),
                'residuals_mean': float(fitted_model.resid.mean()),
                'residuals_std': float(fitted_model.resid.std())
            }
            
            self.results['time_series_analysis'] = results
            return results
        except Exception as e:
            return {"error": f"Time series analysis failed: {str(e)}"}
    
    def deep_learning_correlation(self, target_col, feature_cols=None, epochs=50):
        """Deep learning-based correlation using neural networks"""
        if target_col not in self.data.columns:
            return {"error": f"Target column '{target_col}' not found"}
        
        numeric_data = self.data.select_dtypes(include=[np.number])
        
        if feature_cols is None:
            feature_cols = [col for col in numeric_data.columns if col != target_col]
        
        X = numeric_data[feature_cols].fillna(numeric_data[feature_cols].mean())
        y = numeric_data[target_col].fillna(numeric_data[target_col].mean())
        
        X_scaled = self.scaler.fit_transform(X)
        y_scaled = (y - y.mean()) / y.std()
        
        # Build neural network
        model = keras.Sequential([
            layers.Dense(64, activation='relu', input_shape=(X_scaled.shape[1],)),
            layers.Dropout(0.3),
            layers.Dense(32, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(16, activation='relu'),
            layers.Dense(1)
        ])
        
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        
        # Train with validation split
        history = model.fit(
            X_scaled, y_scaled,
            epochs=epochs,
            batch_size=32,
            validation_split=0.2,
            verbose=0
        )
        
        # Predictions
        y_pred_scaled = model.predict(X_scaled, verbose=0)
        y_pred = y_pred_scaled.flatten() * y.std() + y.mean()
        
        # Metrics
        r2 = r2_score(y, y_pred)
        mse = mean_squared_error(y, y_pred)
        
        results = {
            'r2_score': float(r2),
            'rmse': float(np.sqrt(mse)),
            'final_loss': float(history.history['loss'][-1]),
            'final_val_loss': float(history.history['val_loss'][-1]),
            'training_history': {
                'loss': [float(x) for x in history.history['loss'][-10:]],
                'val_loss': [float(x) for x in history.history['val_loss'][-10:]]
            },
            'predictive_power_increase': float(r2 * 100)
        }
        
        self.results['deep_learning_correlation'] = results
        return results
    
    def mind_vortex_evaluation(self, target_col, feature_cols=None):
        """
        Mind Vortex: Evaluate multiple model variations and their contributions
        Creates a comprehensive comparison of all techniques with dynamic impact analysis
        """
        if target_col not in self.data.columns:
            return {"error": f"Target column '{target_col}' not found"}
        
        vortex_results = {
            'variations': [],
            'best_model': None,
            'comparative_metrics': {},
            'predictive_power_ranking': [],
            'dynamic_impact_metrics': {}
        }
        
        # Run all analysis techniques
        print("🌀 Activating Mind Vortex Analysis...")
        
        # 1. Pearson Correlation
        pearson_results = self.pearson_correlation_analysis(target_col)
        
        # 2. Regression Models
        regression_results = self.regression_models_analysis(target_col, feature_cols)
        
        # 3. Decision Trees
        dt_results = self.decision_tree_analysis(target_col, feature_cols, task='regression')
        
        # 4. Time Series (if applicable)
        try:
            ts_results = self.time_series_analysis(target_col)
        except:
            ts_results = {"error": "Time series not applicable"}
        
        # 5. Deep Learning
        dl_results = self.deep_learning_correlation(target_col, feature_cols, epochs=30)
        
        # 6. Dynamic Predictive Power Impact Analysis
        print("   🔄 Calculating dynamic predictive power impacts...")
        dynamic_impact = self.calculate_dynamic_predictive_power_impact(target_col, feature_cols)
        
        # Compile variations
        all_models = {}
        
        # From regression
        if 'regression_models' in self.results:
            for model_name, metrics in self.results['regression_models'].items():
                all_models[f"Regression-{model_name}"] = {
                    'type': 'regression',
                    'r2_score': metrics.get('r2_score', 0),
                    'cv_mean': metrics.get('cv_mean', 0),
                    'aic': metrics.get('aic', float('inf'))
                }
        
        # From decision trees
        if 'decision_tree_analysis' in self.results:
            for model_name, metrics in self.results['decision_tree_analysis'].items():
                all_models[f"TreeBased-{model_name}"] = {
                    'type': 'tree',
                    'r2_score': metrics.get('r2_score', metrics.get('accuracy', 0)),
                    'cv_mean': metrics.get('cv_mean', 0)
                }
        
        # From deep learning
        if 'deep_learning_correlation' in self.results:
            all_models['DeepLearning-Neural Network'] = {
                'type': 'deep_learning',
                'r2_score': self.results['deep_learning_correlation'].get('r2_score', 0),
                'loss': self.results['deep_learning_correlation'].get('final_val_loss', 0)
            }
        
        # Rank models by R2 score
        ranked_models = sorted(
            all_models.items(),
            key=lambda x: x[1].get('r2_score', 0),
            reverse=True
        )
        
        # Calculate predictive power gains
        vortex_results['predictive_power_ranking'] = [
            {
                'model': name,
                'type': metrics['type'],
                'r2_score': float(metrics.get('r2_score', 0)),
                'predictive_power': float(metrics.get('r2_score', 0) * 100),
                'power_gain': float((metrics.get('r2_score', 0) - (ranked_models[-1][1].get('r2_score', 0) if len(ranked_models) > 0 else 0)) * 100)
            }
            for name, metrics in ranked_models
        ]
        
        vortex_results['best_model'] = ranked_models[0] if ranked_models else None
        
        # Dynamic impact metrics
        if 'dynamic_predictive_power' in self.results:
            vortex_results['dynamic_impact_metrics'] = {
                'feature_impacts': self.results['dynamic_predictive_power'].get('feature_impacts', {}),
                'top_impact_features': self.results['dynamic_predictive_power'].get('top_impact_features', []),
                'baseline_predictive_power': float(self.results['dynamic_predictive_power'].get('baseline_r2', 0) * 100)
            }
        
        vortex_results['comparative_metrics'] = {
            'total_variations_tested': len(all_models),
            'best_r2_score': float(ranked_models[0][1].get('r2_score', 0)) if ranked_models else 0,
            'average_r2_score': float(np.mean([m[1].get('r2_score', 0) for m in ranked_models])) if ranked_models else 0,
            'worst_r2_score': float(ranked_models[-1][1].get('r2_score', 0)) if ranked_models else 0,
            'power_range': float((ranked_models[0][1].get('r2_score', 0) - ranked_models[-1][1].get('r2_score', 0)) * 100) if ranked_models else 0,
            'techniques_used': [
                'Pearson Correlation',
                'Multiple Regression Models',
                'Decision Trees',
                'Time Series Analysis',
                'Deep Learning Neural Networks',
                'Dynamic Predictive Power Analysis'
            ]
        }
        
        self.results['mind_vortex'] = vortex_results
        return vortex_results
    
    def get_all_results(self):
        """Get all analysis results"""
        return self.results
    
    def calculate_dynamic_predictive_power_impact(self, target_col, feature_cols=None):
        """
        Calculate dynamic predictive power impact for each feature
        Shows how much each feature contributes to prediction accuracy
        Uses incremental addition to measure contribution
        """
        if target_col not in self.data.columns:
            return {"error": f"Target column '{target_col}' not found"}
        
        numeric_data = self.data.select_dtypes(include=[np.number])
        
        if feature_cols is None:
            feature_cols = [col for col in numeric_data.columns if col != target_col]
        
        X = numeric_data[feature_cols].fillna(numeric_data[feature_cols].mean())
        y = numeric_data[target_col].fillna(numeric_data[target_col].mean())
        
        # Baseline model (using all features)
        baseline_model = LinearRegression()
        X_scaled = self.scaler.fit_transform(X)
        baseline_model.fit(X_scaled, y)
        baseline_r2 = r2_score(y, baseline_model.predict(X_scaled))
        
        # Calculate incremental impact of each feature
        feature_impacts = {}
        
        # Start with correlation-based importance as a baseline measure
        for i, feature in enumerate(feature_cols):
            # Single feature model
            X_single = numeric_data[[feature]].fillna(numeric_data[[feature]].mean())
            X_single_scaled = StandardScaler().fit_transform(X_single)
            
            single_model = LinearRegression()
            single_model.fit(X_single_scaled, y)
            single_r2 = r2_score(y, single_model.predict(X_single_scaled))
            
            # Calculate contribution to baseline
            # For perfect models, use correlation and importance
            corr = abs(numeric_data[feature].corr(y))
            
            # Weighted impact calculation
            if baseline_r2 > 0.99:  # Near-perfect model
                # Use correlation strength and variance explained
                impact = single_r2
                contribution = corr * single_r2 * 100
            else:
                # Remove feature and measure drop
                features_without = [f for f in feature_cols if f != feature]
                if features_without:
                    X_without = numeric_data[features_without].fillna(numeric_data[features_without].mean())
                    X_without_scaled = StandardScaler().fit_transform(X_without)
                    
                    model_without = LinearRegression()
                    model_without.fit(X_without_scaled, y)
                    r2_without = r2_score(y, model_without.predict(X_without_scaled))
                    
                    impact = baseline_r2 - r2_without
                    contribution = impact * 100
                else:
                    impact = baseline_r2
                    contribution = baseline_r2 * 100
            
            impact_percentage = (impact / baseline_r2 * 100) if baseline_r2 > 0 else 0
            
            feature_impacts[feature] = {
                'absolute_impact': float(impact),
                'percentage_impact': float(impact_percentage),
                'predictive_power_contribution': float(contribution),
                'r2_with_feature': float(baseline_r2),
                'r2_single_feature': float(single_r2),
                'correlation_strength': float(corr)
            }
        
        # Sort by predictive power contribution
        sorted_impacts = dict(sorted(
            feature_impacts.items(),
            key=lambda x: x[1]['predictive_power_contribution'],
            reverse=True
        ))
        
        results = {
            'feature_impacts': sorted_impacts,
            'baseline_r2': float(baseline_r2),
            'total_features': len(feature_cols),
            'top_impact_features': [
                {
                    'feature': k,
                    'impact': v['absolute_impact'],
                    'percentage': v['percentage_impact'],
                    'contribution': v['predictive_power_contribution'],
                    'single_r2': v['r2_single_feature']
                }
                for k, v in list(sorted_impacts.items())[:5]
            ]
        }
        
        self.results['dynamic_predictive_power'] = results
        return results
    
    def generate_contribution_summary(self):
        """Generate detailed contribution summary for visualization"""
        summary = {
            'correlation_insights': [],
            'model_performance': [],
            'feature_importance_aggregate': {},
            'predictive_power_gains': [],
            'dynamic_impact_analysis': {}
        }
        
        # Correlation insights
        if 'pearson_correlation' in self.results:
            top_corr = self.results['pearson_correlation'].get('top_correlations', [])[:5]
            summary['correlation_insights'] = top_corr
        
        # Model performance
        if 'regression_models' in self.results:
            for model_name, metrics in self.results['regression_models'].items():
                summary['model_performance'].append({
                    'model': model_name,
                    'r2_score': metrics.get('r2_score', 0),
                    'cv_performance': metrics.get('cv_mean', 0)
                })
        
        # Aggregate feature importance
        feature_imp_sources = []
        
        if 'regression_models' in self.results:
            for model_name, metrics in self.results['regression_models'].items():
                if 'feature_importance' in metrics:
                    feature_imp_sources.append(metrics['feature_importance'])
        
        if 'decision_tree_analysis' in self.results:
            for model_name, metrics in self.results['decision_tree_analysis'].items():
                if 'feature_importance' in metrics:
                    feature_imp_sources.append(metrics['feature_importance'])
        
        # Average feature importance
        all_features = set()
        for source in feature_imp_sources:
            all_features.update(source.keys())
        
        for feature in all_features:
            importances = [source.get(feature, 0) for source in feature_imp_sources]
            summary['feature_importance_aggregate'][feature] = float(np.mean(importances))
        
        # Sort by importance
        summary['feature_importance_aggregate'] = {
            k: v for k, v in sorted(
                summary['feature_importance_aggregate'].items(),
                key=lambda x: x[1],
                reverse=True
            )
        }
        
        # Predictive power gains
        if 'mind_vortex' in self.results:
            summary['predictive_power_gains'] = self.results['mind_vortex'].get('predictive_power_ranking', [])
        
        # Dynamic impact analysis
        if 'dynamic_predictive_power' in self.results:
            summary['dynamic_impact_analysis'] = self.results['dynamic_predictive_power'].get('top_impact_features', [])
        
        return summary
