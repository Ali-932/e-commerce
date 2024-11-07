import pandas as pd

Gdata = pd.read_json('g-manga_structured.json', encoding='utf-8', orient='records')

Gdata = Gdata[Gdata['manga'].apply(lambda x: len(x['volumes']) > 0)]

Gdata.to_json('g-manga_nonzero_vols.json', orient='records', force_ascii=False, indent=4)
