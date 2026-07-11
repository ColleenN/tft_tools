from pathlib import Path
import json
import bs4
import csv


REPLACE_MAP = {
    "magicdamage":"MAGIC DAMAGE",
    "physicaldamage":"PHYSICAL DAMAGE",
    "truedamage":"TRUE DAMAGE",
}

SCALING_MAP = {
    '(%i:scaleAP%)': '(AP SCALING)',
    '(%i:scaleHealth%)': '(HP SCALING)',
    '(%i:scaleAD%)': '(AD SCALING)',
    '(%i:scaleAP% %i:scaleHealth%)': '(AP + HP SCALING)',
    '(%i:scaleHealth% %i:scaleAP%)' : '(AP + HP SCALING)',
    '(%i:scaleHealth% %i:scaleAD%)': '(AD + HP SCALING)',
    '(%i:scaleAD% %i:scaleAP%)': '(AD + AP SCALING)',
    '(%i:scaleMR%)': '(MR SCALING)',
    '(%i:scaleArmor%)': '(ARMOR SCALING)',
    '(%i:scaleSoul%)': '(SOUL SCALING)',
    '(%i:scaleArmor% %i:scaleAP%)': '(ARMOR + AP SCALING)'
}


def transform_ability_html(bs_tag):

    for scaling_key, scaling_text_value in SCALING_MAP.items():
        if scaling_key in bs_tag.text:

            if bs_tag.name in REPLACE_MAP:
                descriptor = REPLACE_MAP[bs_tag.name]
                return f"{descriptor} {scaling_text_value}"
            return scaling_text_value

    if bs_tag.name == 'scalehealth':
        return '(HP SCALING)'
    if bs_tag.name == 'scalemana':
        return '(MANA REGEN SCALING)'
    if bs_tag.name == 'magicdamage':
        return 'FLAT MAGIC DAMAGE'

    if bs_tag.name in {'tftkeyword', 'tftbonus', 'br', 'truedamage'}:
        return tag.text.upper()

    return tag.text

    #return tag.text




with Path('../tactools_json_files/unit.json').open() as f:
    base = json.loads(f.read())

units = [v for k,v in base['units'].items()]
traits = base['traits']
tag_names = set()
for unit in units:
    ability_html = unit['ability']
    soup = bs4.BeautifulSoup(ability_html, 'html.parser')
    for tag in soup.find_all(True):
        new_text = transform_ability_html(tag)
        tag.replace_with(new_text)
    unit['ability'] = str(soup)

with Path('../tactools_json_files/unit.csv').open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=units[0].keys())
    writer.writeheader()
    writer.writerows(units)
