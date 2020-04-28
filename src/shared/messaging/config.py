class Config:
    def __init__(self, username, password, host, retry_count=None):
        self.username = username
        self.password = password
        self.host = host
        self.retry_count = retry_count

