class Logger:
    def __init__(self, name):
        self.name = name

    def info(self, message):
        print(f"[INFO] {self.name} - {message}")