import json
import random
from copy import deepcopy
from datetime import datetime, timedelta
from pathlib import Path

import pytz
from flask_restful import Resource
from flask import request, jsonify

from auth import auth_checker
from tickers import TICKERS

FILE_PATH = Path(__file__).parent.joinpath('tweets_template.json').absolute()

last_id = 0
tweets = {'page_1': [], 'page_2': []}
last_updated = None


class SearchTweetsApi(Resource):

    _dummy = {}
    next_token = 'token'

    @property
    def tickers(self):
        return TICKERS

    @property
    def dummy(self):
        if not self._dummy:
            with open(FILE_PATH) as f:
                self._dummy = json.load(f)
        return self._dummy

    @property
    def last_data_first_page(self):
        return tweets['page_1']

    @property
    def last_data_second_page(self):
        return tweets['page_2']

    def change_tweet(self, tweet: dict, ticker: str | None = None):
        global last_id
        last_id += 1
        tweet['created_at'] = last_updated.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        tweet['id'] = str(last_id)
        if entities := tweet.get('entities'):
            for cashtag in entities.get('cashtags', []):
                new_ticker = ticker or random.choice(self.tickers)
                tweet['text'] = tweet['text'].replace(cashtag['tag'], new_ticker)
                cashtag['tag'] = new_ticker

    def change_tweets(self, full_change: bool = True, force_change: bool = False):
        from app import app
        global last_updated, tweets

        now = datetime.now(tz=pytz.utc).replace(microsecond=0)
        if last_updated:
            update_after = last_updated + timedelta(
                minutes=app.config['UPDATE_MINUTES'], hours=app.config['UPDATE_HOURS']
            )
        else:
            update_after = now

        if update_after <= now or force_change:
            last_updated = now
            data = deepcopy(self.dummy["data"])

            if full_change:
                for i in range(2):
                    app.logger.info(f'Changing data for page {i} to created_at {last_updated}, last id = {last_id}')
                    for tweet in data:
                        self.change_tweet(tweet)
                    tweets[f'page_{i + 1}'] = deepcopy(data)
            else:  # меняем только последний элемент
                app.logger.info(f'Changing data to created_at {last_updated} for first tweet')
                self.change_tweet(self.last_data_first_page[0], 'TSLA')

    @auth_checker
    def get(self):
        from app import app

        self.change_tweets()

        if request.args.get('next_token'):
            self.next_token = None
            tweets_data = self.last_data_second_page
            app.logger.info('Returning data for 2 page')
        else:
            tweets_data = self.last_data_first_page
            app.logger.info('Returning data for 1 page')

        if start_time := request.args.get('start_time'):
            tweets_data = self.filter_by_start_time(start_time, tweets_data)

        users = self.dummy["includes"]["users"]
        media = self.dummy["includes"]["media"]
        # if query := request.args.get('query'):
        #     tweets_data = self.filter_data(tweets_data, query)
        if fields := request.args.get('tweet.fields'):
            required_fields = 'id,text,author_id,created_a'
            tweets_data = self.filter_fields(tweets_data, fields, required_fields)
        if user_fields := request.args.get('user.fields'):
            users = self.filter_fields(users, user_fields)
        if media_fields := request.args.get('media.fields'):
            media = self.filter_fields(media, media_fields)

        if not len(tweets_data):
            return jsonify({"meta": {"result_count": 0}})

        result_count = len(tweets_data)
        self.next_token = self.next_token if result_count == 100 else None
        meta = {"result_count": result_count, "next_token": self.next_token}
        return jsonify({"data": tweets_data, "includes": {"users": users, "media": media}, "meta": meta})

    @staticmethod
    def filter_fields(_object: list, _fields: str, _required_fields: str | None = None) -> list:
        new_data = []
        _fields = _fields.split(',')
        if _required_fields:
            _required_fields = _required_fields.split(',')
            _fields.extend(_required_fields)
        for i in _object:
            new_tweet = {k: v for k, v in i.items() if k in set(_fields)}
            new_data.append(new_tweet)

        return new_data

    @staticmethod
    def filter_by_start_time(start_time: str, tweets_data: list) -> list:
        start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%fZ')
        filtered_tweets = []
        for tweet in tweets_data:
            created_at = datetime.strptime(tweet["created_at"], '%Y-%m-%dT%H:%M:%S.%fZ')
            if created_at > start_time:
                filtered_tweets.append(tweet)
        return filtered_tweets

    # @staticmethod
    # def filter_data(_object: list, _query: str) -> list:
    #     data = copy(_object)
    #     _query = _query.split(' ')
    #     if keywords := [k for k in _query if ':' not in _query]:
    #         for keyword in keywords:
    #             data = [i for i in data if keyword in i['text']]
    #     return data


class ForceChange(Resource):

    @staticmethod
    def post():
        full_change = request.json.get('value')
        SearchTweetsApi().change_tweets(full_change, force_change=True)
        if type(full_change) is bool:
            return jsonify(value=full_change)
        else:
            return 'Bad value; should be boolean', 400


class LastId(Resource):

    def post(self):
        from app import app
        global last_id
        last_id = request.json.get('value')
        if type(last_id) is int:
            app.logger.info(f'Changing last id to {last_id}')
            return self.get()
        else:
            return 'Bad value; should be a number', 400

    @staticmethod
    def get():
        return jsonify(value=last_id)


class Healthcheck(Resource):

    @staticmethod
    def get():
        return jsonify(status="OK")
