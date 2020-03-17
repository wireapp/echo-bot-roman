from api.Configuration import Config


class ResponseHandler:

    def __init__(self, config: Config):
        self.confg = config

    def handle(self, json: dict):
        pass
