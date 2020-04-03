from flask import request, jsonify, Response
from flask_restx import Namespace, Resource, fields

from api.Configuration import get_configuration
from client.ResponseHandler import ResponseHandler

roman_api = Namespace('bot', description='Bot API.')


@roman_api.route('', methods=['POST'])
@roman_api.route('messages', methods=['POST'])
class Messages(Resource):
    dummy_model = roman_api.model('Message', {
        'type': fields.String(required=True, description='Type of the message.')
    })

    @roman_api.doc(
        security='bearer',
        body=dummy_model
    )
    def post(self):
        config = get_configuration()

        try:
            bearer_token = request.headers['Authorization'].split("Bearer ", 1)[1]
            if bearer_token != config.roman_token:
                return auth_denied()
        except Exception:
            return auth_denied()

        ResponseHandler(config).handle_json(request.get_json())
        return jsonify({'success': True})


def auth_denied() -> Response:
    return Response('Access denied, wrong or missing token.', 401)
