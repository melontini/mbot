import markovify
import re
import spacy

SEPARATOR = r"\s*@@note@@\s*"

nlp = spacy.load("en_core_web_sm")

class Text(markovify.Text):
    def word_split(self, sentence):
        ret = []

        for word in nlp(sentence):
            if word.pos_ == 'PUNCT':
                continue

            ret.append("::".join((word.orth_, word.pos_)))

        return ret

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence
    
    def sentence_split(self, text):
        return re.split(SEPARATOR, text)
