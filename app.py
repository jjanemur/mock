from base64 import b64encode

from flask import Flask

app = Flask(__name__)


class BasicAuthenticator:
    def login(self, username: str, password: str):
        if username != "dummy" or password != "password":
            return 'Unauthorized', 401

        token = b64encode(f'{username}:{password}'.encode('utf-8')).decode('ascii')
        return {'token': token}


if __name__ == '__main__':
    app.run(debug=True)
