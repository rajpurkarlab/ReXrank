import json
import torch
from transformers import AutoModelForImageTextToText, AutoProcessor
from PIL import Image
from pathlib import Path
from tqdm import tqdm
import os

class MedGemmaMCQInference:
    def __init__(self, model_name="google/medgemma-4b-it", device="cuda"):
        """
        Initialize the MedGemma model and processor
        Args:
            model_name (str): Name or path of the model
            device (str): Device to run inference on ("cuda" or "cpu")
        """
        self.device = device
        self.model = AutoModelForImageTextToText.from_pretrained(
            model_name,
            torch_dtype=torch.bfloat16,
            device_map="auto"
        )
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model.eval()

    def load_images(self, image_paths, base_path=""):
        """
        Load images from paths
        Args:
            image_paths (list): List of image paths
            base_path (str): Base path to prepend to image paths
        Returns:
            list: List of loaded images (limited to first 2 for MedGemma)
        """
        images = []
        for img_path in image_paths:
            full_path = Path(base_path) / img_path.lstrip('/')
            try:
                img = Image.open(str(full_path)).convert("RGB")
                images.append(img)
            except Exception as e:
                print(f"Error loading image {full_path}: {e}")
        
        # MedGemma works best with single images, but we'll take the first one
        # If you need multiple images, you might need to process them separately
        return images[:1] if images else []

    def generate_prompt(self, question: str, options: list, context: str = "") -> str:
        """
        Generate a prompt for the medical question-answering model.
        Args:
            question (str): The medical question to be answered
            options (list): List of option strings
            context (str, optional): Additional context or information. Defaults to "".
        Returns:
            str: Formatted prompt string ready for model input
        """
        system_prompt = """You are a medical expert assistant. Your task is to answer multiple-choice questions about medical images. Please analyze the image carefully and select the single most correct answer. Reply with only the letter of your choice (A/B/C/D)."""
        
        formatted_options = "\n".join(f"{opt}" for opt in options)
        
        prompt_parts = [
            "Question: " + question.strip(),
            "\nOptions:",
            formatted_options
        ]
        
        if context and context.strip():
            prompt_parts.insert(1, f"\nContext: {context.strip()}")
        
        prompt_parts.append("\nAnswer:")
        
        return "\n".join(prompt_parts)
    
    def process_single_case(self, case_data, base_path=""):
        """
        Process a single case
        Args:
            case_data (dict): Case data including images, question, and options
            base_path (str): Base path for image loading
        Returns:
            dict: Results including model's answer and confidence
        """
        # Load images (taking only the first one for MedGemma, first is AP/PA)
        images = self.load_images(case_data['image_path_list'], base_path)  
        if not images:
            return {"error": "No images could be loaded"}

        # Generate prompt
        prompt = self.generate_prompt(
            case_data['question'],
            case_data['options'],
            case_data.get('context', '')
        )

        # Prepare messages for MedGemma
        messages = [
            {
                "role": "system",
                "content": [{"type": "text", "text": "You are an expert medical professional specializing in medical image analysis and diagnosis."}]
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image", "image": images[0]}
                ]
            }
        ]

        try:
            # Process input using MedGemma's chat template
            inputs = self.processor.apply_chat_template(
                messages, 
                add_generation_prompt=True, 
                tokenize=True,
                return_dict=True, 
                return_tensors="pt"
            ).to(self.device, dtype=torch.bfloat16)

            input_len = inputs["input_ids"].shape[-1]

            # Generate response
            with torch.inference_mode():
                generation = self.model.generate(
                    **inputs,
                    max_new_tokens=256,
                    do_sample=False,  # Use deterministic generation for MCQ
                    temperature=0.1,
                    pad_token_id=self.processor.tokenizer.eos_token_id
                )
                generation = generation[0][input_len:]

            # Decode the generated text
            response = self.processor.decode(generation, skip_special_tokens=True)
            response = response.strip()

            return {
                "model_response": response,
                "question_id": case_data.get('study_id', '') + '_' + case_data.get('task_name', ''),
                "question": case_data.get('question', ''),
                "options": case_data.get('options', []),
                "correct_answer": case_data.get('correct_answer', ''),
                "category": case_data.get('category', ''),
                "subcategory": case_data.get('subcategory', ''),
                "num_images_used": len(images)
            }

        except Exception as e:
            return {
                "error": f"Processing error: {str(e)}",
                "question_id": case_data.get('study_id', '') + '_' + case_data.get('task_name', ''),
                "question": case_data.get('question', ''),
                "options": case_data.get('options', []),
                "correct_answer": case_data.get('correct_answer', ''),
            }

    def process_batch(self, json_data, base_path="", output_file="../results/MedGemma.json"):
        """
        Process multiple cases with progress bar and checkpointing
        Args:
            json_data (dict): Dictionary containing multiple cases
            base_path (str): Base path for image loading
            output_file (str): Path to save results
        Returns:
            dict: Results for all cases
        """
        # Load existing results if available
        results = {}
        if os.path.exists(output_file):
            try:
                with open(output_file, 'r') as f:
                    results = json.load(f)
                print(f"Loaded {len(results)} existing results from {output_file}")
            except json.JSONDecodeError:
                print(f"Error loading existing results from {output_file}, starting fresh")

        # Create progress bar
        pbar = tqdm(total=len(json_data), desc="Processing cases with MedGemma")
        # Update progress bar based on existing results
        pbar.update(len(results))

        # Process remaining cases
        for case_id, case_data in json_data.items():
            # Skip if already processed
            if case_id in results:
                continue

            try:
                results[case_id] = self.process_single_case(case_data, base_path)
                
                # Save results after each successful case (checkpointing)
                with open(output_file, 'w') as f:
                    json.dump(results, f, indent=2)
                    
            except Exception as e:
                results[case_id] = {"error": str(e)}
                print(f"Error processing case {case_id}: {e}")
                
                # Also save on error
                with open(output_file, 'w') as f:
                    json.dump(results, f, indent=2)
            
            pbar.update(1)

        pbar.close()
        print(f"Processing complete. Processed {len(results)} cases.")
        return results

    def evaluate_results(self, results_file):
        """
        Evaluate the results by comparing model answers with correct answers
        Args:
            results_file (str): Path to results JSON file
        Returns:
            dict: Evaluation metrics
        """
        with open(results_file, 'r') as f:
            results = json.load(f)
        
        correct = 0
        total = 0
        category_stats = {}
        
        for case_id, result in results.items():
            if 'error' in result:
                continue
                
            total += 1
            correct_answer = result.get('correct_answer', '').strip().upper()
            model_response = result.get('model_response', '').strip().upper()
            
            # Extract answer letter from model response
            model_answer = ''
            for char in model_response:
                if char in ['A', 'B', 'C', 'D']:
                    model_answer = char
                    break
            
            if model_answer == correct_answer:
                correct += 1
            
            # Track by category
            category = result.get('category', 'Unknown')
            if category not in category_stats:
                category_stats[category] = {'correct': 0, 'total': 0}
            category_stats[category]['total'] += 1
            if model_answer == correct_answer:
                category_stats[category]['correct'] += 1
        
        overall_accuracy = correct / total if total > 0 else 0
        
        # Calculate category accuracies
        for category in category_stats:
            cat_correct = category_stats[category]['correct']
            cat_total = category_stats[category]['total']
            category_stats[category]['accuracy'] = cat_correct / cat_total if cat_total > 0 else 0
        
        return {
            'overall_accuracy': overall_accuracy,
            'correct': correct,
            'total': total,
            'category_stats': category_stats
        }

def main():
    # Configuration
    base_path = None # image_root_dir
    input_file = "sample.json" 
    output_file = "../results/MedGemma.json"

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Initialize model
    print("Initializing MedGemma model...")
    inferencer = MedGemmaMCQInference()
    
    # Load JSON data
    print(f"Loading data from {input_file}...")
    with open(input_file, 'r') as f:
        cases = json.load(f)
    
    print(f"Loaded {len(cases)} cases")
    
    # Process all cases with progress bar and checkpointing
    results = inferencer.process_batch(cases, base_path, output_file)
    print(f"\nProcessing complete. Results saved to {output_file}")
    
    # Evaluate results
    print("\nEvaluating results...")
    eval_results = inferencer.evaluate_results(output_file)
    print(f"Overall Accuracy: {eval_results['overall_accuracy']:.3f} ({eval_results['correct']}/{eval_results['total']})")
    
    print("\nCategory-wise Results:")
    for category, stats in eval_results['category_stats'].items():
        print(f"  {category}: {stats['accuracy']:.3f} ({stats['correct']}/{stats['total']})")

if __name__ == "__main__":
    main()
