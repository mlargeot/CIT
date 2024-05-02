def list_to_dict(items: list) -> dict:
    dict_items = {}
    i = 0
    for item in items:
        dict_items[i] = dict(item)
        i = i + 1
    return dict_items
