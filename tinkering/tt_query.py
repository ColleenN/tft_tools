import httpx
import json
from pprint import pformat

url = "https://d2.tft.tools/combos/explorer/1100/14210/1"

payload = json.dumps({
  "uid": "9c0d2242-f73c-40dd-b1dd-4364ccb76d66",
  "filters": [
    {
      "typ": "u",
      "value": "TFT12_Blitzcrank",
      "tier": "2",
      "itemCount": "3",
      "exclude": False
    }
  ]
})
headers = {
  'Content-Type': 'application/json'
}

#response = httpx.post(url, headers=headers, data=payload)
response = httpx.get("https://api.tft.tools/match/EUN1_3684035983")



data = json.loads(response.content)
print(pformat(data["info"]["participants"][1]))


#print(pformat(data['matches'][0]))

