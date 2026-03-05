import datetime

# 여기에 나중에 실제 미국 주식 API나 크롤링 코드가 들어갑니다.
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 기존 HTML 템플릿에 날짜만 갈아끼우는 예시
html_content = f"""
<html>
<head><title>AI Stock Report</title></head>
<body style="background: #1a1a1a; color: white; text-align: center;">
    <h1>📈 AI 증권팀 데일리 리포트</h1>
    <p>최종 업데이트 시간: {now} (UTC)</p>
    <p>현재 상태: 24시간 무인 가동 중</p>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
