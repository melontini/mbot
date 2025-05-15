import markovify
import re
import spacy

SEPARATOR = r"\s*@@note@@\s*"

nlp = spacy.load("en_core_web_sm")

class Text(markovify.Text):
    def word_split(self, sentence):
        ret = []

        for part in re.split(r'(:[a-zA-Z0-9_.-]+:|@[a-zA-Z0-9_.-]+(?:@[a-zA-Z0-9_.-]+)?)', sentence):
            if part.startswith(':') or part.startswith('@'):  # TODO: idk how accurate these will be
                ret.append(f'{part}::X')
                continue

            for word in nlp(part):
                ret.append("::".join((word.text_with_ws, word.pos_)))

        return ret

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence
    
    def sentence_split(self, text):
        return re.split(SEPARATOR, text)
