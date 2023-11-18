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
    def __init__(self, test_id: int or None, creator_user_id: int, creation_time, test_key: UUID, test_name: str, subject_name: str or None,  all_questions: list, all_answers: list, right_answers: list, visible_result: bool) -> None:
        self.test_id = test_id
        self.creator_user_id = creator_user_id
        try:
            self.creation_time = creation_time.strftime('%Y-%m-%d %H:%M:%S')
        except AttributeError:
            self.creation_time = creation_time
        self.test_key = test_key
        self.test_name = test_name
        self.subject_name = subject_name
        self.all_questions = all_questions
        self.all_answers = all_answers
        self.right_answers = right_answers
        self.visible_result = visible_result

class TestResult():
    def __init__(self, solved_test_id: int, who_done_test: int, completion_time, count_correct_answers: int, count_answers_in_total: int, answers_with_mistakes: list) -> None:
        self.who_done_test = who_done_test
        try:
            self.completion_time = completion_time.strftime('%Y-%m-%d %H:%M:%S')
        except AttributeError:
            self.completion_time = completion_time
            self.solved_test_id = solved_test_id
            self.count_correct_answers = count_correct_answers
            self.count_answers_in_total = count_answers_in_total
            self.answers_with_mistakes = answers_with_mistakes
    def procent_of_right(self):
        return round(self.self.count_correct_answers / self.count_answers_in_total * 100)
    
    def recomend_mark(self):
        if self.procent_of_right() >= 85:
            return 5
        elif self.procent_of_right() >= 65:
            return 4
        elif self.procent_of_right() >= 40:
            return 3
        else:
            return 2