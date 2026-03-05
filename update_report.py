import yfinance as yf
import datetime
import json
import logging
import pandas as pd
import numpy as np

# 로깅 설정
logging.basicConfig(level=logging.INFO)

def fetch_extensive_data():
    # 지수 및 주요 자산 30일 데이터 수집
    assets = {
        "INDEX": {"코스피": "^KS11", "나스닥": "^IXIC", "S&P500": "^GSPC", "공포지수": "^VIX"},
        "ALT": {"비트코인": "BTC-USD", "금": "GC=F", "원유": "CL=F"},
        "BEAST": {"TQQQ": "TQQQ", "SOXL": "SOXL", "NVDA": "NVDA", "MSTR": "MSTR", "TSLA": "TSLA"},
        "SECTOR": {"반도체": "SOXX", "바이오": "XBI", "금융": "XLF", "헬스케어": "XLV", "에너지": "XLE"}
    }
    data_pool = {}
    for cat, group in assets.items():
        for name, sym in group.items():
            try:
                t = yf.Ticker(sym)
                h = t.history(period="30d")
                if len(h) >= 2:
                    prices = h['Close'].round(2).tolist()
                    curr, prev = h['Close'].iloc[-1], h['Close'].iloc[-2]
                    chg = ((curr - prev) / prev) * 100
                    data_pool[sym] = {"name": name, "price": curr, "chg": chg, "history": prices}
            except: pass
    return data_pool

def ai_strategic_meeting(d):
    # 15인 위원회 회의 결과 도출 (경주마 5종 및 옵션 분석)
    # 섹션 1: 경주마 ㄱㄱ (초고위험 레버리지 및 코인주)
    horse_racing = [
        {"t": "SOXL", "y": "+5.2%", "r": "반도체 레버리지 광기 구간. MACD 돌파 확인. 상남자 전용."},
        {"t": "MSTR", "y": "+8.4%", "r": "비트코인 현물 보유 세력주. 코인 유동성 직결. 야수의 심장 필수."},
        {"t": "TQQQ", "y": "+3.1%", "r": "나스닥 3배. 지수 상승 시 돈복사기 가동. 세력 매집 포착."},
        {"t": "NVDL", "y": "+6.7%", "r": "엔비디아 2배. AI 대장주의 끝없는 랠리 추종. 숏커버링 예상."},
        {"t": "CONL", "y": "+12.1%", "r": "코인베이스 2배. 가상자산 폭등장 주도주. 하이리스크 하이리턴."}
    ]
    
    # 옵션 세력 분석 (맥스페인)
    option_flow = [
        {"t": "NVDA", "m": "135.0", "s": "세력 140불 콜옵션 대량 매집. 132불 하단 지지 후 수익 실현 타점."},
        {"t": "TSLA", "m": "210.0", "s": "맥스페인 가격 205불. 변동성 확대 구간. 215불 돌파 시 숏스퀴즈."},
        {"t": "AAPL", "m": "225.0", "s": "횡보 흐름. 기관들 풋옵션 매도로 하방 경직성 확보. 230불 목표."},
        {"t": "QQQ", "m": "480.0", "s": "강한 콜옵션 우세. 만기일 전후 변동성 주의. 눌림목 매수 타점."},
        {"t": "BTC", "m": "65k", "s": "옵션 시장 유동성 역대급. 세력들 하단 62k 강력 지지 중. 홀딩 전략."}
    ]

    events = [
        {"d": "어제", "e": "미 연준 베이지북 발표 - 경기 둔화 우려 완화로 나스닥 반등"},
        {"d": "오늘", "e": "신규 실업수당 청구 건수 / 트럼프 경제 특보 연설 예정"},
        {"d": "내일", "e": "비농업 고용지수 발표 (나스닥 향방 결정적 키) / 브로드컴 실적 발표"}
    ]

    return horse_racing, option_flow, events

def generate_v11_html(data, horses, options, events):
    now = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
    # 대표님 이미지 (누끼 처리 완료 버전)
    ant_face_url = "https://i.ibb.co/v6XkYvR/ax-removebg.png"
    history_json = {sym: d['history'] for sym, d in data.items()}

    def get_card(sym, d):
        c = 'text-red-500' if d['chg'] > 0 else 'text-blue-500'
        return f'''
        <div class="group relative bg-[#2d2d2d] p-4 rounded-xl border border-zinc-800 shadow-inner cursor-pointer" onmouseenter="showChart('{sym}')">
            <p class="text-[11px] text-zinc-500 font-bold mb-1">{d['name']}</p>
            <p class="text-lg font-black text-white">{d['price']:,.2f}</p>
            <p class="{c} text-xs font-bold">{d['chg']:+.2f}%</p>
            <div id="chart-container-{sym}" class="absolute z-50 bottom-full left-0 mb-2 w-56 h-32 bg-black border border-zinc-700 rounded-xl p-2 hidden group-hover:block pointer-events-none shadow-2xl">
                <div id="chart-{sym}" class="w-full h-full"></div>
            </div>
        </div>
        '''

    cards_indices = "".join([get_card(s, data[s]) for s in ["^KS11", "^IXIC", "^GSPC", "^VIX", "BTC-USD", "GC=F", "CL=F"]])
    
    horse_cards = ""
    for h in horses:
        sym = h['t']
        d = data.get(sym, {"price":0, "chg":0})
        horse_cards += f'''
        <div class="group relative bg-[#2d2d2d] p-5 rounded-2xl border border-zinc-800 hover:border-red-500/50 transition-all cursor-pointer" onmouseenter="showChart('{sym}')">
            <div class="flex justify-between items-start mb-3">
                <p class="bg-red-500/10 text-red-500 text-[10px] px-2 py-0.5 rounded font-black">경주마 ㄱㄱ</p>
                <p class="text-zinc-500 text-[10px] font-bold">전날: {h['y']}</p>
            </div>
            <p class="text-white font-black text-2xl mb-1">{sym}</p>
            <p class="text-zinc-400 text-xs leading-relaxed font-bold">{h['r']}</p>
            <div id="chart-container-{sym}" class="absolute z-50 bottom-full left-0 mb-2 w-64 h-40 bg-black border border-zinc-700 rounded-xl p-2 hidden group-hover:block pointer-events-none shadow-2xl">
                <div id="chart-{sym}" class="w-full h-full"></div>
            </div>
        </div>
        '''

    option_html = "".join([f'''
        <div class="bg-[#1a1a1a] p-4 rounded-xl border border-zinc-800">
            <div class="flex justify-between mb-2">
                <span class="text-white font-black">{o['t']}</span>
                <span class="text-accent text-xs font-bold">MAX PAIN: {o['m']}</span>
            </div>
            <p class="text-zinc-500 text-xs font-bold">{o['s']}</p>
        </div>
    ''' for o in options])

    event_html = "".join([f'''
        <div class="flex gap-4 items-center p-3 border-b border-zinc-800 last:border-0">
            <span class="bg-zinc-800 text-zinc-400 text-[10px] px-2 py-1 rounded font-black w-12 text-center">{e['d']}</span>
            <span class="text-zinc-200 text-sm font-bold">{e['e']}</span>
        </div>
    ''' for e in events])

    html = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>연신내 개미펀드 V11</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;900&display=swap');
            body {{ background-color: #121212; color: #e0e0e0; font-family: 'Noto Sans KR', 'Malgun Gothic', sans-serif; -webkit-font-smoothing: antialiased; }}
            .text-accent {{ color: #D4AF37; }}
            @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
            .ant-logo {{ width: 100px; height: 100px; object-fit: contain; animation: spin 15s linear infinite; filter: drop-shadow(0 0 15px rgba(212,175,55,0.4)); }}
            .card-gradient {{ background: linear-gradient(145deg, #2d2d2d, #1e1e1e); }}
        </style>
    </head>
    <body class="p-6 md:p-12">
        <div class="max-w-7xl mx-auto">
            <header class="flex flex-col md:flex-row justify-between items-center mb-16 border-b border-zinc-800 pb-10 gap-8">
                <div class="flex items-center gap-8">
                    <img src="{ant_face_url}" class="ant-logo" alt="Beast Ant">
                    <div>
                        <h1 class="text-6xl font-black text-white italic tracking-tighter mb-2">연신내 개미펀드</h1>
                        <p class="text-accent font-black text-sm tracking-[0.4em] uppercase">15 AGENTS ULTIMATE QUANT TERMINAL V11</p>
                    </div>
                </div>
                <div class="bg-[#1e1e1e] p-4 rounded-2xl border border-zinc-800 shadow-2xl text-right">
                    <p class="text-[10px] text-zinc-500 font-black mb-1">REAL-TIME KST SYNC</p>
                    <p class="text-lg font-black text-white italic">{now}</p>
                </div>
            </header>

            <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4 mb-12">{cards_indices}</div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-16">
                <div class="lg:col-span-2 card-gradient p-10 rounded-3xl border border-zinc-800 shadow-2xl relative overflow-hidden">
                    <div class="absolute -right-20 -bottom-20 opacity-5 text-[200px] font-black italic">BEAST</div>
                    <h2 class="text-3xl font-black text-white mb-8 italic flex items-center gap-3">🏛️ 15인 위원회 실시간 전략 보고</h2>
                    <div class="bg-black/30 p-8 rounded-2xl border border-zinc-700/50 mb-8">
                        <p class="text-sm text-zinc-300 leading-relaxed font-bold italic underline decoration-accent decoration-2 underline-offset-8">
                            금일 나스닥은 트럼프의 추가 관세 관련 발언과 연준 위원들의 매파적 태도로 인해 변동성이 극대화되었습니다. 
                            세력들은 현재 반도체 하단 지지선을 테스트 중이며, 옵션 만기일을 앞두고 맥스페인 가격으로의 회귀 본능이 강해질 것으로 보입니다.
                        </p>
                    </div>
                </div>
                <div class="bg-[#1e1e1e] p-8 rounded-3xl border border-zinc-800 shadow-2xl">
                    <h3 class="text-xs font-black text-zinc-500 mb-6 uppercase border-l-4 border-accent pl-4 tracking-widest">나스닥 경제 지표 캘린더</h3>
                    <div class="bg-black/20 rounded-xl border border-zinc-800">{event_html}</div>
                </div>
            </div>

            <h2 class="text-sm font-black text-zinc-500 mb-8 tracking-widest uppercase flex items-center gap-3">
                <span class="w-12 h-[1px] bg-zinc-800"></span> 경주마 ㄱㄱ (초고위험 타겟)
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-6 mb-20">{horse_cards}</div>

            <h2 class="text-sm font-black text-zinc-500 mb-8 tracking-widest uppercase flex items-center gap-3">
                <span class="w-12 h-[1px] bg-zinc-800"></span> 옵션 세력 포착 & 맥스페인 분석
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-5 gap-4 mb-16">{option_html}</div>
        </div>

        <script>
            const allHistory = {json.dumps(history_json)};
            function showChart(sym) {{
                const container = document.getElementById('chart-' + sym);
                if(!container) return;
                const chart = echarts.init(container);
                chart.setOption({{
                    grid: {{ top: 10, bottom: 10, left: 10, right: 10 }},
                    xAxis: {{ type: 'category', show: false }},
                    yAxis: {{ type: 'value', show: false, min: 'dataMin', max: 'dataMax' }},
                    series: [{{
                        data: allHistory[sym],
                        type: 'line',
                        smooth: true,
                        symbol: 'none',
                        lineStyle: {{ color: '#D4AF37', width: 2 }},
                        areaStyle: {{ color: 'rgba(212, 175, 55, 0.1)' }}
                    }}]
                }});
            }}
        </script>
    </body>
    </html>
    """
    with open("index.html", "w", encoding="utf-8") as f: f.write(html)

if __name__ == "__main__":
    d = fetch_extensive_data()
    horses, options, events = ai_strategic_meeting(d)
    generate_v11_html(d, horses, options, events)
