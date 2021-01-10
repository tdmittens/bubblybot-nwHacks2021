def sortDictionary(dict):
    sorted_dict = {}
    sorted_keys = sorted(dict, key=dict.get, reverse=True)
    for value in sorted_keys:
        sorted_dict[value] = dict[value]
    return sorted_dict
