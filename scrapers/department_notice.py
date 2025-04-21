# 학과 공지사항 크롤링 모듈
from bs4 import BeautifulSoup
import requests
from scrapers.utils import clean_text, format_date

def crawl_department_notices():
    """학과 공지사항을 크롤링하는 함수"""
    url = "https://computer.cnu.ac.kr/computer/notice/bachelor.do"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        notices = []
        notice_table = soup.find('table', class_='board-table')
        
        if notice_table:
            # 테이블 내의 각 행(tr) 찾기
            rows = notice_table.find('tbody').find_all('tr')
            
            for row in rows:
                try:
                    # 기본값 설정
                    title = "제목 없음"
                    link = ""
                    author = "작성자 없음"
                    date = "날짜 없음"
                    views = "0"
                    is_notice = "일반"
                    
                    # 공지 여부 확인 (공지 아이콘이 있는지)
                    if row.find('span', class_='noti'):
                        is_notice = "공지"
                    
                    # 제목 추출 - a 태그 직접 찾기
                    a_tag = row.find('a')
                    if a_tag:
                        # 태그 내부 텍스트에서 제목 추출
                        title = a_tag.get_text(strip=True)
                        
                        # 링크 추출 - href 속성에서 상대 경로 가져오기
                        if 'href' in a_tag.attrs:
                            relative_link = a_tag['href']
                            # 상대 경로를 절대 경로로 변환
                            link = "https://computer.cnu.ac.kr/computer/notice/bachelor.do" + relative_link
                    
                    # 작성자, 등록일, 조회수 추출
                    cells = row.find_all('td')
                    if len(cells) >= 5:
                        author = cells[-3].get_text(strip=True)
                        date = cells[-2].get_text(strip=True)
                        views = cells[-1].get_text(strip=True)
                    
                    notices.append({
                        "type": is_notice,
                        "title": title,
                        "link": link,
                        "author": author,
                        "date": date,
                        "views": views
                    })
                except Exception as e:
                    print(f"행 처리 중 오류: {e}")
                    continue
        
        return notices
    
    except Exception as e:
        print(f"크롤링 오류: {e}")
        return []
    
