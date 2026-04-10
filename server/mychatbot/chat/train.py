from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model
import torch

def train():
    # 1. Load dataset
    dataset = load_dataset("json", data_files="data.jsonl", split="train")

    # 2. Load model
    model_id = "Qwen/Qwen2.5-0.5B-Instruct"

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    tokenizer.pad_token = tokenizer.eos_token  # Important

    #FIXED MODEL LOADING (CPU SAFE)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.float32
    )

    model.to("cpu")

    # 3. Apply LoRA
    lora_config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )

    model = get_peft_model(model, lora_config)

    # 4. Tokenize dataset
    def tokenize(example):
        outputs = tokenizer(
            example["text"],
            truncation=True,
            padding="max_length",
            max_length=250
        )
        outputs["labels"] = outputs["input_ids"].copy()
        return outputs

    dataset = dataset.map(tokenize, batched=True)

    #FIXED TRAINING ARGS (CPU SAFE)
    training_args = TrainingArguments(
        output_dir="./qwen-finetuned",
        per_device_train_batch_size=1,
        num_train_epochs=3,
        logging_steps=10,
        save_steps=50,
        fp16=False,  
        gradient_accumulation_steps=2 
    )

    # 6. Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset
    )

    # 7. Train
    print("Training started...")
    trainer.train()

    # 8. Save model
    model.save_pretrained("./my-company-model")
    tokenizer.save_pretrained("./my-company-model")

    print("Training completed! Model saved in ./my-company-model")

if __name__ == "__main__":
    train()