import logging
from pathlib import Path

from flask import Flask
from flask_restful import Api

from search_tweets import SearchTweetsApi, ForceChange, Healthcheck, LastId

app = Flask(__name__)
api = Api(app)

api.add_resource(SearchTweetsApi, "/2/tweets/search/recent", endpoint='tweets')
api.add_resource(ForceChange, "/force_change", endpoint='force_change')
api.add_resource(LastId, "/last_id", endpoint='last_id')
api.add_resource(Healthcheck, "/health", endpoint='health')


app.logger.setLevel(logging.INFO)

if not Path(__file__).parent.joinpath('tweets_template.json').is_file():
    app.logger.error('config.py file is missing')
else:
    app.config.from_object('config')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
