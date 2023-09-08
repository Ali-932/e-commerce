import pandas as pd


Gdata = pd.read_json('Gmanga_refined.json', encoding='utf-8',orient = 'records')

Gdata = Gdata[Gdata['manga'].apply(lambda x: len(x['volumes']) > 0)]

Gdata.to_json('Gmanga_refined_new.json',orient = 'records',force_ascii=False,indent=4)