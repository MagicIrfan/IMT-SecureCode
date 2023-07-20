from response import Response


class OKResponse(Response):
    def __init__(self, body):
        super().__init__("OK", body)
