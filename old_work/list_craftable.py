from pprint import pformat
import json


def current_set_condition(item_entry):
    return (
        item_entry['composition'] and
        (item_entry['apiName'].startswith('TFT_Item')
        or item_entry['apiName'].startswith('TFT9'))
    )


with open("../json_samples/en_us.json") as src_data:
    as_json = json.loads(src_data.read())

craftables = [x for x in as_json['items'] if current_set_condition(x)]

for item in craftables:
    print(item['name'])
