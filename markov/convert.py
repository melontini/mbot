import pandas as pd
import json

path = "data/"
filename = input("What is the file called? ")

with open(path + filename) as json_data:
    dataset = json.load(json_data)


print("converting to misskey format")

for i, post in enumerate(dataset['orderedItems']):

    print(dataset['orderedItems'][i]["object"]["content"])


print("dropping duplicate entries")
