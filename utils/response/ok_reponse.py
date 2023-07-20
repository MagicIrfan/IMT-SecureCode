from utils.response.response_command import Response


class OKResponse(Response):
    def __init__(self, body):
        super().__init__("OK", body)
