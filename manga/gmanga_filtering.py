import pandas as pd
import json
with open('manga_data.json','r',encoding='utf-8') as f:
    data = json.loads(f.read())
#
converted_data=[]
for title,  chapters in data.items():
    volumes  =  set()
    volumes_with_chapters={}
    for  chapter  in  chapters:
        volume_num  =  chapter["title"].split()[0].split(".")[1]
        volumes.add(volume_num)
        value=chapter["title"].split()[1].split(".")[1]
        if volume_num not in volumes_with_chapters:
            volumes_with_chapters[volume_num] = set()
        volumes_with_chapters[volume_num].add(int(value))

    sorted_dict = dict(sorted(volumes_with_chapters.items(), key=lambda x: float(x[0])))
    if '0' in sorted_dict:
        sorted_dict.pop('0')

    converted_data.append(
        {
            "manga": {
                "title": title,
                "volumes": [
                    {
                        "volume": volume,
                        "start_chapter": min(sorted_dict[volume]),
                        "end_chapter": max(sorted_dict[volume]),
                    }
                    for volume in sorted_dict
                ],
            }
        }
    )


#  Convert  converted_data  to  JSON  string
json_string  =  json.dumps(converted_data)
with open('Gmanga_refined.json','w') as f:
    json.dump(converted_data,f,indent=4)
