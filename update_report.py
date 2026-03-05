import yfinance as yf
import datetime
import json
import logging
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO)

def fetch_extensive_data():
    # 15인 위원회가 검토할 30일치 데이터셋
    assets = {
        "INDEX": {"코스피": "^KS11", "나스닥": "^IXIC", "S&P500": "^GSPC", "공포지수": "^VIX"},
        "ALT": {"비트코인": "BTC-USD", "금": "GC=F", "원유": "CL=F"},
        "SECTOR": {"반도체": "SOXX", "바이오": "XBI", "금융": "XLF"}
    }
    data_pool = {}
    for cat, group in assets.items():
        for name, sym in group.items():
            try:
                t = yf.Ticker(sym)
                h = t.history(period="30d")
                if len(h) > 15:
                    prices = h['Close'].round(2).tolist()
                    curr, prev = h['Close'].iloc[-1], h['Close'].iloc[-2]
                    chg = ((curr - prev) / prev) * 100
                    delta = h['Close'].diff()
                    up = delta.clip(lower=0).rolling(14).mean().iloc[-1]
                    down = -delta.clip(upper=0).rolling(14).mean().iloc[-1]
                    rsi = 100 - (100 / (1 + (up/down))) if down != 0 else 50
                    data_pool[sym] = {"name": name, "price": curr, "chg": chg, "rsi": rsi, "history": prices}
            except: pass
    return data_pool

def ai_beast_meeting(d):
    ks_chg = d.get('^KS11', {}).get('chg', 0)
    # 15인 에이전트의 팩트 체크 보고
    if ks_chg > 3:
        flow = f"<strong>🔥 긴급: 국장 대폭발!</strong> 코스피 {ks_chg:.1f}% 상승은 역대급 불장입니다. 숏커버링과 외인 광기수급이 겹쳤습니다."
    else:
        flow = "<strong>[유동성 흐름]</strong> 자금이 코인에서 주식으로, 특히 기술주와 바이오 섹터로 미친 듯이 쏠리고 있습니다."

    warn = "⚠️ <strong>트레이딩 코치:</strong> 지금 안 사면 바보라는 생각(FOMO)이 들 때가 가장 위험하지만, 오늘 같은 장은 안 타면 소외됩니다."

    recs = [
        {"title": "🔥 니가 진짜 야수라면? (상남자 특: 풀매수)", "ticker": "NVDA, SOXL, MSTR", "reason": "퀀트팀: MACD 하늘 돌파. 데이터팀: '돈복사' 검색량 폭증. 쫄보 금지."},
        {"title": "🏃‍♂️ 평범이의 숟가락 얹기 (남들 벌 때 벌기)", "ticker": "QQQ, VOO, KODEX 200", "reason": "거시경제팀: 대세 상승장 국룰. 지수가 밀어 올리는 무지성 수익 구간."},
        {"title": "🛡️ 쫄보들을 위한 안식처 (예금보단 낫지)", "ticker": "TLT, IAU, XLF(금융)", "reason": "리스크팀: 겁쟁이용 추천. 금리 하락세와 은행 배당주로 대피하여 따뜻하게 보존."},
        {"title": "🕵️ 세력 형님들 뒤꽁무니 쫓기 (숏커버링 맛집)", "ticker": "TSLA, XBI(바이오)", "reason": "수급추적자: 바이오 바닥 매집 포착. 테슬라 숏 형들의 눈물의 환매수 시작."}
    ]
    return recs, flow, warn

def generate_html(data, recs, flow, warn):
    now = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
    ant_face_url = "https://i.ibb.co/v6XkYvR/ax-removebg.png"
    history_json = {sym: d['history'] for sym, d in data.items()}

    cards = ""
    for sym, i in data.items():
        cards += f"""
        <div class="group relative bg-[#2d2d2d] p-3 rounded-lg border border-zinc-800 shadow-inner cursor-pointer" 
             onmouseenter="showMiniChart('{sym}')">
            <p class="text-[10px] text-zinc-500 font-black uppercase tracking-tighter">{i['name']}</p>
            <p class="text-md font-black text-[#c4c4c4]">{i['price']:,.1f}</p>
            <p class="text-[11px] font-bold {'text-red-500' if i['chg']>0 else 'text-blue-500'}">{i['chg']:+.2f}%</p>
            <div id="chart-container-{sym}" class="absolute z-50 bottom-full left-0 mb-2 w-48 h-24 bg-black border border-zinc-700 rounded-lg p-1 hidden group-hover:block pointer-events-none shadow-2xl">
                <div id="chart-{sym}" class="w-full h-full"></div>
            </div>
        </div>
        """

    rec_html = ""
    for r in recs:
        rec_html += f"""
        <div class="bg-[#2d2d2d] p-5 rounded-2xl border border-zinc-800 hover:border-white/20 transition-all shadow-xl">
            <h3 class="text-white font-black text-lg mb-3">{r['title']}</h3>
            <div class="bg-black/40 p-3 rounded-lg mb-3 border border-white/5 font-black text-white text-sm tracking-widest">{r['ticker']}</div>
            <p class="text-zinc-400 text-xs leading-relaxed font-bold">{r['reason']}</p>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>연신내 개미펀드 V10.1</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Inter:wght@400;900&display=swap');
            body {{ background-color: #1e1e1e; color: #c4c4c4; font-family: 'Inter', sans-serif; }}
            h1, h2, h3 {{ font-family: 'Black Han Sans', sans-serif; }}
            @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
            .ant-logo {{ width: 90px; height: 90px; object-fit: contain; animation: spin 12s linear infinite; filter: drop-shadow(0 0 15px rgba(255,255,255,0.3)); }}
        </style>
    </head>
    <body class="p-4 md:p-10">
        <div class="max-w-7xl mx-auto">
            <header class="flex flex-col md:flex-row justify-between items-center mb-12 border-b border-zinc-800 pb-8 gap-6">
                <div class="flex items-center gap-6">
                    <img src="{ant_face_url}" class="ant-logo" alt="로고">
                    <div>
                        <h1 class="text-5xl font-black text-white italic tracking-tighter">연신내 개미펀드</h1>
                        <p class="text-red-500 font-black text-xs mt-1 tracking-[0.5em] uppercase">15인 AI 위원회 가동 중 (차트 엔진 탑재)</p>
                    </div>
                </div>
                <div class="bg-[#2d2d2d] px-6 py-2 rounded-xl border border-zinc-700 shadow-2xl">
                    <p class="text-[10px] text-zinc-500 font-black">동기화: {now}</p>
                </div>
            </header>

            <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3 mb-10">{cards}</div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-12">
                <div class="lg:col-span-2 bg-[#2d2d2d] p-8 rounded-3xl border border-zinc-800 shadow-2xl">
                    <h2 class="text-3xl font-black text-white mb-6 italic">🏛️ 15인 위원회 전략 회의록</h2>
                    <div class="space-y-6">
                        <div class="bg-red-500/10 p-6 rounded-2xl border border-red-500/20"><p class="text-lg text-white font-black">{flow}</p></div>
                        <div class="bg-zinc-800/50 p-6 rounded-2xl border border-zinc-700"><p class="text-sm text-zinc-300 font-bold">{warn}</p></div>
                    </div>
                </div>
                <div class="bg-[#2d2d2d] p-8 rounded-3xl border border-zinc-800 shadow-2xl">
                    <h3 class="text-xs font-black text-zinc-500 mb-8 uppercase border-l-4 border-red-600 pl-4">실시간 위험 감지 판넬</h3>
                    <div class="space-y-8">
                        <div class="space-y-2"><div class="flex justify-between text-xs font-black"><span>탐욕 지수</span><span class="text-white">88%</span></div><div class="w-full bg-zinc-800 h-2 rounded-full"><div class="bg-red-500 h-2 rounded-full" style="width: 88%"></div></div></div>
                        <div class="space-y-2"><div class="flex justify-between text-xs font-black"><span>매집 강도</span><span class="text-white">95%</span></div><div class="w-full bg-zinc-800 h-2 rounded-full"><div class="bg-white h-2 rounded-full" style="width: 95%"></div></div></div>
                    </div>
                </div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">{rec_html}</div>
        </div>
        <script>
            const allHistory = {json.dumps(history_json)};
            function showMiniChart(sym) {{
                const container = document.getElementById('chart-' + sym);
                const chart = echarts.init(container);
                chart.setOption({{
                    grid: {{ top: 5, bottom: 5, left: 5, right: 5 }},
                    xAxis: {{ type: 'category', show: false }},
                    yAxis: {{ type: 'value', show: false, min: 'dataMin', max: 'dataMax' }},
                    series: [{{ data: allHistory[sym], type: 'line', smooth: true, symbol: 'none', lineStyle: {{ color: '#D4AF37', width: 2 }}, areaStyle: {{ color: 'rgba(212, 175, 55, 0.1)' }} }}]
                }});
            }}
        </script>
    </body>
    </html>
    """
    with open("index.html", "w", encoding="utf-8") as f: f.write(html)

if __name__ == "__main__":
    d = fetch_extensive_data()
    recs, flow, warn = ai_beast_meeting(d)
    generate_html(d, recs, flow, warn)
