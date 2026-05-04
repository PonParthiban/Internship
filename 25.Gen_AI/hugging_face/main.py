from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "gpt2"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

inputs = tokenizer("AI is", return_tensors="pt")
outputs = model.generate(**inputs, max_length=20)

print(tokenizer.decode(outputs[0]))