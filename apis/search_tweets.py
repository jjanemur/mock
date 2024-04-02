from copy import copy

from flask_restful import Resource
from flask import request, jsonify

from src.tweets_template import OBJECT
from utils.auth import auth_checker


class SearchTweetsApi(Resource):

    _dummy = OBJECT

    @property
    def tweets(self):
        return self._dummy["data"]

    @property
    def users(self):
        return self._dummy["includes"]["users"]

    @property
    def media(self):
        return self._dummy["includes"]["media"]

    # @data.setter
    # def data(self, changes):
    #     self._dummy = changes

    @auth_checker
    def get(self):
        tweets_data = self.tweets
        users = self.users
        media = self.media
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
