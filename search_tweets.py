import json
import random
from copy import copy
from datetime import datetime
from pathlib import Path

import pytz
from flask_restful import Resource
from flask import request, jsonify

from auth import auth_checker
from symbol_ids import SYMBOL_IDS

FILE_PATH = Path(__file__).parent.joinpath('tweets_template.json').absolute()
LAST_ID = 0


class SearchTweetsApi(Resource):

    _dummy = {}

    @property
    def symbols(self):
        return SYMBOL_IDS

    @property
    def dummy(self):
        if not self._dummy:
            with open(FILE_PATH) as f:
                self._dummy = json.load(f)
        return self._dummy

    def change_tweets(self) -> list:
        global LAST_ID

        date = datetime.now(tz=pytz.timezone('UTC'))
        data = self.dummy['data']

        for tweet in data:
            LAST_ID += 1
            tweet['created_at'] = date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            tweet['id'] = LAST_ID
            if entities := tweet.get('entities'):
                for cashtag in entities.get('cashtags', []):
                    new_cashtag = random.choice(self.symbols)
                    tweet['text'] = tweet['text'].replace(cashtag['tag'], new_cashtag)
                    cashtag['tag'] = new_cashtag
        return data

    @auth_checker
    def get(self):
        tweets_data = self.change_tweets()
        users = self.dummy["includes"]["users"]
        media = self.dummy["includes"]["media"]
        if query := request.args.get('query', None):
            tweets_data = self.filter_data(tweets_data, query)
        if fields := request.args.get('tweet.fields', None):
            tweets_data = self.filter_fields(tweets_data, fields)
        if user_fields := request.args.get('user.fields', None):
            users = self.filter_fields(users, user_fields)
        if media_fields := request.args.get('media.fields', None):
            media = self.filter_fields(media, media_fields)
        return jsonify({"data": tweets_data, "includes": {"users": users, "media": media}})

    @staticmethod
    def filter_fields(_object: list, _fields: str) -> list:
        new_data = []
        _fields = _fields.split(',')
        for i in _object:
            new_tweet = {k: v for k, v in i.items() if k in _fields}
            new_data.append(new_tweet)

        return new_data

    @staticmethod
    def filter_data(_object: list, _query: str) -> list:
        data = copy(_object)
        _query = _query.split(' ')
        if keywords := [k for k in _query if ':' not in _query]:
            for keyword in keywords:
                data = [i for i in data if keyword in i['text']]
        return data
