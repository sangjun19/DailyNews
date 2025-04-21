from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# 학교 공지사항 크롤링 함수
def crawl_school_notices():
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
        
        print("크롤링 테스트 결과 (최대 5개):")
        for notice in notices[:10]:
            print(f"- {notice['title']} ({notice['date']})")
            print(f"  링크: {notice['link']}")
        
        return notices
        

    except Exception as e:
        print(f"크롤링 오류: {e}")
        return []


# 카카오 스킬 API 응답 형식
@app.route('/api/notices', methods=['POST'])
def get_notices():
    # 요청 데이터 파싱
    req = request.get_json()
    
    # 크롤링 함수 호출
    notices = crawl_school_notices()[:5]  # 최근 5개 공지만 가져옴
    
    if not notices:
        # 크롤링 실패 시 응답
        response = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "공지사항을 가져오는 중 오류가 발생했습니다."
                        }
                    }
                ]
            }
        }
    else:
        # 응답 메시지 구성
        message = "📢 최근 학교 공지사항입니다:\n\n"
        for notice in notices:
            message += f"• {notice['title']} ({notice['date']})\n"
        
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

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=8080)
    crawl_school_notices()