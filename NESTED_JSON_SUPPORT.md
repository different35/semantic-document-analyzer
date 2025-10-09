# 🧠 Intelligent Nested JSON Support

## Overview

The system now intelligently handles complex nested JSON structures commonly found in sports APIs, eliminating the need for manual data preprocessing.

## What's New?

### ✅ Automatic Data Extraction

The system automatically:
- Detects nested API response structures
- Extracts data from `doc` → `data` hierarchies
- Flattens deeply nested dictionaries
- Identifies and expands entity collections
- Combines multiple files with different structures

### ✅ Supported Patterns

#### Pattern 1: Simple Array
```json
[
  {"team": "Liverpool", "goals": 36},
  {"team": "Arsenal", "goals": 28}
]
```
**Result**: 2 rows

#### Pattern 2: API Response (Single Entity)
```json
{
  "queryUrl": "stats_team_streaks/38",
  "doc": [{
    "event": "stats_team_streaks",
    "data": {
      "team": {"name": "Chelsea"},
      "streaks": {"wins": 5}
    }
  }]
}
```
**Result**: 1 row with flattened columns (`team_name`, `streaks_wins`)

#### Pattern 3: API Response (Multiple Entities)
```json
{
  "queryUrl": "stats_season_overunder/118689",
  "doc": [{
    "data": {
      "stats": {
        "35": {"team": {"name": "Man Utd"}, "matches": 38},
        "43": {"team": {"name": "Fulham"}, "matches": 38},
        ...
      }
    }
  }]
}
```
**Result**: 20 rows (one per team) with flattened columns

#### Pattern 4: Multiple Files
```json
// File 1
{"queryUrl": "...", "doc": [{"data": {...}}]}

// File 2
{"queryUrl": "...", "doc": [{"data": {...}}]}
```
**Result**: Combined rows from all files

## How It Works

### 1. Upload Files
- Select one or more JSON files
- No preprocessing needed
- System detects structure automatically

### 2. Automatic Extraction
```
JSON File → Detection → Extraction → Flattening → DataFrame
```

### 3. Data Preview
```
✅ Data loaded successfully from 3 files!

📊 Dataset Information
   - Rows: 43
   - Total Columns: 581
   - Numeric Columns: 447
   - Text Columns: 134
```

## Examples

### Example 1: Real Sports API Data

**Input**: `stats_season_overunder.json`
```json
{
  "queryUrl": "stats_season_overunder/118689",
  "doc": [{
    "data": {
      "season": {...},
      "stats": {
        "35": {
          "team": {"name": "Man Utd"},
          "matches": 38,
          "total": {
            "ft": {
              "1": {"over": 24, "under": 14},
              "2": {"over": 26, "under": 12}
            }
          }
        },
        "43": {...},
        ...
      }
    }
  }]
}
```

**Output DataFrame**:
```
   team_name  matches  total_ft_1_over  total_ft_1_under  ...
0    Man Utd       38               24                14  ...
1     Fulham       38               29                 9  ...
2    Ipswich       38               31                 7  ...
...
```

### Example 2: Multiple API Files

**Load 3 different stat files**:
```python
# Upload these files in the UI:
- stats_team_streaks.json       (1 team)
- stats_season_overunder.json   (20 teams)
- stats_season_topgoals.json    (20 teams)
```

**Result**: 43 rows combined with all statistics

## Supported File Types

### ✅ Supported
- Nested API responses (`doc` → `data`)
- Entity collections (multiple teams/players)
- Mixed file structures
- Deep nesting (5+ levels)
- Numeric and text data

### ⚠️ Limitations
- Files with only text data (no numeric fields) cannot be analyzed
- Very large files (>100MB) may be slow
- Circular references are not supported

## Error Handling

### Informative Messages

**No Numeric Data**:
```
❌ Data Loading Error

No numeric columns found in the data. The data contains only 
text/categorical fields. Available columns: match_name, team_abbr...

💡 Tips:
- Ensure your JSON files contain numeric data suitable for analysis
- The system supports nested JSON structures from sports APIs
- Files with only text/categorical data cannot be analyzed
```

**Invalid JSON**:
```
❌ Invalid JSON Format

The uploaded file is not valid JSON: Unexpected token at position 42
```

## Technical Details

### Extraction Algorithm

1. **Detect Structure**: Identify if JSON is API response or direct data
2. **Navigate Hierarchy**: Find `doc` → `data` path if present
3. **Identify Collections**: Look for dicts with numeric keys (entity IDs)
4. **Flatten**: Recursively flatten nested dicts into single-level
5. **Combine**: Concatenate multiple files into single DataFrame

### Flattening Rules

- Nested dicts: `{"team": {"name": "X"}}` → `{"team_name": "X"}`
- Metadata fields: Skip fields starting with `_` (except `_id`)
- Lists: Convert simple lists to strings, skip complex lists
- Separator: Use `_` to join nested keys

### Entity Detection

A dict is considered an entity collection if:
- Has > 5 items
- All keys are numeric (entity IDs)
- Values are dicts with > 3 fields

## Best Practices

### 1. File Organization
- Upload related files together
- Use consistent data sources
- Check data quality before upload

### 2. Data Structure
- Ensure numeric fields are numbers, not strings
- Use consistent field names across files
- Include team/player identifiers

### 3. Analysis
- Start with data preview to verify extraction
- Check numeric vs text column counts
- Select appropriate target variables

## FAQ

**Q: Why does my file show "No numeric columns found"?**
A: The file contains only text/categorical data. Ensure numeric stats are included.

**Q: Can I mix simple and nested JSON files?**
A: Yes! The system handles both formats automatically.

**Q: How many files can I upload at once?**
A: No hard limit, but 10-20 files is recommended for performance.

**Q: What if extraction is wrong?**
A: Check the data preview. You may need to preprocess the JSON manually.

**Q: Does this work with all sports APIs?**
A: It works with most common patterns. Unusual structures may need preprocessing.

## Testing Your Files

### Quick Test

1. Upload your JSON file
2. Check the success message
3. Review the data preview
4. Verify row and column counts

### Expected Results

| File Type | Expected Rows | Expected Columns |
|-----------|--------------|------------------|
| Single entity | 1 | 10-200 |
| Team stats (20 teams) | 20 | 50-300 |
| Player stats (30 players) | 30 | 20-100 |
| Multiple files (3) | Sum of all | Combined |

## Troubleshooting

### Issue: Empty DataFrame
- **Cause**: Data is nested too deep or in unexpected location
- **Solution**: Check if `data` field exists in JSON structure

### Issue: Only 1 Row from Multi-Team File
- **Cause**: Entity collection not detected
- **Solution**: Ensure team IDs are numeric strings

### Issue: Too Many Columns
- **Cause**: Very deep nesting creates many flattened fields
- **Solution**: This is normal, use feature selection in analysis

### Issue: Missing Data
- **Cause**: Some fields are lists/objects and get skipped
- **Solution**: Numeric fields are prioritized, complex fields are ignored

## Conclusion

The intelligent nested JSON support makes the system truly autonomous - just upload your API responses and start analyzing! No manual preprocessing, no data wrangling, no formatting required.

**From API → Analysis in seconds!** 🚀
