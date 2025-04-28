# most of the modifications for posting on bsky were copy pasted from this page: https://docs.bsky.app/docs/advanced-guides/posts

import chain
import sys
import requests
import json
import argparse
from datetime import datetime, timezone
# from atproto import Client

parser = argparse.ArgumentParser(description="markov chain bot for bsky and iceshrimp")

parser.add_argument(
    "--did",
    type=str,
    default=None,
    help="at-proto/bluesky did",
    required=False
)

parser.add_argument(
    "--pds",
    type=str,
    default="bsky.social",
    help="at-proto/bluesky pds",
    required=False
)

parser.add_argument(
    "--password",
    type=str,
    default=None,
    help="at-proto/bluesky app-password",
    required=False
)

parser.add_argument(
    "--domain",
    type=str,
    default=None,
    help="domain of your iceshrimp instance",
    required=False
)

parser.add_argument(
    "--token",
    type=str,
    default=None,
    help="access token for your iceshrimp user",
    required=False
)

parser.add_argument(
    "--model",
    type=str,
    default="model.json",
    help="path to the model file",
    required=False
)

parser.add_argument(
    "--max",
    type=int,
    default=80,
    help="maximum number of chars a model can generate",
    required=False
)

parser.add_argument(
    "--overlap",
    type=int,
    default=15,
    help="max_overlap_total",
    required=False
)

parser.add_argument(
    "--tries",
    type=int,
    default=900,
    help="number of tries to generate non-overlapping text",
    required=False
)

parser.add_argument(
    "--min_words",
    type=int,
    default=3,
    help="minimum number of words",
    required=False
)

args = parser.parse_args()

if args.did != None and args.password == None:
    print("--pds and --password flags are required when --did is set")
    exit(-1)

if args.domain != None and args.token == None:
    print("--token flag is required when --domain is set")
    exit(-1)

model_f = open(args.model)
model = chain.Text.from_json(model_f.read())

generated = False
text = None

while not generated:
    text = model.make_short_sentence(args.max, max_overlap_total=args.overlap, tries=args.tries, min_words=args.min_words)
    generated = text is not None

text = text.replace('@','@​').replace('#','#​')
print(text)

# Fediverse posting code
if args.domain != None:
    resp = requests.post("https://" + args.domain + "/api/iceshrimp/notes", json={
        'visibility': 'home',
        'text': text,
        #'cw': 'gyattov generated text', # Ruben has Left His Mark # ruben, why
    }, headers={"Authorization": f"Bearer {args.token}"})

    if resp.status_code != 200:
        resp.raise_for_status()
        exit(-1)

# Bsky posting code
if args.did != None:
    pds_url = "https://" + args.pds
    session = requests.post(
        pds_url + "/xrpc/com.atproto.server.createSession",
        json={
            "identifier": args.did,
            "password": args.password,
        },
    )
    if session.status_code != 200:
        session.raise_for_status()
        exit(-1)
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
            "repo": args.did,
            "collection": "app.bsky.feed.post",
            "record": post,
        },
    )
    resp.raise_for_status()