import json
import pandas as pd
from googleapiclient.discovery import build
from my_api_key import api_key
from time import sleep
from tqdm import tqdm

def check_ids(ids):
    """Query youtube api with list of ids and return subset for which youtube returns a result."""
    
    # break ids list into chunks to avoid angering youtube api
    chunks = [ids[i:i + 50] for i in range(0, len(ids), 50)] 
    
    # create chunks of comma separated strings of ids for query
    chunks = [",".join(chunk) for chunk in chunks]
    
    api_service_name = "youtube"
    api_version = "v3"
    developer_key = api_key()

    # Get credentials and create an API client
    youtube = build(
        api_service_name, api_version, developerKey = developer_key)

    # for each chunk, make a request 
    valid_ids = []
    responses = {}
    idx = 0 # not enumerate so that tqdm will show a bar
    for chunk in tqdm(chunks):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=chunk
        )

        response = request.execute()
        # get valid ids
        valid = [response['items'][i]['id'] for i in range(len(response['items']))]
        valid_ids.extend(valid)
        responses[f"Query {idx}"] = response
        # sleep(0.1)
        idx += 1

    return valid_ids, responses

if __name__ == "__main__":

    ids = pd.read_csv('ids.csv').columns.to_list()

    valid_ids, responses = check_ids(ids)

    print(f'There were {len(valid_ids)} valid ids. Saving results to files.')
    
    # write valid_ids to csv
    with open('valid_ids.txt', 'w') as f:
        f.write(", ".join(valid_ids))
    
    # write all response data to json
    with open('response_data.json', 'w') as f:
        json.dump(responses, f)