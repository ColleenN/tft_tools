from collections import OrderedDict
from json import dumps

from seed_gen.hash_constants import AUGMENT_HASH_MARKER
from seed_gen.base import TFTDataSeed


equippable_item_hashes = {
    'component',
    '{27557a09}',
    '{44ace175}',
    '{d304f83b}',
    '{7ea41d13}',
    '{6ef5c598}',
    '{ebcd1bac}',
    '{eda79d90}',
    '{218b53a5}'
}

non_equippable_item_hashes = {
    'Consumable',
    'TFT_Consumable_ItemRemover',
    'TFT_Consumable_ItemReroller',
    '{b4fe26c6}',
    '{fb608fdb}',
    '{56b1acc8}'
}

component_name_map = {
    'TFT_Item_BFSword': 'num_swords',
    'TFT_Item_ChainVest': 'num_vests',
    'TFT_Item_FryingPan': 'num_pans',
    'TFT_Item_GiantsBelt': 'num_belts',
    'TFT_Item_NeedlesslyLargeRod': 'num_rods',
    'TFT_Item_NegatronCloak': 'num_cloaks',
    'TFT_Item_RecurveBow': 'num_bows',
    'TFT_Item_SparringGloves': 'num_gloves',
    'TFT_Item_Spatula': 'num_spats',
    'TFT_Item_TearOfTheGoddess': 'num_tears',
}

flag_hashes = {
    'artifacts': '{44ace175}',
    'radiants': '{6ef5c598}',
    'supports': '{27557a09}',
    'emblems': '{ebcd1bac}',
    'components': 'component',
    'tg_items': '{218b53a5}',
    'tac_items': '{d304f83b}',
}


class TFTItemSeed(TFTDataSeed):
    seed_name = "items"

    def _extract(self):
        return self.set_blob.data_item_detail

    @staticmethod
    def _filter(raw_record):

        if AUGMENT_HASH_MARKER in raw_record['tags']:
            return False
        item_hash_set = set(raw_record['tags'])

        if item_hash_set & non_equippable_item_hashes:
            return False

        if 'Armory' in raw_record['apiName']:
            return False

        if item_hash_set & equippable_item_hashes:
            return True

        if 'CyberneticItem' in raw_record['apiName']:
            return True
        return False

    @staticmethod
    def _convert(raw_record):
        base = OrderedDict()
        base.update({
            'name': raw_record['name'],
            'api_name': raw_record['apiName'].upper(),
            'effects': dumps(raw_record['effects']),
            'trait_granted': raw_record['incompatibleTraits'][0] if raw_record[
                'incompatibleTraits'] else "",
            'unique': raw_record['unique']
        })
        base['num_craftables'] = 1 if raw_record['composition'] else 0

        for key, hash in flag_hashes.items():
            base[f"num_{key}"] = 1 if hash in raw_record['tags'] else 0

        component_map = {v: 0 for k, v in component_name_map.items()}
        if 'component' in raw_record['tags']:
            key_name = component_name_map[raw_record['apiName']]
            component_map[key_name] = 1
        else:
            for component in raw_record['composition']:
                key_name = component_name_map[component]
                component_map[key_name] = component_map[key_name] + 1
        base.update(component_map)

        return base