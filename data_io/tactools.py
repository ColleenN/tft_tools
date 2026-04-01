from data_io.tft import TFTSetBlob
import json
from pathlib import Path

class TacToolsBlob(TFTSetBlob):

    def __init__(self):
        super().__init__(set_num=13)

    def _load_data(self):
        with Path('../tactools_json_files/tactools_data.json').open() as f:
            base = json.loads(f.read())

            self._base = base
            self._item_data = base['items'] + base['augments']

    def get_emblem_list(self):
        emblem_list = []
        for item in self.data_item_detail:
            if item.get('isEmblem', False):
                emblem_list.append(item['apiName'])
        return emblem_list

    def _load_set_data_items(self, data_item_listing, set_data):
        raise NotImplemented