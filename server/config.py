import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수 가져오기
DEEPL_API_KEY = os.getenv('DEEPL_API_KEY')
SDWEBUI_API = os.getenv('SDWEBUI_API')

# 필요한 경우 기본값 설정
if not DEEPL_API_KEY:
    raise ValueError('DEEPL_API_KEY environment variable is missing.')
if not SDWEBUI_API:
    raise ValueError("SDWEBUI_API is not set in the environment variables")


# 설정 클래스 정의 (선택사항)
class Config:
    DEEPL_API_KEY = DEEPL_API_KEY
    SDWEBUI_API = SDWEBUI_API

