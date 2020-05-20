import logging

from api.Configuration import Config
from client.RomanClient import RomanClient

logger = logging.getLogger(__name__)


class ResponseHandler:
    __prefix = 'You said: '
    __prefix_offset = len(__prefix)

    def __init__(self, config: Config):
        self.config = config
        self.client = RomanClient(config)

    def handle_json(self, json: dict):
        """
        Handle message received from the Roman
        """
        # TODO remove this in the future
        logger.debug(f'Received data')
        logger.debug(f'{json}')

        message_type = json.get('type')
        logger.debug(f'Handling message type: {message_type}')
        try:
            {
                'conversation.bot_request': lambda x: logger.info('Handling bot request.'),
                'conversation.init': self.__init,
                'conversation.new_text': self.__new_message,
                None: lambda x: logger.error(f'No type received for json: {x}')
            }[message_type](json)
        except KeyError:
            # type is different
            logger.warning(f'Unhandled type: {message_type}')
        except Exception as ex:
            logger.exception(ex)

    def __init(self, json: dict):
        logger.debug('init received')
        self.__send_text("Hello! I'm Echo Bot!", [], json['token'])  # TODO get message info

    def __new_message(self, json: dict):
        logger.debug('New text message received.')

        if not json.get('text'):
            logger.warning(f'Unsupported payload.')
            return

        text = json['text']
        mentions = json['mentions']

        new_text = self.__prefix + text
        for mention in mentions:
            mention['offset'] += self.__prefix_offset

        self.__send_text(new_text, mentions, json['token'])

    def __send_text(self, message: str, mentions: list, token: str):
        text = {'data': message, 'mentions': mentions}  # TODO add support for more types than just text
        msg = {'type': 'text', 'text': text}
        self.client.send_message(token, msg)
