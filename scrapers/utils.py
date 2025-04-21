# 공통 유틸리티 함수
import re
from datetime import datetime

def clean_text(text):
    """텍스트 정리 함수"""
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()

def format_date(date_str):
    """날짜 포맷을 'YYYY-MM-DD' 형식으로 통일하는 함수"""
    if not date_str:
        return ""
        
    # 다양한 날짜 형식 처리
    date_formats = [
        '%Y년 %m월 %d일',  # 2025년 04월 20일
        '%Y-%m-%d',       # 2025-04-20
        '%Y.%m.%d',       # 2025.04.20
        '%Y/%m/%d',       # 2025/04/20
        '%m/%d/%Y',       # 04/20/2025
        '%d-%m-%Y',       # 20-04-2025
        '%B %d, %Y',      # April 20, 2025
        '%d %B %Y',       # 20 April 2025
    ]
    
    # 숫자와 구분자만 남기기
    cleaned_date = re.sub(r'[^\d/\-\.\s년월일]', '', date_str)
    
    # 다양한 형식 시도
    for fmt in date_formats:
        try:
            date_obj = datetime.strptime(cleaned_date, fmt)
            return date_obj.strftime('%Y-%m-%d')  # YYYY-MM-DD 형식으로 반환
        except ValueError:
            continue
    
    # 모든 형식 변환 실패 시 원본 반환
    return date_str
