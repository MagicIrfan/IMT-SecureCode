import json
from abc import ABC


class Response(ABC):
    def __init__(self, type_response, body):
        self._type_response = type_response
        self._body = body

    @property
    def type_response(self):
        return self._type_response

    @property
    def body(self):
        return self._body

    def __str__(self):
        response_json = json.dumps(self.to_json())
        return response_json

    def to_json(self):
        return {
            "type": self.type_response,
            "body": self.body
        }
