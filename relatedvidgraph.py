import json
from time import sleep
from tqdm import tqdm
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from my_api_key import api_key

SOURCE_IDS_PATH = 'data/valid_ids.txt'
CACHE_LOCATION = 'data/cache.json'
RAW_RELATED_IDS = 'data/related_ids.json'

def setup_api():
    """Return the youtube api with my key."""

    api_service_name = "youtube"
    api_version = "v3"
    developer_key = api_key()

    youtube = build(
            api_service_name, api_version, developerKey = developer_key)

    return youtube

def get_related_ids(video_id, api, max_results = 200):
    """
    Get a list of top [max_results] related video ids for a given video.
    Returns all related videos if total is less than max_results.

    If the API returns an HttpError, the function will try again twice, pausing
    for two seconds each time. If the third try still returns an error, the function
    will assume that the quota has been reached and raise a Permission Error.

    :param video_id: A valid video_id string
    :param api: a built api on which search() can be called
    :param max_results: the maximum number of related video ids to return 
    :return: a list of video ids related to supplied video_id 
    """

    related_vids = []
    nextPageToken = None

    while len(related_vids) < max_results:

        request = api.search().list(
                        part = "snippet",
                        type = "video",
                        relatedToVideoId = video_id,
                        maxResults = 50,
                        pageToken = nextPageToken
                    )

        response = None
        failed = True
        attempts = 0
        
        while failed:
            # request api for page of max 50 results
            try:
                response = request.execute()
                failed = False

            except HttpError as error:
                # raise error if fails 3 times
                print(error)
                if attempts >= 2:
                    raise PermissionError('API likely reached quota.')

                sleep(2)
                attempts += 1
        
        # get related video ids and add to list
        rel_vids_page = [item['id']['videoId'] for item in response['items']]
        related_vids.extend(rel_vids_page)

        # update the page token
        nextPageToken = response.get('nextPageToken', None)
        
        # break if no next page
        if nextPageToken is None:
            break

    return related_vids

def get_all_related(video_ids, api, max_results = 200):
    """Get all of the related ids, dumping to a json cache if there is an API error."""
    cache = {}

    for id in tqdm(video_ids):
        # get related video ids
        try:
            related_ids = get_related_ids(id, api, max_results = max_results)
            cache[id] = related_ids
        except:
            with open(CACHE_LOCATION, 'w') as file:
                json.dump(cache, file)
            for _ in tqdm(range(1200)): # wait a day
                sleep(60)

    return cache

if __name__ == "__main__":

    # build api
    youtube = setup_api()

    # load video_ids
    with open(SOURCE_IDS_PATH, 'r') as file:
        ids = file.readlines()[0].split(', ')

    # create the matrix and dump to pkl file
    all_related = get_all_related(ids, youtube)

    with open(RAW_RELATED_IDS, 'w') as file:
        json.dump(all_related, file) 


