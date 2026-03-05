import yfinance as yf
import datetime
import logging
import pandas as pd
import numpy as np

# [생략: 데이터 수집 로직은 동일]

def generate_v8_1_html(data, recs, flow, warn):
    now = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
    
    # 누끼 작업 완료된 대표님 이미지
    ant_face_url = "https://i.ibb.co/v6XkYvR/ax-removebg.png"

    html = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>연신내 개미 펀드 V8.1</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
            body {{ background-color: #1e1e1e; color: #c4c4c4; font-family: 'Inter', sans-serif; transition: 0.3s; }}
            
            /* 핵심: 빙글빙글 도는 애니메이션 정의 */
            @keyframes spin {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
            
            .ant-logo {{ 
                width: 70px; 
                height: 70px; 
                object-fit: contain; 
                filter: drop-shadow(0 0 8px rgba(255,255,255,0.3)); 
                /* 애니메이션 적용: 10초마다 한 바퀴, 무한 반복 */
                animation: spin 10s linear infinite; 
            }}
            
            /* [이하 동일] */
    """
    # [중략]
    with open("index.html", "w", encoding="utf-8") as f: f.write(html)

# [실행 로직]
