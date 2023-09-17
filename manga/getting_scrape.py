import requests
import json
import pandas as pd
Gtitles = {}
Gmanga = pd.read_json('Anime1Gmanga2.json', encoding='utf-8',orient = 'records')
for manga in Gmanga['manga']:
    hasImageUrl = any('image_url' in volume for volume in manga['volumes'])
    if not hasImageUrl:
        Gtitles[(manga['title'])] = []
        for manga1 in Gmanga['manga']:
            if manga1['title'] == manga['title']:
                for volume in manga['volumes']:
                    Gtitles[(manga['title'])].append(volume['volume'])

print(Gtitles)
Gtitles = pd.DataFrame.from_dict(Gtitles, orient='index')
print(Gtitles)
Gtitles.dropna()
Gtitles.to_json('need_scrape.json',orient='index', force_ascii=False, indent=4)
