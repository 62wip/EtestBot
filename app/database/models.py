class User():
    def __init__(self, user_id: int, username: str, fio: str, status: chr, group: str or None):
        self.user_id = user_id
        self.username = username
        self.fio = fio
        self.status = status
        self.group = group