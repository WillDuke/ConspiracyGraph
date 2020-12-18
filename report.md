# Mapping Conspiracy Trajectories on Youtube

Notes:

- 3-5 pages, include appropriate visuals to display reults and method

## Introduction

 Youtube automatically recommends videos in large part based on engagement metrics that are agnostic to video quality. This practice has drawn criticism for its potential to expose users to conspiracy theories and other spurious claims.[^1]  In response, Youtube has employed content moderators and automated moderating techniques to remove the most egregious conspiracy content from their recommendations, some of which had drawn hundreds of thousands of views.[^2] A longitudinal study tracking conspiracy videos on Youtube over a 16 month period found that the company’s efforts to demote offending channels had been effective, though the prevalence of conspiracy videos on the site remained relatively high.[^3]

The authors of the conspiracy study made some of their data publicly available, including the results of manual scoring for hundreds of videos on whether they contained conspiracy content.[^4] For this project, we attempted to recreate their logistic regression model which classified videos by whether they contained significant conspiracy content. We applied unsupervised learning methods to identify patterns and characterize the major groupings in the data. 

## Background

## Related Work

## Methods & Theory

### Data Collection 

The publicly available data from Faddoul et al.'s work identifying conspiracy videos contained video IDs, titles, descriptions, comment counts, and conspiracy likelihood scores. A separate set of data contained a smaller number of videos with manually scored labels indicating whether the video contained conspiracy content. 

We initially sought to supplement this data with a distance matrix developed by scoring each video in the original dataset on whether and where they occured in the recommended videos of each of the other videos in our data. In this way, we could develop a distance matrix by computing `1 / log(rank + 1)` for each video pair, where `rank` refers to the position of the recommendation in the list on each video page. We would than symmetrize the matrix such that it would satisfy the requirements of a distance metric. First, we attempted to download the related videos for each video in our data using Google's Youtube v3 API, which exposes a convenient method for just this kind of search. Unfortunately, Google recently reduced the number of queries allowed of this kind such that we would have only been able to request information on less than 100 videos each day.[^bignote] 

With the API no longer an option, we developed a method using `selenium` to automatically visit the page of each Youtube video, parse the page's HTML and CSS to identify links to related videos, and save their video IDs. Though much slower (the relevant code takes more than 24 hours to collect all of the data and will repeatedly open tabs in a browser) and likely not as complete as the API method, we were able to record between 50 and 120 related video IDs for most of the videos in our dataset. From these, we constructed a distance matrix as described above. However, this matrix was so sparse -- almost half of the nodes were isolated -- that we were unable to draw interesting conclusions from (or in some cases, even run) our analyses on these data.

Instead, we returned to the Youtube API, and extracted the top 100 comments for all of the videos in both sets of data from the original paper that were still available.

### Data Preprocessing 

To create a feature matrix from the available data, we constructed a data processing pipeline that processes and combines the text from the titles, descriptions, comments, and tags for each video. In this pipeline, we employed separate techniques for the comments and the other features. Reasoning that keywords would be better captured with TF-IDF vectorization, wherein word frequencies are computed and normalized by the frequency of those words throughout the document corpus, we applied this technique to vectorize the titles, descriptions, and tags for each video. 

For the comments, we trained a document embedding model known as Doc2Vec provided by the gensim library to create vector representations of the comments section of each video. 


## Empirical Results

-- results from classification models
-- phate results
-- k-means clustering
-- hierarchical clustering

## Conclusions


[^1] Ovide, S. (2020, April 20). Take YouTube's Dangers Seriously. Retrieved December 17, 2020, from https://www.nytimes.com/2020/04/20/technology/youtube-conspiracy-theories.html

[^2] Roose, K. (2020, October 15). YouTube Cracks Down on QAnon Conspiracy Theory, Citing Offline Violence. Retrieved December 17, 2020, from https://www.nytimes.com/2020/10/15/technology/youtube-bans-qanon-violence.html

[^3] Faddoul, M., Chaslot, G., &amp; Farid, H. (2020, March 06). A Longitudinal Analysis of YouTube's Promotion of Conspiracy Videos. Retrieved December 17, 2020, from https://arxiv.org/abs/2003.03318

[^4] https://github.com/youtube-dataset/conspiracy

[^bignote] The `yt_api_query/relatedvidgraph.py` file provides documented methods for calling the Youtube API and parsing the response. At first glance, the query limit for free Google projects of 10,000 queries per day seems more than sufficient to gather information on 4200 videos. Unfortunately, calling the `list.search` method counts as 100 queries, which equates to only 100 actual requests. To make matters worse, each initial request can return multiple page, each of which incurs a 100 query penalty to view.  