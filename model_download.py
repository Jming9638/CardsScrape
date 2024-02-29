from transformers import AutoModel, AutoTokenizer


model_name = "google/flan-t5-large"

model = AutoModel.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Save the model and tokenizer to your local disk
model_save_path = "./huggingface/google/flan-t5-large/model"
tokenizer_save_path = "./huggingface/google/flan-t5-large/tokenizer"

model.save_pretrained(model_save_path)
tokenizer.save_pretrained(tokenizer_save_path)
