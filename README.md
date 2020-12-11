# Conspiracy Video Analysis

## Introduction

Youtube is well-known to harbor a large repository of conspiratorial videos. Previous research has demonstrated that Youtube's efforts to remove these videos, while at times successful, have been insufficient to substantially reduce the influence of conspiracy thinking on the site. In this project, we attempt to pair existing data scoring Youtube videos for conspiratorial thinking with graph and NLP methods to gain more insight into how conspiracy videos are linked on Youtube.

## Data Collection

The two folders `yt_api_query` and `yt_scrape` both contain methods for collecting related video IDs for a set of Youtube videos. The former contains methods for checking whether video IDs are available in the API, downloading and parsing comments for a list of videos, and download lists of video recommendations (though this last method was not used due to API request quotas restraints). The latter implements a webscraping script that repeatedly loads Youtube video pages, scrolls down to load all recommended videos, and grabs all of the video links on the page. 

The workflow for the webscraping method was as follows:
* The data in `data/conspiracy_results.json` were parsed to extract video ids for further data gathering in `getidsforgraph.py`.
* The `yt_api_query/check_ids.py` file contains methods to check which of the videos from the original paper are still available.
* The `yt_scrape/webscrape.py` file implements the actual scraper using selenium. The script writes lines to `data/cache.txt` as it identifies related links for each video.
* The initial pass retrieved very few related video IDs for some of the videos in our data set, so `second_pass.py` implements a method to find IDs in the first pass with less than 40 recommendations and re-runs the scraping script for those.
* The `yt_scrape/cache_parser.py` file provides a method to parse the cache and saves a json file (`data/related_ids.json`) for later use.

## Data Preprocessing

With the goal of applying graph-based methods to these data, we transformed the original data and the results of the webscraping as follows:
* The `preproc/crate_adj_matrix.py` script uses the json data to build an adjacency matrix by computing `1 / log(rank + 1)` for each video that occurs in another's related video list. Videos for which there was no match received a score of zero. The resulting matrix was then added to its transpose to create a symmetric distance measure. The maximum score for related videos was 1.44, so the diagonal of the matrix was set to 2. The resulting matrix was saved to `data/adj_matrix.npz`
* Due to the sparsity of the adjacency matrix built using this method, the log-rank score was supplemented with a score reflecting the number of matching tags that two videos shared via the `prepoc/boost_adj.py` file.

To create a feature space for our video sets, we created separate corpora for different features of the videos:
* Comments were retrieved via the Youtube API using methods in `yt_api_query/comments.py`, which pull the top 100 comments and save the author's name, the comment text, the number of replies, the number of likes, and the time that the comment was queried from the API.
* Text data from the video titles, descriptions, and comments were vectorized using `sklearn`'s `CountVectorizer` in `baggify.py`.
