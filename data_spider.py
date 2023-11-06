import requests
import json
from jinja2 import Environment, FileSystemLoader

def query_api(target_champs):

    output = []

    for unit in target_champs:
        response = requests.get(
            f"https://d2.tft.tools/explorer-data/13211/1/u-{unit['apiName']}-3")

        if response.status_code == 200:
            data = json.loads(response.content)['base']
        else:
            data = {'count': 0, 'place': 0, 'top4': 0, 'won': 0}

        data['name'] = unit['name']
        output.append(data)

    return output


def get_target_units():

    with open('set9.json') as data_file:
        set_data = json.loads(data_file.read())

    return_dict = {"1": [], "2": [], "3": []}

    for item in set_data['champions']:

        if str(item['cost']) in return_dict.keys() and item['traits']:
            return_dict[str(item['cost'])].append(
                {'name': item['name'], 'apiName': item['apiName']})

    return return_dict


def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/sandboxba09b239cce44d76848ac891d99b50ac.mailgun.org/messages",
        auth=("api", "5701f6454d185374ef65658d1c98b46a-3750a53b-ba57f06c"),
        data={"from": "Excited User <mailgun@sandboxba09b239cce44d76848ac891d99b50ac.mailgun.org>",
            "to": ["colleenfnelson@gmail.com"],
            "subject": "Hello",
            "text": "Testing some Mailgun awesomeness!"}
    )


def calc_stats(entry):
    return {
        'name': entry['name'],
        'count': entry['count'],
        'avp': entry['place']/entry['count'] if entry['count'] else 0,
        'top4': entry['top4']/entry['count'] if entry['count'] else 0,
        'won': entry['won']/entry['count'] if entry['count'] else 0
    }


unit_list = get_target_units()
unit_stats = {
    "one_cost": [calc_stats(x) for x in query_api(unit_list["1"])],
    "two_cost": [calc_stats(x) for x in query_api(unit_list["2"])],
    "three_cost": [calc_stats(x) for x in query_api(unit_list["3"])]
}

template_env = Environment(loader=FileSystemLoader('D:/TFT_Data'))
email_template = template_env.get_template('email_template.html')
with open('results.html', mode="w", encoding="utf-8") as results:
    results.write(email_template.render({'units': unit_stats}))
