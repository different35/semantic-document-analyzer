#!/usr/bin/env python3
"""
Demo script showing multi-file JSON loading capability
"""

import json
import pandas as pd
import sys
sys.path.insert(0, '/home/runner/work/semantic-document-analyzer/semantic-document-analyzer')

def simulate_multi_file_upload():
    """Simulate uploading multiple JSON files like in the Streamlit app"""
    
    print("=" * 60)
    print("MULTI-FILE JSON UPLOAD DEMONSTRATION")
    print("=" * 60)
    print()
    
    # Simulate loading multiple files (like in app.py)
    uploaded_files = [
        'sample_data_set1.json',
        'sample_data_set2.json'
    ]
    
    print(f"📁 Loading {len(uploaded_files)} JSON files...")
    print()
    
    # Load all JSON files
    json_data = []
    for file_name in uploaded_files:
        with open(file_name, 'r') as f:
            file_data = json.load(f)
            json_data.append(file_data)
            print(f"  ✓ Loaded: {file_name} ({len(file_data)} records)")
    
    print()
    print(f"✅ Data loaded successfully from {len(uploaded_files)} files!")
    print()
    
    # Simulate the load_json_data logic
    print("Processing data...")
    
    # Multiple files, each containing a list of records
    dataframes = [pd.DataFrame(data) for data in json_data]
    combined_data = pd.concat(dataframes, ignore_index=True)
    
    print()
    print("=" * 60)
    print("COMBINED DATASET")
    print("=" * 60)
    print()
    print(f"Total rows: {len(combined_data)}")
    print(f"Total columns: {len(combined_data.columns)}")
    print()
    print("Data Preview:")
    print(combined_data.to_string(index=True))
    print()
    print("=" * 60)
    print("SUCCESS! All files combined into single dataset for analysis")
    print("=" * 60)

if __name__ == "__main__":
    simulate_multi_file_upload()
