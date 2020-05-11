import logging

from flask import request, jsonify, Response
from flask_restx import Namespace, Resource, fields

from api.Configuration import get_configuration
from client.ResponseHandler import ResponseHandler

logger = logging.getLogger(__name__)

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
        logger.debug(f"Used configuration {config}")
        try:
            logger.debug("Reading token.")
            bearer_token = request.headers['Authorization'].split("Bearer ", 1)[1]
            logger.debug(f"Token found: {bearer_token}")
            if bearer_token != config.roman_token:
                logger.debug(f"Auth denied for token {bearer_token}. Expected {config.roman_token}")
                return auth_denied()
        except Exception as ex:
            logger.exception(ex, "Auth denied due to exception.")
            return auth_denied()

        logger.debug("Auth OK.")
        ResponseHandler(config).handle_json(request.get_json())
        logger.debug("Request handled.")
        return jsonify({'success': True})


def auth_denied() -> Response:
    return Response('Access denied, wrong or missing token.', 401)
