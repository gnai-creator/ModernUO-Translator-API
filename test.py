from transformers import MarianTokenizer, MarianMTModel, pipeline

model_name = "Helsinki-NLP/opus-mt-mul-mul"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)
translator = pipeline("translation", model=model, tokenizer=tokenizer)

text = ">>en<< Olá, mundo!"
print(translator(text, max_length=128))
