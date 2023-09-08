import csv
import pandas as pd


df=pd.read_csv('manga.csv', encoding='utf-8')
filtered_manga = df[df['score']>0]
print(filtered_manga.to_dict(orient='records'))
columns=['title', 'type', 'status', 'volumes', 'chapters', 'start_date', 'end_date', 'favorites', 'genres', 'themes','demographics','authors',
         'synopsis','background','main_picture','score','title_japanese','title_english','title_synonyms',]
filtered_manga=filtered_manga.loc[:,columns]
filtered_manga=filtered_manga.sort_values(by='score', ascending=False)
# print(filtered_manga.to_json(orient='records', force_ascii=False, indent=4))

with open('manga2.json', 'w', encoding='utf-8') as f:
    f.write(filtered_manga.to_json(orient='records', force_ascii=False, indent=4))
