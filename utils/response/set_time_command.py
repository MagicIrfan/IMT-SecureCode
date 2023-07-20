from response_command import Response


class SetTimeCommand(Response):
    def __init__(self, body):
        super().__init__("SET_TIME", body)
