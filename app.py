import logging

from flask import Flask
from flask_restful import Api

from search_tweets import SearchTweetsApi, LastSnapshot

app = Flask(__name__)
api = Api(app)


api.add_resource(SearchTweetsApi, "/2/tweets/search/recent", endpoint='tweets')
api.add_resource(LastSnapshot, "/send_last_snapshot", endpoint='send_last_snapshot')

app.logger.setLevel(logging.DEBUG)
app.secret_key = 'SECRET_KEY'

if __name__ == '__main__':
    app.run(debug=True, port=8080)
