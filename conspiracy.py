import numpy as np
import codecs
import json

def load_json_files(file_path):

    '''
    Loads data from a json file

    Inputs:
        file_path   the path of the .json file that you want to read in

    Outputs:
        my_array    this is a numpy array if data is numeric, it's a list if it's a string

    '''

    #  load data from json file
    with codecs.open(file_path, 'r', encoding='utf-8') as handle:
        json_data = json.loads(handle.read())

    # if a string, then returns list of strings
    # if not isinstance(json_data[0], str):
    #     # otherwise, it's assumed to be numeric and returns numpy array
    #     json_data = np.array(json_data)

    return json_data

with open('conspiracy_results.json') as f:
    data = json.load(f)

# print(json.dumps(data, indent = 4, sort_keys=True))

# extract the video IDs the json files

keys = list(data['title'].keys())

import csv
with open('ids.csv', 'w') as f:
    wr = csv.writer(f)
    wr.writerow(keys)

import gdflib



