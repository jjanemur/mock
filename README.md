# twitter_mock

```
cd existing_repo
git remote add origin https://gitlab.exan.tech/qa/twitter_mock.git
git branch -M master
git push -uf origin master
```

## Description
Simple mock on Flask for twitter recent search api https://developer.twitter.com/en/docs/twitter-api/tweets/search/quick-start/recent-search

## Authorization

For authorization just provide any Bearer Token.

## Filters
Can filter only by start_time. Always returns two pages if no start_time filter is given.

## Data generation
Changes id, created_at and cashtags every period given in the config.
To force change data use /force_change api with body {"value": True} for whole file change and {"value": False} to update the last object only. 
To change last id in case the application was restarted use /last_id api with body {"value": id}
