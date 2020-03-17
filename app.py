from importlib import util as importing

from flask import Flask, jsonify

from api.RomanAPI import roman_api

app = Flask(__name__)

app.register_blueprint(roman_api)

config_file = 'config'

if importing.find_spec(config_file):
    app.config.from_object(config_file)


@app.route('/')
def messages():
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(host='localhost', port=8080)
