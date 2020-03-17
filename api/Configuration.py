import os
from dataclasses import dataclass

from flask import current_app as app


@dataclass
class Config:
    roman_url: str
    roman_token: str


def get_configuration() -> Config:
    return Config(roman_url=get_prop('ROMAN_URL'), roman_token=get_prop('ROMAN_TOKEN'))


def get_prop(name: str) -> str:
    env = os.environ.get(name)
    return env if env else app.config[name]
