import re
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from konlpy.tag import Komoran
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
import itertools
import numpy as np
import time, datetime
import matplotlib.pyplot as plt
from collections.abc import Mapping 

from konlpy.tag import Komoran
komoran = Komoran()

from transformers import AutoTokenizer, AutoModelForMaskedLM
tokenizer = AutoTokenizer.from_pretrained("monologg/kobert")
model = AutoModelForMaskedLM.from_pretrained("monologg/kobert")

# 문단을 문장으로 나누는 함수
def sentence_tokenizer(paragraph):
    return re.split(r'(?<=[.!?])\s+', paragraph)

# 문장 어절 단위로 토큰화
def word_tokenizer(sentence):
    return sentence.split(' ')

# 따옴표와 따옴표를 포함하는 문장을 하나의 토큰으로
def process_quoted_words(tokens):
    processed_tokens = []
    quoted_word = ""
    in_quote = False

    for token in tokens:
        if "'" in token:
            if in_quote:
                quoted_word += " " + token
                processed_tokens.append(quoted_word)
                quoted_word = ""
                in_quote = False
            else:
                quoted_word = token
                in_quote = True
        else:
            if in_quote:
                quoted_word += " " + token
            else:
                processed_tokens.append(token)
    return processed_tokens

# 형태소 분석 후 문법적 중요도 점수 추가
def add_linguistic_score(sentence):
    pos = komoran.pos(sentence)
    score = 0
    for p in pos:
        if p[1] == 'NNP':
            score += 0.000001
        elif p[1] == 'NNG':
            score += 0.000001
        elif p[1] == 'vv':
            score += 0.000001
        elif p[1] == 'SL':
            score += 0.000001
        elif p[1] == 'JKS':
            score += 00.000001
        elif p[1] == 'JKO':
            score += 0.000001
    quoted_words = re.findall(r"'(.*?)'", sentence)
    for quoted_word in quoted_words:
        score += 0.0001
    return score

# KoBERT 모델을 이용하여 perplexity 계산
def calculate_perplexity_score(sentence):
    # KoBERT 모델이 이해할 수 있는 형태로 tokenize
    tokens = tokenizer.tokenize(sentence)
    token_ids = tokenizer.convert_tokens_to_ids(tokens)

    # [MASK] 토큰 위치 찾기
    mask_token_index = token_ids.index(tokenizer.mask_token_id)

    # 입력값 생성
    input_ids = torch.tensor([token_ids])
    outputs = model(input_ids)
    predictions = outputs[0]

    # [MASK] 토큰 위치에 대한 예측값 추출
    masked_predictions = predictions[0, mask_token_index]

    # softmax 함수를 이용하여 확률값을 확률 분포로 변환
    probs = torch.softmax(masked_predictions, dim=-1)

    # perplexity 계산
    perplexity = torch.exp(torch.mean(torch.log(probs)))

    return perplexity.item()

# 압축 문장 후보 생성 및 문법적 중요도 점수 계산
def compress_sentence(token):
    compressed_candidates = []
    max_n = 4 #len(token) - 4

    for n in range(1, max_n + 1):
        for i in range(len(token) - n + 1):
            compressed_tokens = token[:i] + token[i + n:]
            compressed_sentence = " ".join(compressed_tokens)
            score = add_linguistic_score(compressed_sentence)
            compressed_candidates.append((compressed_sentence, score, n))

    perplexity_scores = []
    compressed_candidates_with_score = []

    for n in range(1, max_n + 1):
        for i in range(len(token) - n + 1):
            mask_idx = list(range(i, i + n))
            masked_tokens = list(token)
            for j in mask_idx:
                masked_tokens[j] = "[MASK]"
            masked_sentence = " ".join(masked_tokens)

            perplexity_score = calculate_perplexity_score(masked_sentence)
            linguistic_score = compressed_candidates[i][1]
            final_score = perplexity_score - linguistic_score

            perplexity_scores.append(perplexity_score)
            compressed_candidates_with_score.append((re.sub(r'\[MASK\]\s*', '', masked_sentence), final_score, n))

    compressed_candidates_with_score_sorted = sorted(compressed_candidates_with_score, key=lambda x: x[1])
    final_compressed_sentence = re.sub(r'\[MASK\]\s*', '', compressed_candidates_with_score_sorted[0][0])
    selected_n = compressed_candidates_with_score_sorted[0][2]

    return compressed_candidates_with_score_sorted, final_compressed_sentence, selected_n

def compress_paragraph(paragraph):
    sentences = sentence_tokenizer(paragraph)
    compressed_sentences = []

    for sentence in sentences:
        token = word_tokenizer(sentence)
        token = process_quoted_words(token)
        compressed_candidates_with_score_sorted, final_compressed_sentence, selected_n = compress_sentence(token)
        compressed_sentences.append(final_compressed_sentence)

    compressed_paragraph = ' '.join(compressed_sentences)
    return compressed_paragraph

def compress_result(paragraph):
    compressed_paragraph = compress_paragraph(paragraph)
    print(compress_paragraph)
    return compressed_paragraph