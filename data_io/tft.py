import functools
import json
from pathlib import Path


class TFTSetBlob:

    def __init__(self, set_num):
        self._set_num = set_num
        self.offline = False
        self._data = {}

    def _load_data(self):
        if not self.offline:
            from data_io.gcp import read_from_bucket
            base = json.loads(read_from_bucket('tft_set_data', 'base_tft_json'))
        else:
            with Path('../json_samples/en_us.json').open() as f:
                base = json.loads(f.read())
        for item in base['setData']:
            if item['mutator'] == f'TFTSet{self._set_num}':
                self._data = item
                return

        raise ValueError('Could not located requested set json')

    @property
    def data(self):
        if not self._data:
            self._load_data()
        return self._data

    def get_emblem_list(self):
        return [i_name for i_name in self.data['items'] if 'Emblem' in i_name]

    def get_unique_traits(self):
        unique_traits = []
        for trait in self.data['traits']:
            first_trait_tier = trait['effects'][0]
            if first_trait_tier['minUnits'] == 1 and first_trait_tier['maxUnits'] > 10:
                unique_traits.append((trait['name'], trait['apiName']))
        return unique_traits

    def get_base_unit_data(self):
        keys = {'name', 'traits', 'cost', 'role'}
        return_list = []
        for champ in self.data['champions']:
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
