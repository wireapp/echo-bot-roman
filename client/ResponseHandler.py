from api.Configuration import Config
from client.RomanClient import RomanClient


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
        message_type = json['type']
        try:
            {
                'conversation.bot_request': lambda x: print('Handling bot request.'),
                'conversation.init': self.__init,
                'conversation.new_text': self.__new_message
            }[message_type](json)
        except KeyError:
            # type is different
            print(f'Unhandled type: {json["type"]}')
        except Exception as ex:
            print(ex)

    def __init(self, json: dict):
        print('init received')

        self.__send_text("Hello! I'm Echo Bot!", [], json['token'])  # TODO get message info

    def __new_message(self, json: dict):
        print('New text message received.')

        if not json.get('text'):
            print(f'Unsupported payload.')
            return

        payload = json['text']

        text = payload['data']
        mentions = payload['mentions']

        new_text = self.__prefix + text
        for mention in mentions:
            mention['offset'] = mention['offset'] + self.__prefix_offset

        self.__send_text(new_text, mentions, json['token'])

    def __send_text(self, message: str, mentions: list, token: str):
        text = {'data': message, 'mentions': mentions}  # TODO add support for more types than just text
        msg = {'type': 'create', 'text': text}
        self.client.send_message(token, msg)
