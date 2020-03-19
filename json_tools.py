import json
from collections import defaultdict
import sys
import os
from pprint import pprint

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
        return nd
    elif isinstance(d, list):
        nl = []
        for x in d:
            nl.append(update_keys(x, class_mapping))
        return nl
    else:
        return d

def reverse_update_keys(d, class_mapping):
    ''' Bcz json allows only strings as keys
    '''
    if isinstance(d, dict):
        nd={}
        for ok, v in d.items():
            nv = reverse_update_keys(v, class_mapping)
            nk = class_mapping[int(ok)]
            nd[nk] = nv
        return nd
    elif isinstance(d, list):
        nl = []
        for x in d:
            nl.append(reverse_update_keys(x, class_mapping))
        return nl
    else:
        return d

def compress(json_path):
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

    with open(json_path) as f:
        json_data = json.load(f)
    
    keys_dict = get_keys(json_data, class_mapping)
    # for k in json_data.keys():
        # print(k, class_mapping[k])
    # print(class_mapping)
    # print(len(class_mapping))
    nd = update_keys(json_data, class_mapping)
    nj = {
        "keys_map": class_mapping,
        "json": nd
    }
    json_path_dir = os.path.dirname(os.path.realpath(json_path))
    filename, file_extension = os.path.splitext(json_path)
    jsonz_path = os.path.join(json_path_dir, filename + '.jsonz')
    # print(jsonz_path)
    with open(jsonz_path, 'w') as f:
        json.dump(nj, f)
    return jsonz_path

def uncompress(jsonz_path):
    with open(jsonz_path) as f:
        jsonz_data = json.load(f)
    
    keys_dict = jsonz_data['keys_map']
    inv_keys_dict = {v: k for k, v in keys_dict.items()}
    json_data = reverse_update_keys(jsonz_data['json'], inv_keys_dict)

    json_path_dir = os.path.dirname(os.path.realpath(jsonz_path))
    filename, file_extension = os.path.splitext(jsonz_path)
    jsonuz_path = os.path.join(json_path_dir, filename + '-uz.json')
    # print(jsonz_path)
    with open(jsonuz_path, 'w') as f:
        json.dump(json_data, f)
    return jsonuz_path


if __name__ == "__main__":
    if len(sys.argv) == 3:
        # print(sys.argv)
        # json_ref='data/jsons/jsons/sample.json'
        if sys.argv[1] == '-z':
            compress(sys.argv[2])
        elif sys.argv[1] == '-u':
            uncompress(sys.argv[2])

