from collections import OrderedDict
from seed_gen.base import TFTDataSeed, camel_to_snake
from copy import deepcopy

icon_style_map = {
    1: "BRONZE",
    3: "SILVER",
    4: "LEGENDARY",
    5: "GOLD",
    6: "PRISMATIC"
}

class TFTTraitTiersSeed(TFTDataSeed):

    seed_name = "trait_tiers"

    def _extract(self):
        initial = self.set_blob.data['traits']
        records = []
        for trait in initial:
            for level in trait['effects']:
                new_dict = deepcopy(trait)
                new_dict['tier_effect'] = level
                records.append(new_dict)
        return records

    @staticmethod
    def _filter(raw_record):
        return True

    @staticmethod
    def _convert(raw_record):

        base = OrderedDict({
            'name': raw_record['name'],
            'api_name': raw_record['apiName'].upper()
        })
        base['type'] = icon_style_map[raw_record['tier_effect']['style']]
        effect_fields = OrderedDict(
            {f"tier_{camel_to_snake(k)}": v for k, v in raw_record['tier_effect'].items()})
        base.update(effect_fields)
        base['desc'] = raw_record['desc']
        return base