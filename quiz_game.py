
class QuizGame:
  def __init__(self):
    return

  def run_game(self):
    self.print_menu()
    while True:
      try:
        print("welcome")
      except :
        # case
        print("ERROR")
      finally:
        raise NotImplementedError

  def print_menu(self):
    print("========================================")
    print("            🎯 QUIZ SHOW 🎯")
    print("========================================")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("========================================")

gameInstance = QuizGame()
gameInstance.run_game()
