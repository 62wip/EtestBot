from datetime import datetime

class User():
    def __init__(self, user_id: int, username: str, fio: str, status: chr, group: str or None):
        self.user_id = user_id
        self.username = username
        self.fio = fio
        self.status = status
        self.group = group

class Test():
    def __init__(self, creator_user_id: int, creation_time: datetime, test_name: str, subject_name: str, all_questions: list(str), all_answers: list(list(str)), right_answer: list(int), visible_result: bool) -> None:
        self.creator_user_id = creator_user_id
        self.creation_time = creation_time
        self.test_name = test_name
        self.subject_name = subject_name
        self.all_questions = all_questions
        self.all_answers = all_answers
        self.right_answer = right_answer
        self.visible_result = visible_result