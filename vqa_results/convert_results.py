# Rank,Date,Model Name,Institution,Model URL,Overall Accuracy,Differential Diagnosis,Geometric Information Assessment,Location and Distribution Assessment,Negation Assessment,Presence Assessment
# Sort by Overall Accuracy

import os 
import pandas as pd
import numpy as np


model_dict = {
    "Gemini": {
        "Model Name": "Gemini-1.5-Pro",
        "Date": "2024-09-24",
        "Institution": "Google",
        "Model URL": "https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/1-5-pro",
    },
    "Eagle2": {
        "Model Name": "Eagle2-9B",
        "Date": "2025-01-20",
        "Institution": "NVIDIA",
        "Model URL": "https://huggingface.co/nvidia/Eagle2-9B",
    },
    "Janus-Pro-7B": {
        "Model Name": "Janus-Pro-7B",
        "Date": "2025-02-18",
        "Institution": "DeepSeek",
        "Model URL": "https://huggingface.co/deepseek-ai/Janus-Pro-7B",
    },
    "LLaVA": {
        "Model Name": "LLaVA-1.5-7B",
        "Date": "2024-01-03",
        "Institution": "Meta",
        "Model URL": "https://huggingface.co/llava-hf/llava-1.5-7b-hf",
    },
    "Qwen2VL": {
        "Model Name": "Qwen2VL-7B-Instruct",
        "Date": "2024-09-19",
        "Institution": "Alibaba",
        "Model URL": "https://huggingface.co/Qwen/Qwen2VL-7B-Instruct",
    },
    "Qwen25VL": {
        "Model Name": "Qwen2.5VL-7B-Instruct",
        "Date": "2025-04-28",
        "Institution": "Alibaba",
        "Model URL": "https://huggingface.co/Qwen/Qwen2.5VL-7B-Instruct",
    },
    "Phi35_Vision_Instruct": {
        "Model Name": "Phi35-Vision-Instruct",
        "Date": "2024-08-20",
        "Institution": "Microsoft",
        "Model URL": "https://huggingface.co/microsoft/Phi-3.5-vision-instruct",
    },
    "MedGemma": {
        "Model Name": "MedGemma-4B-it",
        "Date": "2025-05-20",
        "Institution": "Google",
        "Model URL": "https://huggingface.co/google/medgemma-4b-it",
    },
}


results_df = pd.read_csv("./model_comparison.csv")


for model_name, model_info in model_dict.items():
    # results_df.loc[results_df["Model"] == model_name, "Date"] = model_info["Date"]
    results_df.loc[results_df["Model"] == model_name, "Model Name"] = model_info["Model Name"]
    results_df.loc[results_df["Model"] == model_name, "Institution"] = model_info["Institution"]
    results_df.loc[results_df["Model"] == model_name, "Model URL"] = model_info["Model URL"]

results_df = results_df.sort_values(by="Overall Accuracy", ascending=False)
# save results with new column names and order following the order of the model_dict
results_df["Rank"] = np.arange(1, len(results_df) + 1)
results_df = results_df[["Rank",  "Model Name", "Institution", "Model URL", "Overall Accuracy", "Differential Diagnosis", "Geometric Information Assessment", "Location and Distribution Assessment", "Negation Assessment", "Presence Assessment"]]
results_df = results_df.sort_values(by="Overall Accuracy", ascending=False)
# index -> Rank column

results_df.to_csv("./vqa_results.csv", index=False)


# Rank,Date,Model Name,Institution,Model URL,Overall Accuracy,Differential Diagnosis,Geometric Information Assessment,Location and Distribution Assessment,Negation Assessment,Presence Assessment
# Sort by Overall Accuracy