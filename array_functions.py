def sortDictionary(dict):
    sorted_dict = {}
    sorted_keys = sorted(dict, key=dict.get, reverse=True)
    for value in sorted_keys:
        sorted_dict[value] = dict[value]
    return sorted_dict


def bubblyRadar(value):
    if value < 1:
        return "Bubblish"
    elif value >= 1 and value < 1.75:
        return "Bubblier"
    elif value >= 1.75 and value < 2.25:
        return "Bubbly"
    else:
        return "very close to Bubbliest"
