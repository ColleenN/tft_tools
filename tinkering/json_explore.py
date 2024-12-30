from data_io.tft import TFTSetBlob
from collections import defaultdict
from pprint import pprint

set_13_json = TFTSetBlob(13)
set_13_json.offline = True
units = set_13_json.get_base_unit_data()
roles = defaultdict()
roles.default_factory = lambda: list()
for x in units:
    roles[x['role']].append(x['name'])
#role_values = {x['role'] for x in units}

pprint(roles)

