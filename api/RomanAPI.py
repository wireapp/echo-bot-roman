from flask import Blueprint, request, jsonify, Response

from api.Configuration import get_configuration
from client.ResponseHandler import ResponseHandler

roman_api = Blueprint('roman_api', __name__)


@roman_api.route('/messages', methods=['POST'])
def messages_api():
    config = get_configuration()

    try:
        bearer_token = request.headers['Authorization'].split("Bearer ", 1)[1]
        if bearer_token != config.roman_token:
            return auth_denied()
    except Exception as ex:
        print(ex)
        return auth_denied()

    ResponseHandler(config).handle(request.get_json())
    return jsonify({'success': True})


def auth_denied() -> Response:
    return Response('Access denied, wrong or missing token.', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
