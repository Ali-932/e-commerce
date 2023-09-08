import base64
from pprint import pprint

import requests
import json
import pandas as pd
Api = 'https://api.mangadex.org/manga'
coverApi = 'https://api.mangadex.org/cover'
headers = {
    "Content-Type": "application/json"
}
content =[]
Gtitles = {}
Gmanga = pd.read_json('Anime1Gmanga2.json', encoding='utf-8',orient = 'records')
for manga in Gmanga['manga']:
    hasImageUrl = any('image_url' in volume for volume in manga['volumes'])
    if not hasImageUrl:
        if manga['start_date']:
            date = manga['start_date'].split('-')[0]
            print(manga['title'],date)
            Gtitles[(manga['title'])] = date
        else:
            Gtitles[(manga['title'])] = 0
print(Gtitles)
for title,year in Gtitles.items():
    t=0
    if year == 0:
        params = {'title': f'{title}'}
    else:
        params = {'title': f'{title}', 'year': f'{year}'}
    while True:
        print(params)
        response=requests.get(Api,headers=headers,params=params)
        if response.status_code == 200:
            # pprint(response.content)
            json_data = json.loads(response.content)
            json_data = json_data['data']
            if len(json_data) > 0:
                mangaOrCoverId = json_data[0]['id']
                break
            elif t == 0:
                modified_title = "".join(ch if ch.isalnum() else " " for ch in title)
                params = {'title': f'{modified_title}'}
                t+=1
                continue
            else:
                break
    params = {'manga[]': mangaOrCoverId, 'limit': 100}
    cover_response= requests.get(coverApi, headers=headers, params=params)
    if cover_response.status_code == 200:
        data = json.loads(cover_response.content)

        # Iterate over the data and save each image
        for item in data['data']:
            print(title,end='')
            print(f" volume {item['attributes']['volume']}")
            file_name = item['attributes']['fileName']
            imageUrl = f'https://uploads.mangadex.org/covers/{mangaOrCoverId}/{file_name}'
            print(imageUrl)
            if item['attributes']['volume'] == None:
                print("its none")
                for manga in Gmanga['manga']:
                    if manga['title'] == title:
                        for volume in manga['volumes']:
                            volume['image_url'] = imageUrl
                            Gmanga.to_json('Anime1Gmanga2.json', orient='records', force_ascii=False, indent=4)
                break
            for manga in Gmanga['manga']:
                if manga['title'] == title:
                    for volume in manga['volumes']:
                        if volume['volume'] == item['attributes']['volume']:
                            volume['image_url'] = imageUrl
                            # Gmanga.to_json('Anime1Gmanga2.json', orient='records', force_ascii=False, indent=4)

    else:
        print("Failed to create account. Error:", response.text)

