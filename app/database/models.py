from datetime import datetime
from uuid import UUID

class User():
    def __init__(self, user_id: int, username: str, fio: str, status: str, group: str or None):
        self.user_id = user_id
        self.username = username
        self.fio = fio
        self.status = status
        self.group = group

class Test():
    def __init__(self, creator_user_id: int, creation_time, test_key: UUID, test_name: str, subject_name: str or None,  all_questions: list, all_answers: list, right_answers: list, visible_result: bool) -> None:
        self.creator_user_id = creator_user_id
        self.creation_time = creation_time.strftime('%Y-%m-%d %H:%M:%S')
        self.test_key = test_key
        self.test_name = test_name
        self.subject_name = subject_name
        self.all_questions = all_questions
        self.all_answers = all_answers
        self.right_answers = right_answers
        self.visible_result = visible_result