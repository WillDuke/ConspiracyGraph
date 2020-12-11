import json
from yt_scrape.webscrape import init_webdriver, get_all_related
# second pass through videos to fill out missing from first pass

# load related_ids.json

NEW_CACHE_LOCATION = "..data/second_cache.txt"
RELATED_IDS_LOC = "../data/related_ids_second_pass.json"


if __name__ == "__main__":

    # get the names of the ids
    with open("../data/related_ids.json") as f:
        related_ids = json.load(f)

    # 122 with less than 40 related ids
    failed_ids = [key for key, val in related_ids.items() if len(val) < 40]

    driver = init_webdriver()

    all_related = get_all_related(failed_ids, driver, NEW_CACHE_LOCATION)

    with open(RELATED_IDS_LOC) as f:
        json.dump(all_related, f)