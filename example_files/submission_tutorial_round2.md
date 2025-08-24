# ReXRank Submission Guideline

In this tutorial, we'll cover the process of submitting your model and results for official evaluation on ReXRank. Once your model has been evaluated, your scores will be added to the leaderboard.

##  Model Submission

Your model submission should include the following:

1. **Model Description:** This description identifies your submission on the leaderboard: {Name_of_model} (Institution) paper link, code link, year

2. **Conda Environment File:** Include the `environment.yaml` file support `conda install`.

3. **Inference Script:** The model should support the following command: ```python inference.py --input_json_file <input_json_file> --save_json_file <output_json_file> --img_root_dir <img_root_dir>```

   We provide example scripts for both tasks:
   - [Radiology Report Generation (RRG) Example](https://github.com/rajpurkarlab/ReXrank/blob/main/example_files/merversa_inference.py) using [MedVersa](https://huggingface.co/hyzhou/MedVersa/tree/main)
   - [Visual Question Answering (VQA) Example](https://github.com/rajpurkarlab/ReXrank/blob/main/example_files/medgamma_inference.py) using [MedGemma](https://huggingface.co/google/medgemma-4b-it)

   Your submission should clearly indicate which task(s) your model is designed for (RRG, VQA, or both).

Please send an email to Xiaoman Zhang xiaomanzhang.zxm@gmail.com with all the required information. Use the email title format: [ReXrank Submission] + Name_of_model. 

## Removing Your Models from the Leaderboard

If you decide you no longer want your model's score on the leaderboard, you can send an email to us. When the leaderboard updates, your model will no longer appear.

