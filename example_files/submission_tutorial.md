# ReXRank Submission Guideline

In this tutorial, we'll cover the process of submitting your model and results for official evaluation on ReXRank. Once your model has been evaluated, your scores will be added to the leaderboard.

## 1. Evaluating on the MIMIC-CXR Test Set

To achieve a consistent score with our leaderboard, please use the official MIMIC-CXR test split. You can download the file from [this link](URL). We evaluate at the study level. If the submitted model can input multiple images, we will input all images of a study. If the submitted model includes only one image, we will default to using the frontal image. Additionally, we have the context file, and the model can select if you are going to use this info. Run the evaluation script on the MIMIC-CXR test set and obtain the output score file, which needs to be included in the submission.

## 2. Model Submission

Your model submission should include the following:

1. **Model Description:** This description identifies your submission on the leaderboard: {Name_of_model} (Institution) paper link, code link, year

2. **Conda Environment File:** Include the `environment.yaml` file support `conda install`.

3. **Inference Script:** The model should support the following command: ```python inference.py <input_json_file> <output_json_file> <img_root_dir>```  We provide an [example](/ReXrank-test/example_ile/merversa_inference.py) of MedVersa for understanding our requirements. 

4. **Evaluation Result:** Include the evaluation result on the MIMIC-CXR test set.

Please send an email to Xiaoman Zhang xiaomanzhang.zxm@gmail.com with all the required information. Use the email title format: [ReXrank Submission] + Name_of_model. 

## Removing Your Models from the Leaderboard

If you decide you no longer want your model's score on the leaderboard, you can send an email to us. When the leaderboard updates, your model will no longer appear.

