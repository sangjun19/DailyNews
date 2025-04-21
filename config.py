# 설정 파일
UNIVERSITY_NOTICE_URL = "https://computer.cnu.ac.kr/computer/index.do"
DEPARTMENT_NOTICE_URL = "https://computer.cnu.ac.kr/computer/notice/bachelor.do"
BUSINESS_NOTICE_URL = "https://computer.cnu.ac.kr/computer/notice/business.do"

# 크롤링 설정
MAX_NOTICES = 5
REQUEST_TIMEOUT = 10  # 초

# 응답 메시지 템플릿
UNIVERSITY_NOTICE_TEMPLATE = "📢 최근 학교 공지사항입니다:\n\n"
DEPARTMENT_NOTICE_TEMPLATE = "📢 최근 학과 공지사항입니다:\n\n"
BUSINESS_NOTICE_TEMPLATE = "📢 최근 사업단 소식입니다:\n\n"
