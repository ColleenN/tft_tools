import json

from seed_gen.hash_constants import *
from data_io.tft import TFTSetBlob
from pathlib import Path
from pprint import pformat


def is_augment(item):
    return (
        AUGMENT_HASH_MARKER in item['tags'] and
        len(set(item['tags']) & {SILVER_AUGMENT, GOLD_AUGMENT, PRISMATIC_AUGMENT}) == 1
    )

#json14 = TFTSetBlob().data

with Path('../json_samples/en_us.json').open(encoding='utf-8') as f:
    base = json.loads(f.read())

item_hashes = {
    'artifacts': '{44ace175}',
    'radiants': '{6ef5c598}',
    'supports': '{27557a09}',
    'emblems': '{ebcd1bac}',
    'components': 'component',
    'tg_items': '{218b53a5}',
    'tac_items': '{d304f83b}',
}



TG_ITEM_HASH = '{218b53a5}'
TAC_ITEM_HASH = '{d304f83b}'
RADIANT_ITEM_HASH = '{6ef5c598}'
ARTIFACT_ITEM_HASH = '{44ace175}'
EMBLEM_ITEM_HASH = '{ebcd1bac}'
CRAFTABLE_ITEM_HASH = '{7ea41d13}'

tg_items = []
emblems = []
craftables = []
radiants = []
artifacts = []
tac_items = []

for item_record in base['items']:

    if TG_ITEM_HASH in item_record['tags']:
        tg_items.append(item_record['apiName'])


    if (
        EMBLEM_ITEM_HASH in item_record['tags']
    ):
        emblems.append(item_record['apiName'])
    elif (
        RADIANT_ITEM_HASH in item_record['tags']
        and not EMBLEM_ITEM_HASH in item_record['tags']
        and item_record['name'].startswith('Radiant')
    ):
        radiants.append(item_record['apiName'])
    elif ARTIFACT_ITEM_HASH in item_record['tags']:
        artifacts.append(item_record['apiName'])
    elif TAC_ITEM_HASH in item_record['tags']:
        tac_items.append(item_record['apiName'])
    elif CRAFTABLE_ITEM_HASH in item_record['tags'] and item_record['composition']:
        craftables.append(item_record['apiName'])

