import functools
import json

from data_io.gcp import read_from_bucket


@functools.lru_cache(maxsize=10)
def get_set_json(set_number):
    base = json.loads(read_from_bucket('tft_set_data', 'base_tft_json'))
    for item in base['setData']:
        if item['mutator'] == f'TFTSet{set_number}':
            return item

    raise ValueError('Set not found')


def get_unique_traits(set_number):
    base_json = get_set_json(set_number)
    unique_traits = []
    for trait in base_json['traits']:
        first_trait_tier = trait['effects'][0]
        if first_trait_tier['minUnits'] == 1 and first_trait_tier['maxUnits'] > 10:
            unique_traits.append(trait['name'])
    return unique_traits


def get_base_data(set_num):
    full_set_json = get_set_json(set_num)
    keys = {'name', 'traits', 'cost'}
    return_list = []
    for champ in full_set_json['champions']:
        if len(champ['traits']) > 0:
            return_list.append({k: v for k, v in champ.items() if k in keys})
    return return_list


COLOR_MAP = {
    1: '#BBBBBB',
    2: '#37D488',
    3: '#6ECCFF',
    4: '#DC38C3',
    5: '#F1C555'
}
