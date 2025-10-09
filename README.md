# ⚽ Football Sports Analytics - Advanced Correlation Engine

Advanced autonomous sports analytics platform with Mind Vortex multi-model evaluation technology, focused on football/soccer data analysis.

## 🌟 Features

### Advanced Analytics Techniques

1. **Pearson Correlation Analysis** 
   - Identify linear relationships between variables
   - Correlation matrix visualization
   - Top correlation pairs identification

2. **Multiple Regression Models**
   - Linear Regression
   - Ridge Regression
   - Lasso Regression
   - Random Forest Regressor
   - Gradient Boosting Regressor
   - Cross-validation with configurable folds
   - AIC (Akaike Information Criterion) calculation

3. **Decision Trees & Logistic Regression**
   - Decision tree regression/classification
   - Logistic regression for binary outcomes
   - Feature importance ranking

4. **Time Series Analysis**
   - ARIMA-based forecasting
   - Trend analysis
   - Future predictions

5. **Deep Learning Correlation**
   - Neural network-based predictions
   - LSTM-style architecture
   - Training history visualization

6. **🌀 Mind Vortex Evaluation**
   - Comprehensive multi-model comparison
   - Automatic best model selection
   - Predictive power ranking
   - Cross-validation metrics (R², Accuracy, AIC, Loss)
   - **⚡ Dynamic Predictive Power Impact Analysis** (NEW)
   - Smart autonomous feature relationship detection
   - Real-time impact power calculation

### Key Capabilities

- 🤖 **Autonomous Operation**: Minimal user input required - upload data and go!
- 📊 **Interactive Visualizations**: Explore results with Plotly charts
- 🔍 **Cross-Validation**: Robust model evaluation with configurable folds
- 📈 **Predictive Power Analysis**: Compare model effectiveness
- 💡 **Feature Importance**: Understand key performance drivers
- 🎯 **Multi-Model Comparison**: R², Accuracy, AIC, Loss metrics
- ⚡ **Dynamic Impact Analysis**: Real-time calculation of feature contribution to predictive power
- 🔄 **Smart Relationship Technology**: Autonomous detection of impactful feature relationships
- 📥 **Export Results**: Download analysis results as JSON

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📊 Usage

### 1. Upload Data

Upload a JSON file with your football statistics data. The format should be:

```json
[
    {
        "team": "Team A",
        "goals_scored": 95,
        "possession_pct": 64.2,
        "passes_completed": 612,
        "points": 89,
        "wins": 28
    },
    ...
]
```

### 2. Configure Analysis

- Select your **target variable** (e.g., "points" or "wins")
- Optionally select specific **feature variables**
- Choose **cross-validation folds** (3-10)
- Select which **analysis techniques** to run

### 3. Run Analysis

Click "🚀 Start Autonomous Analysis" and the system will:
- Automatically process your data
- Apply selected correlation techniques
- Generate comprehensive visualizations
- Rank model performance
- Identify best predictive model

### 4. Explore Results

Navigate through the tabs:

- **🌀 Mind Vortex**: Multi-model evaluation dashboard
- **📈 Correlations**: Correlation analysis and heatmaps
- **🤖 Model Performance**: Detailed model metrics
- **📊 Visualizations**: Interactive charts and graphs
- **📋 Detailed Results**: Raw JSON results

## 📁 Project Structure

```
semantic-document-analyzer/
├── app.py                          # Main Streamlit application
├── core/
│   ├── __init__.py
│   ├── sports_analytics.py         # Core analytics engine
│   ├── visualizations.py           # Visualization utilities
│   └── knowledge_base.py           # Original knowledge base
├── sample_football_data.json       # Sample dataset
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🧠 Mind Vortex Technology

The Mind Vortex is a unique multi-model evaluation system that:

1. **Tests Multiple Variations**: Automatically runs various model configurations
2. **Compares Performance**: Uses cross-validation and multiple metrics
3. **Ranks Models**: Orders models by predictive power
4. **Visualizes Patterns**: Creates spiral/vortex visualizations showing model relationships
5. **Selects Best Model**: Automatically identifies the highest-performing approach
6. **⚡ Dynamic Impact Analysis** (NEW): Calculates real-time predictive power contribution for each feature

### Evaluation Metrics

- **R² Score**: Coefficient of determination (regression quality)
- **Cross-Validation Mean**: Average performance across folds
- **AIC**: Akaike Information Criterion (model complexity vs fit)
- **RMSE**: Root Mean Squared Error
- **Accuracy**: Classification accuracy (for binary targets)
- **Loss**: Neural network training/validation loss
- **⚡ Predictive Power Impact** (NEW): Feature contribution to prediction accuracy
- **🔄 Power Gain**: Relative improvement over baseline models

### Dynamic Predictive Power Impact Analysis

The new Dynamic Impact Analysis feature provides:

- **Absolute Impact**: Direct R² contribution of each feature
- **Percentage Impact**: Relative importance as percentage of total predictive power
- **Power Contribution**: Weighted contribution score combining correlation and predictive strength
- **Impact Flow Visualization**: Cumulative impact cascade showing how features build predictive power
- **Smart Relationship Detection**: Autonomous identification of most impactful feature combinations

## 🎯 Use Cases

### Football Analytics
- Predict match outcomes
- Analyze team performance factors
- Identify key performance indicators
- Forecast future performance

### General Sports Analytics
- Player performance analysis
- Team strategy optimization
- Injury prediction
- Fan engagement metrics

### Business Intelligence
- Sales forecasting
- Customer behavior analysis
- Market trend prediction
- Risk assessment

## 📈 Example Analysis Workflow

1. **Upload** Premier League season data
2. **Select** "points" as target variable
3. **Run** all analysis techniques
4. **Review** Mind Vortex to see that Gradient Boosting achieves R²=0.95
5. **Explore** feature importance to find possession_pct and goals_scored are key
6. **Download** results for reporting

## 🔧 Advanced Configuration

### Custom Model Parameters

Edit `core/sports_analytics.py` to customize:
- Regression model hyperparameters
- Neural network architecture
- Time series model orders
- Cross-validation strategies

### Visualization Themes

Edit `core/visualizations.py` to customize:
- Color schemes
- Chart types
- Layout preferences

## 📚 Dependencies

- **streamlit**: Web interface
- **pandas**: Data manipulation
- **numpy**: Numerical computing
- **scikit-learn**: Machine learning models
- **tensorflow**: Deep learning
- **plotly**: Interactive visualizations
- **statsmodels**: Time series analysis
- **xgboost**: Gradient boosting (optional)

## 🤝 Contributing

Feel free to enhance this project with:
- Additional correlation techniques
- More visualization options
- New model types
- Performance optimizations

## 📄 License

This project is open source and available for educational and commercial use.

## 🙏 Acknowledgments

Built with modern machine learning and data science tools to provide autonomous, intelligent analytics for sports data.

---

**Made with ⚽ for football analytics enthusiasts**
