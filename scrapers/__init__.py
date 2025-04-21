# scrapers/__init__.py
__all__ = ['university_notice', 'department_notice', 'business_notice']

# 편의를 위한 직접 임포트 제공
from .university_notice import crawl_university_notices
from .department_notice import crawl_department_notices
from .business_notice import crawl_business_notices
