import re
import json
import sys

print('[+] loading nlp enhanced markov chain')
import chain

MFM_BEGIN = re.compile(r'\$\[[a-z0-9.,=]+')
MFM_END = re.compile(r'\]+')
HTML = re.compile(r'</?[a-z]+>')
SPACE = re.compile(r'[ \n]+')

print('[+] loading note json')
export_f = sys.argv[1]
export = open(export_f)
export_json = json.load(export)

corpus = []

for note in export_json:
    if note.get('visibility') not in ['public', 'home']:
        continue

    if note.get('localOnly'):
        continue

    if note.get('cw'):
        continue

    text = note.get('text')
    if not text:
        continue

    text = text.lower() 
    text = re.sub(MFM_BEGIN, '', text)
    text = re.sub(MFM_END, '', text)
    text = re.sub(HTML, '', text)
    text = re.sub(SPACE, ' ', text)
    text = text.strip()

    print(f"     - {text}")
    corpus.append(text)

print('[+] building markov chain')
model = chain.Text("@@note@@".join(corpus), well_formed=False)
model_json = model.compile().to_json()

print('[+] exporting')
export = open(export_f.replace('.json', '.model.json'), 'w')
export.write(model_json)
