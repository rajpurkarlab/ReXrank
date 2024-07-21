
from utils import *
from torch import cuda
import os
import csv
import json 
from tqdm import tqdm 
import pandas as pd 


import argparse
parser = argparse.ArgumentParser(description='get_entities')
parser.add_argument('--input_json_file', type=str,default='../../data/mimic-cxr/test_data.json')
parser.add_argument('--save_json_file', type=str,default='../../results/mimic-cxr/MedVersa.json')
parser.add_argument('--img_root_dir', type=str,default='../../data/mimic-cxr/MIMIC-CXR-JPG/files')
# 解析参数
args = parser.parse_args()
    
# ---  Launch Model ---
device = 'cuda' if cuda.is_available() else 'cpu'
model_cls = registry.get_model_class('medomni') # medomni is the architecture name :)
model = model_cls.from_pretrained('../../model/MedVersa').to(device).eval()
print('Load model success')

# --- Define hyperparams ---
num_beams = 1
do_sample = True
min_length = 1
top_p = 0.9
repetition_penalty = 1
length_penalty = 1
temperature = 0.1


# Load the dataset
input_json_file = args.input_json_file
img_root_dir =  args.img_root_dir
save_json_file = args.save_json_file

with open(input_json_file, 'r') as file:
    input_data_dict = json.load(file)

if os.path.exists(save_json_file):
    with open(save_json_file, 'r') as file:
        save_data_dict = json.load(file)
else:
    save_data_dict = {}
for study_id in tqdm(input_data_dict.keys()):
    if study_id in save_data_dict:
        pass 
    else:
        data_dict_idx = input_data_dict[study_id]
        save_data_dict_idx = data_dict_idx
        image_path_list = data_dict_idx['image_path']
        img_path_list_idx = [img_root_dir+image_path for image_path in image_path_list]
        input_clinical = data_dict_idx['context'] 
        # "<context>Age:60-70.Gender:F.Indication: ___-year-old female with pulmonary fibrosis and CHF with worsening shortness of breath.</context>",
        input_image_token = ''.join(f'<img{str(i)}>' for i in range(len(img_path_list_idx)))
        demo_ex = [
            img_path_list_idx,
            input_clinical,
            f"Can you provide a report of {input_image_token} with findings and impression?",
            "cxr",
            "report generation",
        ]
        print(input_clinical,f"Can you provide a report of {input_image_token} with findings and impression?")
        images, context, prompt, modality, task = demo_ex[0], demo_ex[1], demo_ex[2], demo_ex[3], demo_ex[4]
        seg_mask_2d, seg_mask_3d, output_text = generate_predictions(model, images, context, prompt, modality, task, num_beams, do_sample, min_length, top_p, repetition_penalty, length_penalty, temperature, device)
        save_data_dict_idx['model_prediction'] = output_text
        save_data_dict[study_id] = save_data_dict_idx
    with open(save_json_file, 'w') as file:
        json.dump(save_data_dict, file, indent=4)

    