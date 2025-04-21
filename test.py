from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# 학과 공지사항 크롤링 함수
def crawl_department_notices():
    url = "https://computer.cnu.ac.kr/computer/notice/bachelor.do"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        notices = []
        # 공지사항 테이블 찾기
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



# 카카오 스킬 API 응답 형식
@app.route('/api/department-notices', methods=['POST'])
def get_department_notices():
    # 요청 데이터 파싱
    req = request.get_json()
    
    # 크롤링 함수 호출
    notices = crawl_department_notices()[:5]  # 최근 5개 공지만 가져옴
    
    if not notices:
        # 크롤링 실패 시 응답
        response = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "학과 공지사항을 가져오는 중 오류가 발생했습니다."
                        }
                    }
                ]
            }
        }
    else:
        # 응답 메시지 구성
        message = "📢 최근 학과 공지사항입니다:\n\n"
        for notice in notices:
            if notice["type"] == "공지":
                message += f"[공지] {notice['title']} ({notice['date']})\n작성자: {notice['author']} | 조회수: {notice['views']}\n\n"
            else:
                message += f"• {notice['title']} ({notice['date']})\n작성자: {notice['author']} | 조회수: {notice['views']}\n\n"
        
        # 카카오 스킬 응답 형식으로 반환
        response = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": message
                        }
                    }
                ]
            }
        }
    
    return jsonify(response)

# 테스트 함수
def test_crawl_department_notices():
    notices = crawl_department_notices()
    print("학과 공지사항 크롤링 테스트 결과 (최대 5개):")
    for i, notice in enumerate(notices[:10]):
        print(f"{i+1}. {'[공지] ' if notice['type'] == '공지' else ''}{notice['title']} ({notice['date']})")
        print(f"   작성자: {notice['author']} | 조회수: {notice['views']}")
        print(f"   링크: {notice['link']}")
        print()
    return notices

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=8080)
    test_crawl_department_notices()
