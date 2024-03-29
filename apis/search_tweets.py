from copy import copy

from flask_restful import Api, Resource
from flask import request, jsonify

from app import app
from src.tweets import OBJECT

api = Api(app)


class SearchTweetsApi(Resource):

    _dummy = OBJECT

    @property
    def data(self):
        return self._dummy["data"]

    def get_tweets(self):
        fields = request.args.get('tweet_fields', None)
        tweets_data = self.filter_fields(self.data, fields)
        tweets_data = (self.filter_data(tweets_data))

        return jsonify({"data": tweets_data})

    @staticmethod
    def filter_fields(_object, _fields) -> list:
        data = copy(_object)
        new_data = []
        for tweet in data:
            new_item = {k: v for k, v in tweet.items() if k in _fields}
            new_data.append(new_item)

        return new_data

    @staticmethod
    def filter_data(_object: list, **kwargs) -> list:
        filtered_object = _object
        for k, v in kwargs.items():
            if not v:
                continue
            filtered_object = [i for i in filtered_object if i[k] == v]
        return filtered_object


api.add_resource(SearchTweetsApi, "2/tweets/search/recent", endpoint='tweets')


