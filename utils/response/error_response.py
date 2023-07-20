from utils.response.response_command import Response


class ErrorResponse(Response):
    def __init__(self, body):
        super().__init__("ERROR", body)
