import uuid
from dataclasses import dataclass
from typing import Optional

import flask


def request_id() -> 'RequestId':
    """
    Returns ID of the current request.
    """
    request_id = getattr(flask.g, 'request_id', None)
    if request_id:
        return request_id

    nginx_id = flask.request.headers.get("X-Request-Id")
    request_id = RequestId(nginx_id, str(uuid.uuid4()))
    # do not access flask.g when not necessary
    flask.g.request_id = request_id
    return request_id


@dataclass
class RequestId:
    """
    Id application got from header X-Request-Id
    """
    nginx_related: Optional[str]
    """
    Unique ID for each request in the application.
    """
    app_related: str
