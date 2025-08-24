import json
import torch
from transformers import AutoModelForImageTextToText, AutoProcessor
from PIL import Image
import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser(description='MedGemma VQA inference')
    parser.add_argument('--input_json_file', type=str, default='../../data/mimic-cxr/test_data.json')
    parser.add_argument('--save_json_file', type=str, default='../../results/mimic-cxr/MedGemma.json')
    parser.add_argument('--img_root_dir', type=str, default='../../data/mimic-cxr/MIMIC-CXR-JPG/files')
    return parser.parse_args()

def load_image(image_path):
    """Load and preprocess a single image"""
    try:
        image = Image.open(image_path).convert("RGB")
        return image
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None

def main():
    # Parse arguments
    args = parse_args()
    
    # Check if CUDA is available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    # Initialize model and processor
    model_name = "google/medgemma-4b-it"
    print(f"Loading model: {model_name}")
    model = AutoModelForImageTextToText.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16,
        device_map="auto"
    )
    processor = AutoProcessor.from_pretrained(model_name)
    model.eval()
    
    # Load input data
    print(f"Loading data from: {args.input_json_file}")
    with open(args.input_json_file, 'r') as file:
        input_data_dict = json.load(file)
    
    # Check if save file exists
    if os.path.exists(args.save_json_file):
        with open(args.save_json_file, 'r') as file:
            save_data_dict = json.load(file)
    else:
        save_data_dict = {}
    
    # Process a single study for demonstration
    study_id = next(iter(input_data_dict))
    print(f"Processing study: {study_id}")
    
    data_dict_idx = input_data_dict[study_id]
    save_data_dict_idx = data_dict_idx.copy()
    
    # Get image path
    image_path_list = data_dict_idx['image_path']
    img_path = os.path.join(args.img_root_dir, image_path_list[0])
    
    # Load image
    print(f"Loading image: {img_path}")
    image = load_image(img_path)
    if image is None:
        print("Failed to load image. Exiting.")
        return
    
    # Get context (if available)
    context = data_dict_idx.get('context', '')
    
    # Create question for VQA
    question = "Can you describe the key findings in this chest X-ray?"
    
    # Prepare messages for MedGemma
    messages = [
        {
            "role": "system",
            "content": [{"type": "text", "text": "You are an expert medical professional specializing in medical image analysis."}]
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": f"{context}\n{question}"},
                {"type": "image", "image": image}
            ]
        }
    ]
    
    # Process input using MedGemma's chat template
    print("Processing input...")
    inputs = processor.apply_chat_template(
        messages, 
        add_generation_prompt=True, 
        tokenize=True,
        return_dict=True, 
        return_tensors="pt"
    ).to(device, dtype=torch.bfloat16)
    
    input_len = inputs["input_ids"].shape[-1]
    
    # Generate response
    print("Generating response...")
    with torch.inference_mode():
        generation = model.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=processor.tokenizer.eos_token_id
        )
        generation = generation[0][input_len:]
    
    # Decode the generated text
    response = processor.decode(generation, skip_special_tokens=True)
    
    # Save results
    save_data_dict_idx['model_prediction'] = response.strip()
    save_data_dict[study_id] = save_data_dict_idx
    
    # Write to output file
    print(f"Saving results to: {args.save_json_file}")
    os.makedirs(os.path.dirname(args.save_json_file), exist_ok=True)
    with open(args.save_json_file, 'w') as file:
        json.dump(save_data_dict, file, indent=4)
    
    # Print results
    print("\n--- Results ---")
    print(f"Context: {context}")
    print(f"Question: {question}")
    print(f"Answer: {response.strip()}")
    print(f"Results saved to: {args.save_json_file}")

if __name__ == "__main__":
    main()
