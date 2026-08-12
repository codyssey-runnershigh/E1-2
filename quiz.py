class Quiz:
    def __init__(self, question: str, choices: list[str], answer: int) -> None:
        self.question = question
        self.choices = list(choices)

    def submit_answer(self, user_answer: int) -> None:
        self.answer = int(user_answer)

    def is_correct(self, user_answer: int) -> bool:
        return int(user_answer) == self.answer

    def correct_choice_text(self) -> str:
        if 1 <= self.answer <= len(self.choices):
            return self.choices[self.answer - 1]
        return ""

    def format_question(self, number:int = 0) -> str:
        lines = []
        if number is not None:
            lines.append(f"[문제 {number}] {self.question}")
        else:
            lines.append(self.question)
        for idx, choice in enumerate(self.choices, start=1):
            lines.append(f"  {idx}. {choice}")
        return "\n".join(lines)

    def summary_line(self, number: int) -> str:
        return f"[{number}] {self.question}"

    def to_dict(self) -> dict:
        return {
            "QUESTION": self.question,
            "ANSWER": {str(i + 1): choice for i, choice in enumerate(self.choices)},
            "CORRECT_ANSWER": self.answer,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Quiz":
        if not isinstance(data, dict):
            raise ValueError("데이터가 dict 형식이 아닙니다.")

        # 문제 텍스트 파싱 ("QUESTION")
        question = data.get("QUESTION") or ""
        if not question or not isinstance(question, str):
            raise ValueError("비어있지 않은 문제 텍스트가 필요합니다.")

        # 선택지 파싱 ("ANSWER")
        raw_choices = data.get("CHOICES") or data.get("choices") or []
        if isinstance(raw_choices, dict):
            # dict 키(1, 2, 3, 4) 정렬하여 리스트로 전환
            choices = [
                str(raw_choices[k])
                for k in sorted(raw_choices.keys(), key=lambda x: int(x) if str(x).isdigit() else x)
            ]
        elif isinstance(raw_choices, list):
            choices = [str(c) for c in raw_choices]
        else:
            raise ValueError("선택지 형식이 바르지 않습니다.")

        # 정답 번호 파싱 ("CORRECT_ANSWER" 또는 "answer")
        answer = data.get("CORRECT_ANSWER")
        if answer is None:
            raise ValueError("정답 번호가 필요합니다.")

        try:
            answer = int(answer)
        except ValueError:
            raise ValueError("정답 번호는 숫자여야 합니다.")

        return cls(question, choices, answer)