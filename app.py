import logging

from flask import Flask
from flask_restful import Api

from search_tweets import SearchTweetsApi

app = Flask(__name__)
api = Api(app)


api.add_resource(SearchTweetsApi, "/2/tweets/search/recent", endpoint='tweets')
app.logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    app.run(debug=True)
