import pandas as pd

pd=pd.read_json('Anime1Gmanga.json', encoding='utf-8',orient = 'records')

pd.dropna(subset=['manga'], inplace=True)

pd.to_json('Anime1Gmanga1.json',orient = 'records',force_ascii=False,indent=4)