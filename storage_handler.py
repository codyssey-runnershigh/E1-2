import json
import os

STATUS_OK = "ok"           # 정상적으로 읽음
STATUS_MISSING = "missing"  # 파일 없음, 기본 데이터로 실행
STATUS_BROKEN = "broken"    # 파일이 깨졌거나 json 형식 아님
DEFAULT_PATH = "state.json"

class Storage:
    """프로젝트 루트의 state.json 을 다룬다."""

    def __init__(self, path: str = DEFAULT_PATH) -> None:
        self.path = path

    # ------------------------------------------------------------------
    def exists(self) -> bool:
        """파일 존재 확인"""
        return os.path.exists(self.path)

    def load(self) :
        """
            파일 데이터 LOAD 및 validation
            데이터와 로드실패여부 반환
            실패: JSON 파싱 실패, 최상위가 dict 가 아님, "quizzes" 키가 없거나 list 가 아님, score는 보류
        """
        if not self.exists(): return None, STATUS_MISSING
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError, UnicodeDecodeError):
            return None, STATUS_BROKEN
        if not isinstance(data, dict) or not isinstance(data.get("quizzes"), list):
            return None, STATUS_BROKEN
        return data, STATUS_OK
