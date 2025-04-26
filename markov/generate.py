# most of the modifications for posting on bsky were copy pasted from this page: https://docs.bsky.app/docs/advanced-guides/posts

import chain
import sys
import requests
import json
from datetime import datetime, timezone
# from atproto import Client

import secrets__

model_f = open( secrets__.PATH + "model.json")
model = chain.Text.from_json(model_f.read())

generated = False
text = None

while not generated:
    text = model.make_short_sentence(80, tries=900, min_words=3)
    generated = text is not None

text = text.replace('@','@​').replace('#','#​')
print(text)

# Fediverse posting code
requests.post("https://cafe.autumn.town/api/iceshrimp/notes", json={
    'visibility': 'home',
    'text': text,
    #'cw': 'gyattov generated text', # Ruben has Left His Mark 
}, headers={"Authorization": f"Bearer {secrets__.TOKEN}"})


# Bsky posting code

pds_url = "https://pds.lobotomy.town"
session = requests.post(
    pds_url + "/xrpc/com.atproto.server.createSession",
    json={
        "identifier": "markov.autumn.town",
        "password": secrets__.BSKY,
    },
)
# Fetch the current time
# Using a trailing "Z" is preferred over the "+00:00" format
now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

# Required fields that each post must include
post = {
    "$type": "app.bsky.feed.post",
    "text": text,
    "createdAt": now,
}

resp = requests.post(
    pds_url + "/xrpc/com.atproto.repo.createRecord",
    headers={"Authorization": f"Bearer {session.json()['accessJwt']}"},
    json={
        "repo": "did:plc:vwcw6xd4udigfcylfhgh5deb",
        "collection": "app.bsky.feed.post",
        "record": post,
    },
)
resp.raise_for_status()