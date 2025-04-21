# 학교 전체 공지사항 크롤링 모듈
from bs4 import BeautifulSoup
import requests
from .utils import clean_text, format_date

def crawl_university_notices():
    """학교 전체 공지사항을 크롤링하는 함수"""
    url = "https://computer.cnu.ac.kr/computer/index.do"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        notices = []
        notice_divs = [div for div in soup.find_all('div') if div.get('class') and any('box-notice' in c for c in div.get('class'))]
        
        for div in notice_divs:
            a_tag = div.find('a')
            if a_tag:
                title_tag = a_tag.find('h3', class_='t1')
                date_tag = a_tag.find('p')
                if title_tag and date_tag:
                    title = title_tag.text.strip()
                    link = a_tag.get('href')
                    date = date_tag.text.replace('등록일:', '').strip()
                    notices.append({"title": title, "link": link, "date": date})
            
        return notices
    
    except Exception as e:
        print(f"크롤링 오류: {e}")
        return []
