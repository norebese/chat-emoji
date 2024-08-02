# pre_sentence.py
from mecab import MeCab
# from mecab
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SentenceProcessor:
    def __init__(self):
        self.mecab = MeCab()
        self.current_sentence = {}
        self.textlist = {}

    def check_verb(self, sentence):
        pos_text = self.mecab.pos(sentence)
        # logger.info(f"Morpheme analysis for '{sentence}': {pos_text}")
        return any(pos.startswith(('VV', 'VA', 'XSV')) for _, pos in pos_text)

    def process_chat(self, sender, chat_message):
        if sender not in self.current_sentence:
            self.current_sentence[sender] = []
        if sender not in self.textlist:
            self.textlist[sender] = []

        self.current_sentence[sender].append(chat_message)

        if self.check_verb(chat_message):
            # 현재까지의 문장을 결합
            complete_sentence = ' '.join(self.current_sentence[sender])
            self.textlist[sender].append(complete_sentence)

            # 현재 문장 초기화
            self.current_sentence[sender] = []

        # logger.info(f"Current sentence for {sender}: {self.current_sentence[sender]}")
        # logger.info(f"Current textlist for {sender}: {self.textlist[sender]}")

        return self.textlist[sender], self.current_sentence[sender]


# 싱글톤 인스턴스 생성
sentence_processor = SentenceProcessor()