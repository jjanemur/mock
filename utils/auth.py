from flask_restful import reqparse


def auth_checker(func):
    def wrapper(*args, **kwargs):
        parser = reqparse.RequestParser()
        parser.add_argument('Authorization',
                            type=str,
                            required=True,
                            location='headers',
                            help='Authorization can not be empty!')
        token = parser.parse_args()['Authorization']

        if token == 'Bearer 123':
            result = func(*args, **kwargs)
            return result
        else:
            return 'Unauthorised', 401

    return wrapper
