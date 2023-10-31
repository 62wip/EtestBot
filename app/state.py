from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    waiting_for_set_fio = State()
    waiting_for_set_status = State()
    waiting_for_set_group = State()
    waiting_for_feedback = State()
    waiting_for_update_for_teacher = State()
    waiting_for_update_for_student = State()
    waiting_for_update_fio = State()
    waiting_for_update_status = State()
    waiting_for_update_group = State()
    waiting_for_test_name = State()
    waiting_for_test_subject = State()
    waiting_for_test_question = State()
    waiting_for_test_answer = State()
    waiting_for_test_preview = State()
    waiting_for_del_question = State()