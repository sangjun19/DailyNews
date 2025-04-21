from scrapers.university_notice import crawl_university_notices
from scrapers.department_notice import crawl_department_notices

if __name__ == "__main__":
    # notices = crawl_university_notices()
    notices = crawl_department_notices()
    for notice in notices[:5]:
        print(f"- {notice['title']} ({notice['date']})")
        print(f"  링크: {notice['link']}")
