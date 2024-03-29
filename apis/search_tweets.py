from copy import copy

from flask_restful import Resource
from flask import request, jsonify

from src.tweets import OBJECT


class SearchTweetsApi(Resource):

    _dummy = OBJECT

    @property
    def data(self):
        return self._dummy["data"]

    # @data.setter
    # def data(self, changes):
    #     self._dummy = changes

    def get(self):
        tweets_data = self.data
        if fields := request.args.get('tweet.fields', None):
            tweets_data = self.filter_fields(self.data, fields)
        if query := request.args.get('query', None):
            tweets_data = self.filter_data(tweets_data, query)

        return jsonify({"data": tweets_data})

    @staticmethod
    def filter_fields(_object: list, _fields: str) -> list:
        new_data = []
        _fields = _fields.split(',')
        for tweet in _object:
            new_tweet = {k: v for k, v in tweet.items() if k in _fields}
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
