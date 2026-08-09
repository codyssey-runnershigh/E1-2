from io_controller import io_controller,ExitSignal
from storage_handler import Storage

QUIZ_PLAY = 1
ADD_QUIZ = 2
QUIZ_LIST = 3
CHECK_SCORE = 4

class QuizGame:
  quiz_list = []

  def __init__(self):
    return

  def run_game(self):
    io = io_controller()
    while True:
      try:
        self.print_menu(io)
        menu_num = io.ask_int("선택: ", QUIZ_PLAY, CHECK_SCORE)
        if menu_num == QUIZ_LIST:
          loader = Storage()
          data, status = loader.load()
          if status == Storage.STATUS_OK:
            print(data)
      except ExitSignal:
        io.warn("EXIT")
        break
      except :
        io.warn("ERROR")
        break
      finally:
        io.info("finally")

  def print_menu(self, io):
    io.title("            🎯 QUIZ SHOW 🎯")
    io.text(f"{QUIZ_PLAY}. 퀴즈 풀기")
    io.text(f"{ADD_QUIZ}. 퀴즈 추가")
    io.text(f"{QUIZ_LIST}. 퀴즈 목록")
    io.text(f"{CHECK_SCORE}. 점수 확인")
    io.divider()

  def quiz_loader(self, quizData):
    return 1


gameInstance = QuizGame()
gameInstance.run_game()
