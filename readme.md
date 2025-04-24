# autumnated

i just stole from [sneexy's repo](https://forged.synth.download/sneexy/markov) the innovation i bring is just a script that converts mastodon to misskey for the sake of having journalist posts work with this mate also i guess nix flake so i don't need to put a bullet into my head dealing with python  (instead, i blow my head off dealing with nix )

# markov

minimally modified fork of [kopper's markov bot](https://activitypub.software/kopper/markov) to post to iceshrimp.net. while still only taking in misskey exports. that's all i needed.

## use

clone the repository somewhere:
```sh
git clone https://forged.synth.download/sneexy/markov.git
cd markov
```

ideally, create a venv first:
```sh
python -m venv venv
source ./venv/bin/activate # assuming we're still in the markov folder - you'll need to do this everytime you want to use the bot, make a script or something to make it easier
```

now install everything:
```sh
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

import your misskey notes export:
```sh
python import-misskey.py name-of-your-notes-export.json # will take a bit depending on how large your export is
mv xxxxx.model.json model.json # exported file will be named something else, rename it to model.json to prevent it from erroring out when generating
```

add your iceshrimp.net user/bot account token:
```sh
echo "TOKEN='InsertVerySecureTokenHere'" > secrets__.py
```

...then edit `generate.py` and modify the `requests.post` section near the bottom to point the url to your instance.

ℹ️ alternatively, if you'd like to use this to post to misskey, replace it with this (replacing `yourinstance.tld` with your instance):
```python
requests.post("https://yourinstance.tld/api/notes/create", json={
    'i': secrets__.TOKEN,

    'visibility': 'home',
    'noExtractMentions': True,
    'noExtractHashtags': True,

    'text': text,
    #'cw': 'markov chain generated post'
})

```

...or perhaps with mastodon (untested):
```python
requests.post("https://yourinstance.tld/api/v1/statuses", json={
    "status": text,
    #"spoiler_text": "markov chain generated post",
    "visibility": "unlisted"
}, headers={"Authorization": f"Bearer {secrets__.TOKEN}"})
```

finally, make a markov generated post:
```sh
python generate.py
```

you can use a cronjob/crontab on your user to automate posting, for example, to post every two hours:
```
0 */2 * * * cd /home/ruben/markov && source /home/ruben/markov/venv/bin/activate && python /home/ruben/markov/generate.py
```

### example script

here's a dumb and probably over engineered script i made to interact with the bot. you may edit this and use it to your own will and needs.
```bash
#!/bin/bash
# cding into the markov directory is required otherwise it fails to load the model
CURRENT_DIR=$(pwd)
cd /home/ruben/markov && \
  source /home/ruben/markov/venv/bin/activate && \
  python /home/ruben/markov/generate.py && \
  cd $CURRENT_DIR
```