import httpx
import json
from data_io.tft import TFTSetBlob
from pprint import pprint


url = "https://d2.tft.tools/combos/explorer/1100/15020/2"

set_data = TFTSetBlob(13)

emblem_filter = []
for name in set_data.get_emblem_list():
    emblem_filter.append(
        {
            "typ": "i",
            "value": name,
            "exclude": True
        }
    )


payload = json.dumps({
    "uid": "9c0d2242-f73c-40dd-b1dd-4364ccb76d66",
    "filters": emblem_filter,
})
headers = {
    'Content-Type': 'application/json'
}

response = httpx.post(url, headers=headers, data=payload)
#response = httpx.get("https://api.tft.tools/match/EUN1_3684035983")

data = json.loads(response.content)
#print(pformat(data["info"]["participants"][1]))
#print(pformat(data['matches'][0]))

#pprint(data['traits'])
processed = sorted(data['traits'], key=lambda t: t[2]['delta'])
uniques = [x[1] for x in set_data.get_unique_traits()]
final = []
for item in processed:

    if item[0] in uniques or item[2]['count'] < 3000:
        continue

    final_dict = item[2]
    final_dict['Trait_Name'] = item[0]
    final_dict['Trait_Tier'] = item[1]
    final.append(final_dict)

pprint(final, width=500)
