from collections import OrderedDict
from json import dumps
from seed_gen.base import TFTDataSeed

summon_units = {
    "TFT_TrainingDummy",
    "TFT_BlueGolem",
    "TFT14_SummonLevel2",
    "TFT14_SummonLevel4"
}

def camel_to_snake(some_str):

    new_str = ""
    for char in some_str:
        if char.isupper():
            new_str += "_" + char.lower()
        else:
            new_str += char
    return new_str


class TFTUnitSeed(TFTDataSeed):

    seed_name = "units"

    def _extract(self):
        return self.set_blob.data['champions']

    @staticmethod
    def _filter(raw_record):
        return len(raw_record['traits']) > 0 or raw_record["apiName"] in summon_units

    @staticmethod
    def _convert(raw_record):
        keys_to_keep = ["name", "apiName", "cost", "traits", "role"]
        base_dict = OrderedDict(
            {camel_to_snake(k): raw_record[k] for k in keys_to_keep})
        base_dict["shop_unit"] = len(raw_record['traits']) > 0
        base_dict["traits"] = dumps(base_dict["traits"])
        flattened_stats = {
            f"stats_{camel_to_snake(k)}": v for k, v in raw_record['stats'].items()
        }
        base_dict.update(flattened_stats)
        return base_dict
