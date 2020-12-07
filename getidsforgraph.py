import numpy as np
import codecs
import json
import csv

def write_ids_to_csv(filepath, save_to = "data/ids.csv"):
    """Get videoids from conspiracy_results.json file into csv."""

    with open(filepath) as f:
        data = json.load(f)

    keys = list(data['title'].keys())

    with open(save_to, 'w') as f:
        wr = csv.writer(f)
        wr.writerow(keys)

if __name__ == "__main__":

    filepath = 'data/conspiracy_results.json'

    write_ids_to_csv(filepath)