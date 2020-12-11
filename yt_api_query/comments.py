import json
from time import sleep
from datetime import datetime
from tqdm import tqdm
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from my_api_key import api_key

SOURCE_IDS_PATH = '../data/valid_ids.txt'
CACHE_LOCATION = '../data/comments_cache.txt'
RAW_COMMENTS = '../data/comments.json'

def setup_api(api_key):
    """Return the youtube api with my key."""

    api_service_name = "youtube"
    api_version = "v3"

    youtube = build(
            api_service_name, api_version, developerKey = api_key)

    return youtube

def parse_comments(response, query_date):
    """
    Parse response to comment query, extracting 
    comment text, like count, and reply count. query_date adds the time that the
    comment was requested to the comment dictionary.
    
    :param response: response object from Youtube v3 API commentThread().list() query
    
    return list of dictionaries each containing comment text, replies, and likes
    """

    # avoid KeyErrors with get
    threads = response.get('items', [{}])

    parsed_list = []
    for thread in threads:

        replies = thread.get('snippet', {}).get('totalReplyCount', 0)
        
        comment_info = thread.get('snippet', {}).get('topLevelComment', {})
        comment = comment_info.get('snippet', {}).get('textDisplay')
        likes = comment_info.get('snippet', {}).get('likeCount')
        name = comment_info.get('snippet', {}).get('authorDisplayName')

        # create dict with text, number of replies, and number of likes, and time of query
        comment_dict = {'name': name, 'text': comment, 
                        'replies': replies, 'likes': likes,
                        'query_date': query_date}

        parsed_list.append(comment_dict)

    return parsed_list

def get_comments(video_id, api, max_results = 100, max_requests = 1):
    """
    Get a list of top [max_results] comments for a given video.
    Returns a dictionary with video ids as keys and the unformatted responses as values.

    If the API returns an HttpError, the function will try again twice, pausing
    for two seconds each time. If the third try still returns an error, the function
    will assume that the quota has been reached and raise a Permission Error.

    :param video_id: A valid video_id string
    :param api: a built api on which commenThreads().list() can be called
    :param max_results: the maximum number of comment threads to return (default: 50)
    :param max_requests: limits the number of requests per video_id (default: 1)
    :return: a dictionary of video ids and response objects
    """

    comments = []
    nextPageToken = None
    num_requests = 0

    while len(comments) < max_results and num_requests < max_requests:

        request = api.commentThreads().list(
                    part="snippet",
                    order="relevance",
                    textFormat="plainText",
                    videoId= video_id,
                    pageToken = nextPageToken,
                    maxResults = 100
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
                if error.args[0].status == 404:
                    raise ValueError(f'Comments were disabled for {video_id}')
                # raise error if fails 3 times
                elif attempts >= 2:
                    raise PermissionError('API likely reached quota.')

                sleep(3)
                attempts += 1

        # record time of query, parse and add to comments
        query_date = str(datetime.now())
        parsed_response = parse_comments(response, query_date)
        comments.extend(parsed_response)

        # update the page token
        nextPageToken = response.get('nextPageToken', None)
        
        # break if no next page
        if nextPageToken is None:
            break
        
        num_requests += 1

    return comments

def get_all_comments(video_ids, api, max_results = 50, max_requests = 1):
    """Get all comments for a list of video ids, writing to a cache after each request."""
    
    all_comments = {}
    
    for id in tqdm(video_ids):
        # get related video ids

        try:
            comments = get_comments(id, api, 
                                    max_results = max_results, 
                                    max_requests = max_requests)

        # catch disabled comments error but allow PermissionError to stop requests
        except ValueError:
            print(f'Comments were disabled for {id}')
            comments = []

        with open(CACHE_LOCATION, 'a+') as f:
            f.write(f"{id}: {comments}\n")
    
        all_comments[id] = comments

        # try to avoid angering Youtube API
        sleep(0.1)
    
    return all_comments

if __name__ == "__main__":

    # build api
    youtube = setup_api(api_key())

    # load video_ids
    with open(SOURCE_IDS_PATH, 'r') as file:
        ids = file.readlines()[0].split(', ')

    # get all comments from videos in id list
    all_related = get_all_comments(ids, youtube)

    with open(RAW_COMMENTS, 'w') as f:
        json.dump(all_related, f)

