import json
from webscrape import init_webdriver, get_all_related
# second pass through videos to fill out missing from first pass

# load related_ids.json

NEW_CACHE_LOCATION = "../data/second_cache.txt"
RELATED_IDS_LOC = "../data/related_ids_second_pass.json"

def parse_cache(path):
    """Parse the cache.txt file into a dictionary."""
    parsed = {}
    with open(path, 'r') as f:
        for row in f.readlines():
            key, val = row.strip('\n').split(": ")
            parsed[key] = eval(val)

    return parsed

def update_related_ids():

    second_pass = parse_cache(NEW_CACHE_LOCATION)

    with open("../data/related_ids.json", 'r') as f:
        related_ids = json.load(f)

    for k,v in related_ids.items():
        if len(second_pass.get(k, [])) > len(v):
            related_ids[k] = second_pass[k]

    with open(RELATED_IDS_LOC, 'w') as f:
        json.dump(related_ids, f)

if __name__ == "__main__":

    # get the names of the ids
    with open("../data/related_ids.json") as f:
        related_ids = json.load(f)

    # 122 with less than 40 related ids
    failed_ids = [key for key, val in related_ids.items() if len(val) < 40]

    driver = init_webdriver()

    all_related = get_all_related(failed_ids, driver, NEW_CACHE_LOCATION)

    with open(RELATED_IDS_LOC, 'w') as f:
        json.dump(all_related, f)

    update_related_ids()