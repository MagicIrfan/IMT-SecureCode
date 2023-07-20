from utils.response.response_command import Response


class GetTimeCommand(Response):
    def __init__(self, body):
        super().__init__("GET_TIME", body)
