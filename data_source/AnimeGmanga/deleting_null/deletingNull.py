import pandas as pd

pd=pd.read_json('AnimeGmanga_withnull.json', encoding='utf-8',orient = 'records')

pd.dropna(subset=['manga'], inplace=True)

pd.to_json('AnimeGmanga_withoutNull.json',orient = 'records',force_ascii=False,indent=4)