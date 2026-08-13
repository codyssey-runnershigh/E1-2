from io_controller import io_controller, ExitSignal
from storage_handler import Storage, STATUS_OK
from quiz import Quiz

QUIZ_PLAY = 1
ADD_QUIZ = 2
QUIZ_LIST = 3
CHECK_SCORE = 4
QUIZZES = "quizzes"
RECORDS = "records"

class QuizGame:

  def __init__(self):
    self.io = io_controller()
    self.storage = Storage()
    self.load_data, self.status = self.storage.load()
    self.quiz_list: list[Quiz] = []
    if self.status == STATUS_OK and self.load_data and QUIZZES in self.load_data:
      for item in self.load_data[QUIZZES]:
        self.quiz_list.append(Quiz.from_dict(item))
    return

  def run_game(self):
    while True:
      try:
        self.io.title("            🎯 QUIZ SHOW 🎯")
        self.print_menu()
        select_menu_num = self.io.ask_int("선택: ", QUIZ_PLAY, CHECK_SCORE)

        if select_menu_num == QUIZ_PLAY:
          if not self.quiz_list:
            self.io.warn("퀴즈 목록을 불러올 수 없거나 퀴즈가 없습니다.")
            continue
          else:
            for idx, quiz in enumerate(self.quiz_list, start=1):
              self.set_quiz(idx, quiz)
          self.print_save_result(self.quiz_list)
        elif select_menu_num == ADD_QUIZ:
          self.io.title("➕ 퀴즈 추가")
          self.add_quiz()
        elif select_menu_num == QUIZ_LIST:
          self.io.title("📋 퀴즈 목록")
          for idx, quiz in enumerate(self.quiz_list, start=1):
            self.print_quiz(idx, quiz)
        elif select_menu_num == CHECK_SCORE:
          continue

      except ExitSignal:
        self.io.warn("EXIT")
        break
      except :
        self.io.warn("ERROR")
        break
      finally:
        self.io.info("finally")

  def print_menu(self):
    self.io.text(f"{QUIZ_PLAY}. 퀴즈 풀기")
    self.io.text(f"{ADD_QUIZ}. 퀴즈 추가")
    self.io.text(f"{QUIZ_LIST}. 퀴즈 목록")
    self.io.text(f"{CHECK_SCORE}. 점수 확인")
    self.io.divider()

  def print_quiz(self, num: int, quiz: Quiz):
    self.io.divider(True)
    self.io.text(quiz.format_question(num))

  def add_quiz(self):
    question = self.io.ask_text("문제: ")
    choices = [
      self.io.ask_text(f"{idx}번 선택지: ")
      for idx in range(1, 5)
    ]
    correct_answer = self.io.ask_int("정답 번호: ", 1, len(choices))
    quiz = Quiz(question, choices, correct_answer)

    if not isinstance(self.load_data, dict):
      self.load_data = {QUIZZES: [], RECORDS: []}
    self.load_data.setdefault(QUIZZES, []).append(quiz.to_dict())
    self.storage.save(self.load_data)
    self.quiz_list.append(quiz)
    self.status = STATUS_OK
    self.io.success("퀴즈가 추가되었습니다.")

  def set_quiz(self, num:int, quiz: Quiz):
    self.print_quiz(num, quiz)
    self.io.blank()

    user_answer = self.io.ask_int("정답: ", 1, 4)
    quiz.submit_answer(user_answer)
    self.io.blank()

    if quiz.is_correct():
      self.io.success("정답입니다!")
    else:
      self.io.warn("오답입니다.")
    self.io.blank()

  def print_save_result(self, quiz_list: list[Quiz]):
    '''
      퀴즈 결과 통계, 저장 (1회만)
    '''
    total_count = len(quiz_list)
    correct_count = 0
    for quiz in quiz_list:
      if quiz.is_correct():
        correct_count += 1

    score = round(correct_count / total_count * 100)

    self.io.title("퀴즈 결과")
    self.io.text(f"총 {total_count} 문제 중 {correct_count} 문제 정답")
    self.io.text(f"점수: {score} 점")

    # 결과를 records에 저장 (1회만)
    if not getattr(self, "_result_saved", False):
      record = {
        "QUESTION_COUNT": total_count,
        "CORRECT_COUNT": correct_count,
        "SCORE": score,
      }
      if not isinstance(self.load_data, dict):
        self.load_data = {QUIZZES: [], RECORDS: []}
      self.load_data.setdefault(RECORDS, []).append(record)
      self.storage.save(self.load_data)
      self._result_saved = True
      self.io.info("결과가 저장되었습니다.")

  def quiz_loader(self, quizData):
    self.load_data, self.status = self.storage.load()
    self.quiz_list: list[Quiz] = []
    if self.status == STATUS_OK and self.load_data and QUIZZES in self.load_data:
      for item in self.load_data[QUIZZES]:
        self.quiz_list.append(Quiz.from_dict(item))
    self.score_list = self.load_data.get(RECORDS, []) if self.status == STATUS_OK else []


gameInstance = QuizGame()
gameInstance.run_game()
