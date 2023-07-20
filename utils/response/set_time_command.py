from response import Response


class SetTimeCommand(Response):
    def __init__(self, body):
        super().__init__("SET_TIME", body)
