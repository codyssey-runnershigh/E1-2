from io_controller import io_controller, ExitSignal
from storage_handler import Storage, STATUS_OK
from quiz import Quiz

QUIZ_PLAY = 1
ADD_QUIZ = 2
QUIZ_LIST = 3
CHECK_SCORE = 4

class QuizGame:

  def __init__(self):
    self.io = io_controller()
    self.loader = Storage()
    self.load_data, self.status = self.loader.load()
    self.quiz_list: list[Quiz] = []
    if self.status == STATUS_OK and self.load_data and "quizzes" in self.load_data:
      for item in self.load_data["quizzes"]:
        self.quiz_list.append(Quiz.from_dict(item))
    return

  def run_game(self):
    while True:
      try:
        self.print_menu()
        select_menu_num = self.io.ask_int("선택: ", QUIZ_PLAY, CHECK_SCORE)

        if select_menu_num == QUIZ_PLAY:
          if not self.quiz_list:
            self.io.warn("퀴즈 목록을 불러올 수 없거나 퀴즈가 없습니다.")
            continue
          else:
            for idx, quiz in enumerate(self.quiz_list, start=1):
              self.set_quiz(idx, quiz)
        elif select_menu_num == ADD_QUIZ:
          continue
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
    self.io.title("            🎯 QUIZ SHOW 🎯")
    self.io.text(f"{QUIZ_PLAY}. 퀴즈 풀기")
    self.io.text(f"{ADD_QUIZ}. 퀴즈 추가")
    self.io.text(f"{QUIZ_LIST}. 퀴즈 목록")
    self.io.text(f"{CHECK_SCORE}. 점수 확인")
    self.io.divider()

  def print_quiz(self, num: int, quiz: Quiz):
    self.io.divider(True)
    print(quiz.format_question(num))

  def set_quiz(self, num:int, quiz: Quiz):
    self.print_quiz(num, quiz)
    user_answer = self.io.ask_int("정답: ", 1, 4)
    quiz.submit_answer(user_answer)
    if quiz.is_correct(user_answer):
      self.io.success("정답입니다!")
    else:
      self.io.warn("오답입니다.")

  def check_result(self, quiz_list: list[Quiz]):
    '''
      퀴즈 결과 통계, 저장
    '''
    pass

  def quiz_loader(self, quizData):
    self.load_data, self.status = self.loader.load()
    self.quiz_list: list[Quiz] = []
    if self.status == STATUS_OK and self.load_data and "quizzes" in self.load_data:
      for item in self.load_data["quizzes"]:
        self.quiz_list.append(Quiz.from_dict(item))
    #todo: 점수 load


gameInstance = QuizGame()
gameInstance.run_game()
