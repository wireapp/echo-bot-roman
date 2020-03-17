from flask import Blueprint, request, jsonify, abort

from api.Configuration import get_configuration

roman_api = Blueprint('roman_api', __name__)


@roman_api.route('/messages', methods=['POST'])
def messages_api():
    # TODO verify that this is the way
    config = get_configuration()

    bearer_token = request.headers['Authorization'].split("Bearer ", 1)[1]

    if bearer_token != config.roman_token:
        return abort(401)

    json = request.get_json()

    return jsonify({'success': True})
