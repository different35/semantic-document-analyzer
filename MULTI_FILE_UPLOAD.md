# Multi-File JSON Upload - Sample Data

This directory contains sample JSON files that demonstrate the multi-file upload capability.

## Sample Files

### sample_data_set1.json
Contains La Liga teams (Real Madrid, Barcelona) with their statistics.

### sample_data_set2.json
Contains additional La Liga teams (Atletico Madrid, Sevilla) with their statistics.

### sample_football_data.json
Contains Premier League teams with comprehensive statistics.

## How to Use Multi-File Upload

1. **Single File**: Upload just one JSON file for analysis
2. **Multiple Files**: Select multiple JSON files (Ctrl+Click or Cmd+Click) to combine datasets

### Example: Combining La Liga datasets

Upload both `sample_data_set1.json` and `sample_data_set2.json` to analyze all 4 teams together:

```bash
# The system will automatically:
# 1. Load sample_data_set1.json (2 teams)
# 2. Load sample_data_set2.json (2 teams)  
# 3. Combine into single dataset (4 teams total)
# 4. Run analysis on the combined data
```

## Benefits

- ✅ **Combine datasets** from different sources
- ✅ **Scale analysis** across multiple data files
- ✅ **Organize data** by leagues, seasons, or categories
- ✅ **Maintain compatibility** with single-file uploads

## Data Format

All JSON files should follow the same structure:

```json
[
    {
        "team": "Team Name",
        "goals_scored": 85,
        "goals_conceded": 35,
        "shots_per_game": 18.2,
        "possession_pct": 62.5,
        ...
    }
]
```

Files with matching column names will be combined seamlessly!
