import json
import csv

ALL_IDS = './data/ids.csv'
DATA_SOURCE = './data/conspiracy_results.json'

def write_ids_to_csv(filepath, save_to = ALL_IDS):
    """Get videoids from conspiracy_results.json file into csv."""

    with open(filepath) as f:
        data = json.load(f)

    keys = list(data['title'].keys())

    with open(save_to, 'w') as f:
        wr = csv.writer(f)
        wr.writerow(keys)

if __name__ == "__main__":

    write_ids_to_csv(DATA_SOURCE)