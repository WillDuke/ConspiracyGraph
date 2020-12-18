import json
from check_ids import check_ids
from my_api_key import api_key
from comments import get_all_comments, setup_api

# with open('../data/training_set.json') as f:
#     train = json.load(f)

# ## extract ids
# ids = list(train['title'].keys())

# # get valid ids via api query
# valid_training_ids, responses = check_ids(ids)

# # write valid_ids to csv
# with open('../data/training_valid_ids.txt', 'w') as f:
#     f.write(", ".join(valid_training_ids))

# # write all response data to json
# with open('../data/training_response_data.json', 'w') as f:
#     json.dump(responses, f)

# # crosscheck new ids with valid_ids
# with open('../data/valid_ids.txt', 'r') as f:
#     valid_ids = f.readlines()[0].split(', ')

# # 179 of 898 training ids are in the original data
# print(len([i for i in valid_training_ids if i in valid_ids]))


# getting the new comments
CACHE_LOCATION = "../data/training_comments_cache.txt"

with open('../data/training_valid_ids.txt') as f:
    training_ids = f.readlines()[0].split(', ')

# get comments from the Google API for the training_ids 
# (decided to get all so that they would be pulled at the same time)
youtube = setup_api(api_key())
all_related = get_all_comments(training_ids, youtube, 
                                cache = CACHE_LOCATION)

with open('../data/training_comments.json', 'w') as f:
    json.dump(all_related, f)

# back-up procedure for when above inexplicably fails
# def parse_comments_cache(path):

#     comments = {}
#     with open(path, 'r') as f:
#         for row in f.readlines():
#             key, val = row.split(": ", 1)
#             comments[key] = eval(val)
    
#     return comments

# all_related = parse_comments_cache(CACHE_LOCATION)


