# 🎯 Football Sports Analytics - Usage Guide

## Quick Start Guide

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/different35/semantic-document-analyzer.git
cd semantic-document-analyzer

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Demo

Test the system with sample football data:

```bash
python demo.py
```

This will:
- Load sample Premier League statistics
- Run all analysis techniques
- Display results in the terminal
- Save detailed results to JSON files

### 3. Launch the Interactive UI

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

## Using the Interface

### Step 1: Upload Data

1. Click **"Browse files"** in the sidebar
2. Select one or more JSON files with football/sports data
3. Preview your data to verify it loaded correctly

**Multiple File Support:**
- You can upload multiple JSON files at once
- All files will be automatically combined into a single dataset
- Files can have the same or different structures (common fields will be aligned)

**Required Format:**
- JSON array of objects or dictionary with arrays
- Must contain numeric columns for analysis
- At least one target variable to predict

### Step 2: Configure Analysis

1. **Select Target Variable**: The metric you want to predict (e.g., "points", "wins", "goals")
2. **Select Features** (optional): Specific variables to use as predictors
3. **Set CV Folds**: Number of cross-validation folds (3-10)
4. **Choose Techniques**: Select which analysis methods to run

### Step 3: Run Analysis

Click **"🚀 Start Autonomous Analysis"**

The system will:
- Automatically process your data
- Apply selected correlation techniques
- Train multiple models
- Evaluate with cross-validation
- Generate comprehensive visualizations

### Step 4: Explore Results

Navigate through 5 result tabs:

#### 🌀 Mind Vortex Tab
- Multi-model performance dashboard
- Spiral visualization showing model relationships
- Best model identification
- Comparative metrics table

#### 📈 Correlations Tab
- Interactive correlation heatmap
- Top correlation pairs
- Target-specific correlations

#### 🤖 Model Performance Tab
- Side-by-side model comparison
- Detailed metrics for each model
- Feature importance charts

#### 📊 Visualizations Tab
- Comprehensive contribution dashboard
- Time series forecasts (if applicable)
- Deep learning training history

#### 📋 Detailed Results Tab
- Raw JSON output
- Filterable by analysis type
- Downloadable results

### Step 5: Download Results

Use download buttons to export:
- **Full Results**: Complete analysis in JSON format
- **Contribution Summary**: Key insights and feature importance

## Analysis Techniques Explained

### 1. Pearson Correlation Analysis
**What it does:** Measures linear relationships between variables

**When to use:** 
- Identify which stats are related (e.g., possession vs passes)
- Find redundant features
- Understand data structure

**Output:**
- Correlation matrix heatmap
- Top correlation pairs
- Target variable correlations

### 2. Regression Models
**What it does:** Predicts continuous values using various algorithms

**Models included:**
- Linear Regression (baseline)
- Ridge Regression (handles multicollinearity)
- Lasso Regression (feature selection)
- Random Forest (non-linear patterns)
- Gradient Boosting (highest accuracy)

**Metrics:**
- R² Score: Prediction quality (0-1, higher is better)
- RMSE: Average prediction error
- AIC: Model complexity vs fit
- CV Mean: Cross-validation performance

### 3. Decision Trees & Logistic Regression
**What it does:** Classification and feature ranking

**When to use:**
- Binary outcomes (win/loss)
- Feature importance analysis
- Interpretable models

**Output:**
- Decision tree structure
- Feature importance ranking
- Classification accuracy

### 4. Time Series Analysis
**What it does:** Forecasts future values based on historical trends

**When to use:**
- Sequential data (season progression)
- Trend analysis
- Performance prediction

**Output:**
- ARIMA model parameters
- Future forecasts
- Model fit metrics (AIC, BIC)

### 5. Deep Learning Correlation
**What it does:** Neural network-based prediction

**When to use:**
- Complex non-linear patterns
- Large datasets
- Maximum prediction accuracy

**Architecture:**
- 4-layer neural network
- Dropout for regularization
- Optimized with Adam

**Output:**
- R² score
- Training/validation loss
- Learning curves

### 6. 🌀 Mind Vortex Evaluation
**What it does:** Comprehensive multi-model comparison system

**Process:**
1. Runs ALL selected techniques
2. Collects performance metrics
3. Ranks models by predictive power
4. Identifies best approach

**Unique Features:**
- Automatic model selection
- Cross-technique comparison
- Visualization of model relationships
- Aggregate feature importance

**Metrics Compared:**
- R² Score (regression quality)
- Cross-validation performance
- AIC (model efficiency)
- Accuracy (classification)

## Understanding Results

### R² Score Interpretation
- **0.9-1.0**: Excellent prediction
- **0.7-0.9**: Good prediction
- **0.5-0.7**: Moderate prediction
- **<0.5**: Poor prediction

### Feature Importance
- Shows which stats matter most
- Values sum to 1.0
- Higher = more important
- Use to focus data collection

### Model Selection Guide

**Use Linear Regression when:**
- Simple relationships
- Interpretability needed
- Baseline comparison

**Use Random Forest when:**
- Non-linear patterns
- Robust to outliers
- Feature importance needed

**Use Gradient Boosting when:**
- Maximum accuracy required
- Competition/production use
- Sufficient data available

**Use Neural Networks when:**
- Very large dataset
- Complex patterns
- GPU available

## Example Analyses

### Example 1: Predict Team Points
```
Target: points
Features: [goals_scored, possession_pct, passes_completed]
Result: Gradient Boosting R²=0.98
Key Feature: goals_scored (importance=0.65)
```

### Example 2: Win/Loss Prediction
```
Target: wins
Task: Classification
Result: Decision Tree Accuracy=0.89
Key Features: goals_scored, tackles
```

### Example 3: Player Performance
```
Target: player_rating
Features: [goals, assists, passes, tackles]
Result: Neural Network R²=0.94
Key Pattern: Non-linear relationship with assists
```

## Troubleshooting

### Issue: No numeric columns found
**Solution:** Ensure JSON contains numeric values, not strings

### Issue: Perfect R²=1.0 scores
**Cause:** Small dataset or data leakage
**Solution:** Use more data, check for duplicate columns

### Issue: Time series fails
**Cause:** Not enough sequential data
**Solution:** Disable time series or add more data points

### Issue: Deep learning takes too long
**Solution:** Reduce epochs (30-50) or use smaller dataset for testing

## Best Practices

1. **Data Quality**
   - Clean data before upload
   - Remove missing values or let system handle them
   - Ensure consistent units

2. **Feature Selection**
   - Start with all features
   - Use correlation to remove redundant ones
   - Focus on top important features

3. **Model Selection**
   - Always run Mind Vortex for best results
   - Compare multiple models
   - Consider interpretability vs accuracy

4. **Validation**
   - Use 5-fold CV for reliable results
   - Check cross-validation scores
   - Beware of overfitting (training >> validation)

5. **Interpretation**
   - Don't just look at R² scores
   - Examine feature importance
   - Validate predictions make sense

## Advanced Usage

### Custom Data Preprocessing

Edit `core/sports_analytics.py` to add:
- Custom feature engineering
- Data normalization strategies
- Outlier handling

### Custom Visualizations

Edit `core/visualizations.py` to:
- Change color schemes
- Add new chart types
- Modify layouts

### Model Hyperparameters

Modify in `sports_analytics.py`:
```python
# Random Forest
RandomForestRegressor(n_estimators=200, max_depth=15)

# Neural Network
epochs=100  # More training
layers.Dense(128)  # Bigger network
```

## Support

For issues or questions:
1. Check this guide
2. Review sample_football_data.json format
3. Run demo.py to verify installation
4. Check console for error messages

---

**Happy Analyzing! ⚽📊**
