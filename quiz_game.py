from io_controller import io_controller,ExitSignal

class QuizGame:
  def __init__(self):
    return

  def run_game(self):
    io = io_controller()
    while True:
      try:
        self.print_menu(io)
        menu_num = io.ask_int("input int test: ", 1, 5)
        print(menu_num)
      except ExitSignal:
        print("EXIT")
        break
      except :
        print("ERROR")
        break
      finally:
        print("finally")

  def print_menu(self, io):
    io.title("            🎯 QUIZ SHOW 🎯")
    io.text("1. 퀴즈 풀기")
    io.text("2. 퀴즈 추가")
    io.text("3. 퀴즈 목록")
    io.text("4. 점수 확인")
    io.divider()

gameInstance = QuizGame()
gameInstance.run_game()
