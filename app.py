from flask import Flask, request, jsonify
from flask_restful import Api, Resource


from data_generator import OBJECT
from filters import filter_data

app = Flask(__name__)
api = Api(app)


@app.route('/')
def index():

    return 'Template'


@app.route('/users', methods=['GET'])
def get_users():
    username = request.args.get('username', None)
    user_id = request.args.get('id', None)

    return jsonify(filter_data(OBJECT, username=username, user_id=user_id))


if __name__ == '__main__':
    app.run(debug=True)
