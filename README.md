# Conspiracy Video Analysis

## Introduction

Youtube is well-known to harbor a large repository of conspiratorial videos. Previous research has demonstrated that Youtube's efforts to remove these videos, while at times successful, have been insufficient to substantially reduce the influence of conspiracy thinking on the site. In this project, we attempt to pair existing data scoring Youtube videos for conspiratorial thinking with graph and NLP methods to gain more insight into how conspiracy videos are linked on Youtube.

## Data Collection

The two folders `yt_api_query` and `yt_scrape` both contains methods for collecting related video IDs for a set of Youtube videos. The former represents a failed bid that ran up against recently reduced request quotas for Youtube's v3 API. The latter implements a webscraping script that repeatedly loads Youtube video pages, scrolls down to load all recommended videos, and grabs all of the video links on the page. 

The workflow for the webscraping method was as follows:
* The data in `data/conspiracy_results.json` were parsed to extract video ids for further data gathering in `getidsforgraph.py`.
* The `yt_api_query/check_ids.py` file contains methods to check which of the videos from the original paper are still available.
* The `yt_scrape/webscrape.py` file implements the actual scraper using selenium. The script writes lines to `data/cache.txt` as it identifies related links for each video.
* The `yt_scrape/cache_parser.py` file provides a method to parse the cache and saves a json file (`data/related_ids.json`) for later use.
* The `preproc/crate_adj_matrix.py` script uses the json data to build an adjacency matrix by computing `1 / log(rank + 1)` for each video that occurs in another's related video list. Videos for which there was no match received a score of zero. The maximum score for related videos was 1.44, so the diagonal of the matrix was set to 2. The resulting matrix was saved to `data/adj_matrix.npy`