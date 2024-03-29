from base64 import b64encode
from flask import Flask
from flask_restful import Api

from apis.search_tweets import SearchTweetsApi

app = Flask(__name__)
api = Api(app)


class BasicAuthenticator:
    def login(self, username: str, password: str):
        if username != "dummy" or password != "password":
            return 'Unauthorized', 401

        token = b64encode(f'{username}:{password}'.encode('utf-8')).decode('ascii')
        return {'token': token}


api.add_resource(SearchTweetsApi, "/2/tweets/search/recent", endpoint='tweets')

if __name__ == '__main__':
    app.run(debug=True)
