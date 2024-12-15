




def query_explorer(
    item_include_filter: list = None,
    item_exclude_filter: list = None,
    unit_include_filter: list = None,
    unit_exclude_filter: list = None
):
    filters = prep_filter(item_include_filter, item_exclude_filter, unit_include_filter, unit_exclude_filter)


def prep_filter(
    item_include_filter: list[str] = None,
    item_exclude_filter: list = None,
    unit_include_filter: list = None,
    unit_exclude_filter: list = None
):
    filter_list = []

    for item in item_include_filter:
        filter_list.append({"typ": "i", "value": item, "exclude": True})

    for item in item_exclude_filter:
        filter_list.append({"typ": "i", "value": item, "exclude": False})

    for item in unit_include_filter:
        filter_list.append({"typ": "i", "value": item, "exclude": True})

    return filter_list