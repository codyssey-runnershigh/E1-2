
LINE = "=" * 40
THIN_LINE = "-" * 40


class ExitSignal(Exception):
    """
    사용자가 Ctrl+C 또는 EOF 로 종료를 요청했다는 Error class.
    """


class io_controller:
    """입력 검증 + 출력 문구를 한 곳에 모은다."""

    # ------------------------------------------------------------------
    # 입력
    # ------------------------------------------------------------------
    def _read(self, prompt: str) -> str:
        """Ctrl+C / EOF 를 ExitSignal 로 Throw"""
        try:
            return input(prompt)
        except (KeyboardInterrupt, EOFError):
            print()          # 줄바꿈으로 프롬프트 정리
            raise ExitSignal()

    def ask_int(self, prompt: str, min_value: int, max_value: int) -> int:
        """
          int 입력 받음. trim / min,max validation
        """
        while True:
            try:
              value = self._read(prompt).strip()
              if not value:  # 빈 문자열 검사 (strip 후 빈 문자열은 "")
                  self.warn("빈 입력은 허용되지 않습니다.")
                  continue
              intValue = int(value)
              if intValue < min_value or intValue > max_value:
                  self.warn("범위를 벗어난 값입니다.")
                  continue
              return intValue
            except ValueError:
                self.warn("잘못된 입력입니다. 정수를 입력해주세요.")
                continue
            except ExitSignal:
                raise ExitSignal()

    def ask_text(self, prompt: str, allow_empty: bool = False) -> str:
        """문자열을 입력받는다. 기본은 빈 입력을 허용하지 않는다."""
        # TODO: _read 후 strip(). 비어 있고 allow_empty 가 False 면
        #       안내 후 다시 묻는다.
        while True:
            try:
                value = self._read(prompt).strip()
                if not value and not allow_empty:
                    self.warn("빈 입력은 허용되지 않습니다.")
                    continue
            except ExitSignal:
                raise ExitSignal()


    def ask_yes_no(self, prompt: str) -> bool:
        """y/n 확인. 삭제처럼 되돌릴 수 없는 동작 앞에 쓴다."""
        # TODO: _read 후 strip().lower() 가 "y"/"yes" 면 True,
        #       "n"/"no" 면 False, 그 외에는 안내 후 재입력.
        while True:
          try:
            value = self._read(prompt).strip()
            if value.lower() in ["y", "yes"]:
              return True
            elif value.lower() in ["n", "no"]:
              return False
            else:
              self.warn("잘못된 입력입니다. y 또는 n을 입력해주세요.")
              continue
          except ExitSignal:
            raise ExitSignal()

    def pause(self) -> None:
        """'엔터를 누르면 메뉴로 돌아갑니다' 대기."""
        # TODO: self._read("\n엔터를 누르면 메뉴로 돌아갑니다... ")
        raise NotImplementedError

    # ------------------------------------------------------------------
    # 출력 기능
    # ------------------------------------------------------------------
    def blank(self) -> None:
        print()

    def divider(self, thin: bool = False) -> None:
      if thin:
        print(THIN_LINE)
      else:
        print(LINE)

    def title(self, text: str) -> None:
        self.divider()
        self.text(text)
        self.divider()

    def text(self, message: str = "") -> None:
        print(message)

    def info(self, message: str) -> None:
        print(f"📌 {message}")

    def warn(self, message: str) -> None:
        print(f"⚠️ {message}")

    def success(self, message: str) -> None:
        print(f"✅ {message}")