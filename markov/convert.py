import json

path = "data/"
filename = input("What is the file called? ")

with open(path + filename) as json_data:
    dataset = json.load(json_data)


print("converting to misskey format")

final = []

# idgaf if there's a more efficient way . 
for i, post in enumerate(dataset['orderedItems']):
    if dataset['orderedItems'][i]["type"] == "Create":
        if dataset['orderedItems'][i]["object"]["summary"] == "null":
            cw = null
        else:
            cw = json.dumps(dataset['orderedItems'][i]["object"]["summary"]) 
        # Strips out follower-only posts
        if dataset['orderedItems'][i]["object"]["to"] == ["https://wetdry.world/users/torepang/followers"] and dataset['orderedItems'][i]["object"]["cc"] == []:
            continue
        else:
            content = json.dumps(dataset['orderedItems'][i]["object"]["content"]) 
    else:
        continue
    post = {
        "text": content,
        "cw": cw,
        "visibility": "public",
        "localOnly": False
    }
    final.append(post)

output_filename = input("output filename? ")
with open(output_filename + ".json", "w") as f:
    json.dump(final, f)

print( "done mate  have a cuppa on me mate ")