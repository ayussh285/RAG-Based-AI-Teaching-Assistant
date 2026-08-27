import requests
import os
import json
import pandas as pd
# from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib

def create_embedding(text_list):
    r= requests.post("http://localhost:11434/api/embed" , json ={
        "model":"bge-m3",
        "input":  text_list
    })

    embedding = r.json()['embeddings']
    return embedding

jsons = os.listdir("newjsons")
my_dict = []
chunk_id = 0

for json_file in jsons:
    with open (f"newjsons/{json_file}") as f:
        content = json.load(f)
    print(f"Creating embeddings for {json_file}")
    embeddings = create_embedding([c['text'] for c in content['chunks']])
    i=0
    for chunk in (content['chunks']):
        # print(chunk)
        chunk['chunk_id'] = chunk_id
        chunk['embedding'] = embeddings[i]
        i+=1
        chunk_id+=1
        my_dict.append(chunk)

# print(my_dict)
df = pd.DataFrame.from_records(my_dict)
# print(df)
joblib.dump(df, 'embeddings.joblib')

