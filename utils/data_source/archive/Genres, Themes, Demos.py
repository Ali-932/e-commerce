import ast

import pandas as pd

data = pd.read_json('Anime1Gmanga3.json')

genres=set()
themes=set()
demographics=set()

for i in data['manga']:
    for j in ast.literal_eval(i['demographics']):
        demographics.add(j)
print(demographics)
