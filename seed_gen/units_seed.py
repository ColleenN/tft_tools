from collections import OrderedDict
from seed_gen.base import TFTDataSeed, camel_to_snake
from copy import deepcopy

summon_units = {
    "TFT_TrainingDummy",
    "TFT_BlueGolem",
    "TFT14_SummonLevel2",
    "TFT14_SummonLevel4"
}


class TFTUnitSeed(TFTDataSeed):

    seed_name = "units"

    def _extract(self):
        return self.set_blob.data['champions']

    @staticmethod
    def _filter(raw_record):
        return len(raw_record['traits']) > 0 or raw_record["apiName"] in summon_units

    @staticmethod
    def _convert(raw_record):
        keys_to_keep = ["name", "apiName", "cost", "role"]
        base_dict = OrderedDict(
            {camel_to_snake(k): raw_record[k] for k in keys_to_keep})
        base_dict["shop_unit"] = len(raw_record['traits']) > 0
        flattened_stats = {
            f"stats_{camel_to_snake(k)}": v for k, v in raw_record['stats'].items()
        }
        base_dict.update(flattened_stats)
        return base_dict


class TFTUnitTraitSeed(TFTDataSeed):

    seed_name = "unit_innate_traits"

    def _extract(self):
        initial = self.set_blob.data['champions']
        records = []
        for champ in initial:
            for trait in champ['traits']:
                new_dict = deepcopy(champ)
                new_dict['single_trait_entry'] = trait
                records.append(new_dict)
        return records

    @staticmethod
    def _filter(raw_record):
        return len(raw_record['traits']) > 0

    @staticmethod
    def _convert(raw_record):
        fields = ['name', 'apiName', 'single_trait_entry']
        base = OrderedDict({camel_to_snake(k): raw_record[k] for k in fields})
        base['trait'] = base['single_trait_entry']
        del base['single_trait_entry']
        return base
