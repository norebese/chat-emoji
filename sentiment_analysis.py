from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline

model_name = "searle-j/kote_for_easygoing_people"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

pipe = TextClassificationPipeline(
    model=model,
    tokenizer=tokenizer,
    device=-1,  # gpu number, -1 if cpu used
    return_all_scores=True,
    function_to_apply='sigmoid'
)

def analyze_sentiment(text):
    results = []
    for output in pipe(text)[0]:
        if output["score"] > 0.4:
            results.append(output)
    return results