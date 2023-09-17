from pprint import pprint

import pandas as pd
import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from translatepy import Translator

translator = Translator()
# try:
Gdata = pd.read_json('Anime1Gmanga3.json', encoding='utf-8',orient = 'records')
Adata = pd.read_json('manga2.json', encoding='utf-8',orient = 'records')
# Gdata = Gdata[Gdata['manga'].apply(lambda x: len(x['volumes']) > 0)]

titles1=list(Gdata['manga'])
# titles2 = Adata.to_dict(orient='records')
titles2=list(Adata['title'])
# pprint(titles2[:2])
# pprint(titles1[:2])
similar_titles = []
similarity_threshold = 85
merge_result = []
Adata=Adata.to_dict(orient='records')
for title1 in titles1:
    best_match = process.extractOne(title1['title'], titles2, scorer=fuzz.ratio)
    if best_match[1] >= similarity_threshold:
        # print(title1['title'],best_match[0], best_match[1])
        filtered_items = [
            item
            for item in Adata
            if item['title'] == best_match[0]
            and item['type'] in ['manga', 'one_shot']
        ]
        # print(filtered_items)
        if filtered_items.__len__()==0:
            for index, manga in Gdata['manga'].items():
                if type(manga) is not dict:
                    continue
                if manga['title'] == title1['title']:
                    # print('found', manga)
                    Gdata['manga'] = Gdata['manga'].drop(index)
                    break
            continue
        # print(filtered_items[0]['title'])
        for manga in Gdata['manga']:
            if type(manga) is not dict:
                continue
            if manga['title'] == title1['title']:
                filtered_items[0]['synopsis']=str(translator.translate(manga['synopsis'],'arabic')) if manga['synopsis'] else None
                filtered_items[0]['background']=str(translator.translate(manga['background'],'arabic')) if manga['background'] else None
                authors=eval(filtered_items[0]['authors'])
                for i in authors:
                    i['role'] = str(translator.translate(i['role'],'arabic')) if i['role'] else None
                filtered_items[0]['authors']=str(authors)
                info = (
                    {}
                    | {
                        key: value
                        for key, value in filtered_items[0].items()
                        if key != 'volumes'
                    }
                    if filtered_items
                    else {}
                )
                for key in list(info.keys()):
                    manga[key]=info[key]
    else:
        # print('not found',title1)
        for index, manga in Gdata['manga'].items():
            if type(manga) is not dict:
                continue
            if manga['title'] == title1['title']:
                # print('found',manga)
                Gdata['manga'] = Gdata['manga'].drop(index)
                break

Gdata.to_json('Anime1Gmanga0.json',orient='records', force_ascii=False, indent=4)
