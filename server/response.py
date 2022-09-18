class Response:

    def __init__(self, success: bool, **args):
        self.success = success
        self.args = args