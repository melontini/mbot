import pandas as pd
import json

path = "data/"
file1 = input("first file mate: ")
file2 = input("second file mate: ")

json1 = pd.read_json(path + file1)
json2 = pd.read_json(path + file2)

combined = pd.concat([json1,json2])
columns = ["id","createdAt","fileIds","files","replyId","renoteId","poll","visibleUserIds","reactionAcceptance"]
combined = combined.drop(columns, axis=1)
combined = combined.replace("null", None)
combined = combined.drop_duplicates()

output = input('combined json filename please mate: ')

combined.to_json("data/" + output, index=False, orient="records")