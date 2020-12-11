import json

CACHE_PATH = './data/cache.txt'
RAW_RELATED_IDS = './data/related_ids_full.json'

def parse_cache(path = CACHE_PATH):
    """Parse the cache.txt file into a dictionary."""
    parsed = {}
    with open(path, 'r') as f:
        for row in f.readlines():
            key, val = row.strip('\n').split(": ")
            parsed[key] = eval(val)

    return parsed

if __name__ == "__main__":

    parsed = parse_cache()

    with open(RAW_RELATED_IDS, 'w') as f:
        json.dump(parsed, f)

# get related ids from first 70

# with open('data/related_ids_70.json') as f:
#     first_70 = json.load(f)

# # combine and save to related_ids.json
# next_half = parse_cache()

# first_half = {**first_70, **next_half}

# with open('data/related_ids.json', 'w') as f:
#     json.dump(first_half, f)

