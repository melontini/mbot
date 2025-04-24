import chain
import sys
import requests

import secrets__

model_f = open("model.json")
model = chain.Text.from_json(model_f.read())

generated = False
text = None

while not generated:
    text = model.make_short_sentence(80, tries=900, min_words=3)
    generated = text is not None

text = text.replace('@','@​').replace('#','#​')
print(text)

requests.post("https://beeping.synth.download/api/iceshrimp/notes", json={
    'visibility': 'home',
    'text': text,
    #'cw': 'gyattov generated text',
}, headers={"Authorization": f"Bearer {secrets__.TOKEN}"})