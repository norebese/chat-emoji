import nltk
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForSequenceClassification, TextClassificationPipeline

nltk.download('punkt')
# nltk.download('all')
compress_model = AutoModelForSeq2SeqLM.from_pretrained('eenzeenee/t5-small-korean-summarization')
compress_tokenizer = AutoTokenizer.from_pretrained('eenzeenee/t5-small-korean-summarization')

model_name = "searle-j/kote_for_easygoing_people"
emotion_model = AutoModelForSequenceClassification.from_pretrained(model_name)
emotion_tokenizer = AutoTokenizer.from_pretrained(model_name)

pipe = TextClassificationPipeline(
    model=emotion_model,
    tokenizer=emotion_tokenizer,
    device=-1,  # gpu number, -1 if cpu used
    return_all_scores=True,
    function_to_apply='sigmoid'
)


# 문장 요약 모델
def compress_process(inputs):
    inputs = compress_tokenizer(inputs, max_length=512, truncation=True, return_tensors="pt")
    output = compress_model.generate(**inputs, num_beams=3, do_sample=True, min_length=10, max_length=64)
    decoded_output = compress_tokenizer.batch_decode(output, skip_special_tokens=True)[0]
    result = nltk.sent_tokenize(decoded_output.strip())[0]
    return result


# 문장 감정 분석 모델
def analyze_sentiment(text):
    results = []
    for output in pipe(text)[0]:
        if output["score"] > 0.4:
            results.append(output)
    # Sort the results by score in descending order and take the top 3
    top_3_results = sorted(results, key=lambda x: x["score"], reverse=True)[:3]

    return top_3_results


# txt = 'ㅋㅋㅋ 오늘 날씨 흐림. 쪄 죽겠다 ㅜㅜ 올 때 메로나 사와~! 아 오늘 한강공원 가려고 했는데...'
# result = compress_process(txt)
# print(result)