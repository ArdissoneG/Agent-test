class Tool:
    name: str

    def run(self, action: dict):
        raise NotImplementedError
