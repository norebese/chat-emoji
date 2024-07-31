import deepl
import os
from dotenv import load_dotenv

# 예시 인풋
#t1 = [{'label': '불평/불만', 'score': 0.7809296250343323}, {'label': '짜증', 'score': 0.8571460247039795}, {'label': '힘듦/지침', 'score': 0.7137463688850403}]
#t2 = '지하철에 사람도 많고 지하철에 사람도 많아서 힘들어서 죽는줄 오늘까지 다 완성해야 하는데 시간이 없어 시간이 없어  시간이 없어 내일까지 완성해야 하는데 시간이 없어 시간이 없어'

# env로드, 및 값을 불러와 할당
load_dotenv()
auth_key = os.getenv('DeepL_API_Key')
translator = deepl.Translator(auth_key)

def deep_l(emotion_list,sentence,translator=translator) :
    result = {}
    emotion_before = [] # 번역 전의 감정:확률을 담을 리스트
    emotion_after = [] # 번역 후의 감정:확률을 담을 리스트

    emotion = [] # 감정들을 담을 리스트

    #번역 전의 받아온 리스트 처리
    for item in emotion_list:
        emotion_before.append((item['label'],round(item['score'],2)))
        emotion.append(item['label'])
    
    # 감정 단어들을 ,으로 합침
    emotion_str = ','.join(emotion)
    # 감정 단어를 합친 문자열에 문장을 합침
    text = emotion_str+','+sentence
    
    # 번역기 설정. 인풋 코리안, 아웃풋 영어
    translation = translator.translate_text(text, source_lang ="KO", target_lang="EN-US")
    # 번역 결과를 ,를 기준으로 분리해 리스트화
    translation = translation.text.split(',')
    # 0,1,2 : 감정 번역 결과, 3(-1) : 문장 번역 결과
    translation_emotion = translation[0:3]

    # translation_emotion,emotion_before , 번역한 이모션 리스트와 번역 전의 이모션 튜플을 묶어 빼옴
    for text,tup in zip(translation_emotion,emotion_before):
        emotion_after.append((text,tup[-1]))

    result['ref'] = {'emotion':emotion_before,'sentence':sentence}
    result['processed'] = {'emotion':emotion_after,'sentence':translation[-1]}
    
    #결과 반환
    return result

#test= deep_l(t1,t2)
#print(test)
#{'ref': {'emotion': [('불평/불만', 0.78), ('짜증', 0.86), ('힘듦/지침', 0.71)], 'sentence': '지하철에 사람도 많고 지하철에 사람도 많아서 힘들어서 죽는줄 오늘까지 다 완성해야 하는데 시간이 없어 시간이 없어  시간이 없어 내일까지 완성해야 하는데 시간이 없어 시간이 없어'}, 'processed': {'emotion': [('Complain/Complain', 0.78), ('Irritated', 0.86), ('Difficult/Instructive', 0.71)], 'sentence': "There are a lot of people in the subway and there are a lot of people in the subway and it's killing me I have to finish it by today and I don't have time I don't have time I don't have time I don't have time I don't have time I don't have time I don't have time I don't have time I don't have time"}}

