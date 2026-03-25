import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer

def train():
    model_id = "Qwen/Qwen2.5-0.5B-Instruct"
    
    print("Loading model and tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    # Load the model. (Requires a GPU for reasonable training times)
    model = AutoModelForCausalLM.from_pretrained(
        model_id, 
        device_map="auto", 
        torch_dtype=torch.bfloat16
    )

    print("Applying LoRA configuration...")
    # LoRA allows us to train just a tiny fraction of the model's parameters, saving memory
    lora_config = LoraConfig(
        r=8, 
        lora_alpha=32, 
        target_modules=["q_proj", "v_proj"], 
        lora_dropout=0.05, 
        bias="none", 
        task_type="CAUSAL_LM"
    )
    model = get_peft_model(model, lora_config)

    print("Loading dataset...")
    # Replace 'dataset.jsonl' with your actual training data file
    dataset = load_dataset("json", data_files="dataset.jsonl", split="train")

    print("Starting training...")
    training_args = TrainingArguments(
        output_dir="./results",
        per_device_train_batch_size=2,
        num_train_epochs=3,       # How many times to loop through the data
        learning_rate=2e-4,
        logging_steps=10,
    )

    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        dataset_text_field="text",
        args=training_args,
    )

    trainer.train()

    print("Saving the custom model...")
    # Save the fine-tuned model to a local folder
    model.save_pretrained("./my-custom-model")
    tokenizer.save_pretrained("./my-custom-model")
    print("Done! You can now load the model from './my-custom-model'")

if __name__ == "__main__":
    train()