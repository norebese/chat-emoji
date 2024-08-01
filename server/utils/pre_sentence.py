# pre_sentence.py
from mecab import MeCab
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SentenceProcessor:
    def __init__(self):
        self.mecab = MeCab()
        self.current_sentence = []
        self.textlist = []

    def check_verb(self, sentence):
        pos_text = self.mecab.pos(sentence)
        logger.info(f"형태소 분석 '{sentence}': {pos_text}")
        return any(pos.startswith(('VV', 'VA', 'XSV')) for _, pos in pos_text)

    def process_chat(self, chat_message):
        self.current_sentence.append(chat_message)

        if self.check_verb(chat_message):
            # 현재까지의 문장을 결합
            complete_sentence = ' '.join(self.current_sentence)
            self.textlist.append(complete_sentence)

            # 현재 문장 초기화
            self.current_sentence = []

        logger.info(f"현재 문장: {self.current_sentence}")
        logger.info(f"현재 텍스트리스트: {self.textlist}")

        return self.textlist


# 싱글톤 인스턴스 생성
sentence_processor = SentenceProcessor()