from transformers import T5ForConditionalGeneration, T5Tokenizer, pipeline

# tokenizer model - loaded once
tokenizer = T5Tokenizer.from_pretrained('t5-base', model_max_length=5000)

# summarizer model - loaded once
model = T5ForConditionalGeneration.from_pretrained('t5-base')

article = """

"""

# inputs = tokenizer.encode("summarize(but preserve important information): " + article, return_tensors="pt", max_length=5000, truncation=True)

# summary_ids = model.generate(inputs, max_length=300, num_beams=2, length_penalty=2.0, early_stopping=True)

# summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)


def summarize_it(article: str):
    inputs = tokenizer.encode("summarize: " + article, return_tensors="pt", max_length=5000, truncation=True)

    summary_ids = model.generate(inputs, max_length=300, num_beams=2, length_penalty=2, early_stopping=True)

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary


if __name__ == '__main__':        
    print("*"*100)
    print(summarize_it(article))