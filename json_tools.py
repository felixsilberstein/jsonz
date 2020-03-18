import json
from collections import defaultdict


def get_keys(d, class_mapping):
    if isinstance(d, dict):
        # print(d)
        # print('-'*80)
        # keys_list += dl.keys()
        
        _ = [class_mapping[k] for k in d.keys()]

        # print(class_mapping)
        for x in d.values():
            get_keys(x, class_mapping)
        # map(lambda x: get_keys(x, class_mapping), d.values())
    elif isinstance(d, list):
        for x in d:
            get_keys(x, class_mapping)
        # map(lambda x: get_keys(x, keys_list), dl)


def update_keys(d, class_mapping):
    if isinstance(d, dict):
        nd={}
        for ok, v in d.items():
            nv = update_keys(v, class_mapping)
            nk = class_mapping[ok]
            nd[nk] = nv

        # print(class_mapping)
        # for x in d.values():
            # get_keys(x, class_mapping)
        # map(lambda x: get_keys(x, class_mapping), d.values())
        return nd
    elif isinstance(d, list):
        nl = []
        for x in d:
            nl.append(update_keys(x, class_mapping))
        return nl
    else:
        return d

def compress_json(json_ref):
    '''
        reprocess the json as:
        {
            keys-dict:{
                "key1": 1,
                ...
                "key_n": index_n
                }
            json_obj: {
                "<key-dict[key_n]>": "value for key_n"
                ...
            }
        }
    '''
    class_mapping = defaultdict(int)
    class_mapping.default_factory = class_mapping.__len__

    with open(json_ref) as f:
        post_data = json.load(f)
    
    keys_dict = get_keys(post_data, class_mapping)
    # for k in post_data.keys():
        # print(k, class_mapping[k])
    # print(class_mapping)
    # print(len(class_mapping))
    nd = update_keys(post_data, class_mapping)
    with open('data/jsons/jsons/sample.jsonz', 'w') as f:
        json.dump(nd, f)


if __name__ == "__main__":
    json_ref='data/jsons/jsons/sample.json'
    compress_json(json_ref)