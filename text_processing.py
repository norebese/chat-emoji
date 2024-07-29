# text_processing.py

from konlpy.tag import Okt
from collections.abc import Mapping  # collections 대신 collections.abc 사용

class TextProcessor:
    def __init__(self):
        self.okt = Okt()
        self.task_list = []
        self.target = []
        self.current_sentence = []

    def process_text(self, userText):
        self.task_list.append(userText)
        words = self.okt.pos(userText)
        for word, pos in words:
            self.current_sentence.append(word)
            if pos == 'Verb':
                self.target.append(' '.join(self.current_sentence))
                self.current_sentence = []

        self.finalize_target()
        return True

    def finalize_target(self):
        if self.current_sentence:
            if self.target:
                self.target[-1] += ' ' + ' '.join(self.current_sentence)
            else:
                self.target.append(' '.join(self.current_sentence))

    def get_results(self):
        merged_sentence = ' '.join(self.task_list)
        return self.task_list, self.target, merged_sentence
