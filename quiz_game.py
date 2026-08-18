from io_controller import io_controller, ExitSignal
from storage_handler import Storage, STATUS_OK
from quiz import Quiz
from datetime import datetime

QUIZ_PLAY = 1
ADD_QUIZ = 2
QUIZ_LIST = 3
CHECK_SCORE = 4
QUIZZES = "quizzes"
RECORDS = "records"
_DEFAULT_QUIZ_DATA = {
    "quizzes": [
       {
          "QUESTION": "다음 중 윤동주의 시집은 무엇인가?",
          "CHOICES": {
            "1": "청록집",
            "2": "진달래꽃",
            "3": "하늘과 바람과 별과 시",
            "4": "님의 침묵"
          },
          "CORRECT_ANSWER": 3
        },
        {
          "QUESTION": "다음 중 이상의 작품은 무엇인가?",
          "CHOICES": {
            "1": "날개",
            "2": "메밀꽃 필 무렵",
            "3": "동백꽃",
            "4": "소나기"
          },
          "CORRECT_ANSWER": 1
        },
        {
          "QUESTION": "다음 중 밀란 쿤데라의 대표작은 무엇인가?",
          "CHOICES": {
            "1": "이방인",
            "2": "참을 수 없는 존재의 가벼움",
            "3": "변신",
            "4": "백년의 고독"
          },
          "CORRECT_ANSWER": 2
        },
        {
          "QUESTION": "밀란 쿤데라의 소설 『참을 수 없는 존재의 가벼움』에서 ‘가벼움’과 대비되는 개념은 무엇인가?",
          "CHOICES": {
            "1": "침묵",
            "2": "무거움",
            "3": "자유",
            "4": "우연"
          },
          "CORRECT_ANSWER": 2
        },
        {
          "QUESTION": "다음 중 표도르 도스토옙스키의 작품은 무엇인가?",
          "CHOICES": {
            "1": "죄와 벌",
            "2": "전쟁과 평화",
            "3": "아버지와 아들",
            "4": "닥터 지바고"
          },
          "CORRECT_ANSWER": 1
        },
    ],
    "records": []
  }

class QuizGame:

  def __init__(self):
    self.io = io_controller()
    self.storage = Storage()
    self._load_data_with_fallback()
    self._result_saved = False
    return

  def run_game(self):
    while True:
      try:
        self.io.title("            🎯 QUIZ SHOW 🎯")
        self.print_menu()
        select_menu_num = self.io.ask_int("선택: ", QUIZ_PLAY, CHECK_SCORE)

        if select_menu_num == QUIZ_PLAY:
          self.io.title("🎮 퀴즈 풀기")
          self.play_quiz()
        elif select_menu_num == ADD_QUIZ:
          self.io.title("➕ 퀴즈 추가")
          self.add_quiz()
        elif select_menu_num == QUIZ_LIST:
          self.io.title("📋 퀴즈 목록")
          self.show_quiz_list()
        elif select_menu_num == CHECK_SCORE:
          self.io.title("🏆 점수 기록")
          self.check_score()

      except ExitSignal:
        self.io.warn("KeyboardInterrupt")
        break
      except :
        self.io.warn("ERROR")
        break
      finally:
        self.io.blank()

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

  def play_quiz(self):
    if not self.quiz_list:
      self.io.warn("퀴즈 목록을 불러올 수 없거나 퀴즈가 없습니다.")
      return

    self._result_saved = False
    for idx, quiz in enumerate(self.quiz_list, start=1):
      self.set_quiz(idx, quiz)
    self.print_save_result(self.quiz_list)

  def show_quiz_list(self):
    for idx, quiz in enumerate(self.quiz_list, start=1):
      self.print_quiz(idx, quiz)

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
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    self.io.title("퀴즈 결과")
    self.io.text(f"총 {total_count} 문제 중 {correct_count} 문제 정답")
    self.io.text(f"점수: {score} 점")
    self.io.text(f"저장 시각: {current_time}")

    # 결과를 records에 저장 (1회만)
    if not getattr(self, "_result_saved", False):
      record = {
        "QUESTION_COUNT": total_count,
        "CORRECT_COUNT": correct_count,
        "SCORE": score,
        "DATE": current_time,
      }
      if not isinstance(self.load_data, dict):
        self.load_data = {QUIZZES: [], RECORDS: []}
      self.load_data.setdefault(RECORDS, []).append(record)
      self.storage.save(self.load_data)
      self._result_saved = True
      self.io.info("결과가 저장되었습니다.")

  def check_score(self):
    self._load_data_with_fallback()
    records = self.load_data.get(RECORDS, [])
    if not records:
      self.io.warn("저장된 점수 기록이 없습니다.")
    else:
      top_records = sorted(records, key=lambda x: x.get("SCORE", 0), reverse=True)[:5]
      for idx, record in enumerate(top_records, start=1):
        date_str = record.get("DATE", "N/A")
        self.io.text(f"[{idx}] {date_str} - 총 {record.get('QUESTION_COUNT')}문제 중 {record.get('CORRECT_COUNT')}문제 정답 ({record.get('SCORE')}점)")
    self.io.divider()

  def quiz_loader(self, quizData):
    self._load_data_with_fallback()
    self.score_list = self.load_data.get(RECORDS, [])

  def _load_data_with_fallback(self):
    self.load_data, self.status = self.storage.load()
    is_valid = True
    if self.status != STATUS_OK or not isinstance(self.load_data, dict) or QUIZZES not in self.load_data:
      is_valid = False
    else:
      try:
        temp_list = []
        for item in self.load_data[QUIZZES]:
          temp_list.append(Quiz.from_dict(item))
      except (ValueError, TypeError, KeyError):
        is_valid = False

    if not is_valid:
      import copy
      import shutil

      # 기존 파일이 존재하는 경우 (포맷이 손상되었거나 잘못된 스키마인 경우) 백업 생성
      if self.storage.exists():
        backup_path = self.storage.path + ".bak"
        try:
          shutil.copyfile(self.storage.path, backup_path)
          self.io.info(f"기존의 유효하지 않은 파일을 백업으로 보존했습니다: {backup_path}")
        except Exception as e:
          self.io.warn(f"기존 파일 백업 중 오류 발생: {e}")
      self.load_data = copy.deepcopy(_DEFAULT_QUIZ_DATA)
      self.status = STATUS_OK
      self.io.warn("데이터가 유효하지 않거나 없습니다. 기본 데이터를 사용, 저장합니다.")
      self.storage.save(self.load_data)

    self.quiz_list = []
    for item in self.load_data[QUIZZES]:
      self.quiz_list.append(Quiz.from_dict(item))


if __name__ == "__main__":
  gameInstance = QuizGame()
  gameInstance.run_game()
