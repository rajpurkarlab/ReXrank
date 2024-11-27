# Evaluation Script for ReXRank Predictions

## Overview
This script converts a prediction JSON file into ground truth and prediction CSV files. These CSV files can be used for further evaluation using the scoring metrics from the [CXR-Report-Metric](https://github.com/rajpurkarlab/CXR-Report-Metric) repository. For the GREEN, we follow the [GREEN](https://github.com/Stanford-AIMI/GREEN) repository. For the RaTEScore, we follow the [RaTEScore](https://github.com/MAGIC-AI4Med/RaTEScore) repository. For the FineRadScore, we follow [FineRadScore](https://github.com/rajpurkarlab/FineRadScore) repository.
## Script

```python
import os
import json
import pandas as pd

def split_json(input_json_file, GT_REPORTS, PREDICTED_REPORTS):
    """
    Converts a JSON file of predictions into ground truth and prediction CSV files.
    
    Parameters:
    - input_json_file: str, path to the input JSON file
    - GT_REPORTS: str, path to the output ground truth CSV file
    - PREDICTED_REPORTS: str, path to the output prediction CSV file
    """
    with open(input_json_file, 'r') as file:
        input_data_dict = json.load(file)

    gt_reports = []
    predicted_reports = []

    for study_id, input_data_idx in input_data_dict.items():
        model_prediction = input_data_idx['model_prediction']
        findings = input_data_idx['section_findings']
        impression = input_data_idx['section_impression']

        # Handle NaN values
        findings = findings if pd.notna(findings) else None
        impression = impression if pd.notna(impression) else None

        groundtruth = f"Findings: {findings} Impression: {impression}"
        predicted_reports.append([study_id, model_prediction])
        gt_reports.append([study_id, groundtruth])

    # Convert to DataFrame
    predicted_reports_df = pd.DataFrame(predicted_reports, columns=['study_id', 'report'])
    gt_reports_df = pd.DataFrame(gt_reports, columns=['study_id', 'report'])

    # Save to CSV files
    predicted_reports_df.to_csv(PREDICTED_REPORTS, index=False)
    gt_reports_df.to_csv(GT_REPORTS, index=False)
    
    # Check for NaN values in 'report' column of gt_reports_df
    if gt_reports_df['report'].isnull().values.any():
        print("WARNING: There are NaN values in 'report' column of gt_reports_df.")

    # Check for NaN values in 'report' column of predicted_reports_df
    if predicted_reports_df['report'].isnull().values.any():
        print("WARNING: There are NaN values in 'report' column of predicted_reports_df.")
