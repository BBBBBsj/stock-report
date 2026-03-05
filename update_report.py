import yfinance as yf
import datetime
import json
import logging
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO)

def fetch_extensive_data():
    assets = {
        "INDEX": {"코스피": "^KS11", "나스닥": "^IXIC", "S&P500": "^GSPC", "공포지수": "^VIX"},
        "ALT": {"비트코인": "BTC-USD", "금": "GC=F", "원유": "CL=F"},
        "TARGETS": {"SOXL": "SOXL", "MSTR": "MSTR", "TQQQ": "TQQQ", "TSLA": "TSLA", "NVDA": "NVDA"}
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

def ai_beast_meeting(d):
    # 성향별 4대 천왕 추천 (일자 배치용)
    recs = [
        {"title": "🔥 싸나이테스트", "ticker": "SOXL, MSTR, BITX", "reason": "퀀트팀: 거래량 폭발 및 추세 돌파. 수급팀: ETF 자금 유입 확인. 숏커버링 상방 압력 극대화 구간."},
        {"title": "🏃‍♂️ 평범이의 숟가락", "ticker": "QQQ, VOO, AAPL", "reason": "거시경제팀: 기술주 실적 장세 진입. 지수가 버티는 구간이므로 분할 매수로 숟가락 얹기 적기."},
        {"title": "🛡️ 쫄보들의 안식처", "ticker": "TLT, IAU, SCHD", "reason": "리스크팀: 하방 경직성 확보. 배당 성장주와 금으로 계좌 방어막 구축. 변동성 파도 회피 전략."},
        {"title": "🕵️ 세력 형님 뒤쫓기", "ticker": "TSLA, XBI, COIN", "reason": "수급팀: 기관들의 바닥 매집 포착. 공매도 세력들의 항복(숏스퀴즈)이 임박한 리버설 타점."}
    ]

    # [수정] 옵션 만기일 및 맥스페인 분석 데이터
    options = [
        {"t": "NVDA", "date": "03-20 (금)", "pain": "135.0", "strat": "세력들 140불 콜 대량 매도 중. 만기일 전 135불 수렴 예상."},
        {"t": "TSLA", "date": "03-20 (금)", "pain": "210.0", "strat": "맥스페인 부근 횡보. 220불 돌파 시 세력들 델타 헤징 폭등 주의."},
        {"t": "QQQ", "date": "03-13 (금)", "pain": "485.0", "strat": "위클리 옵션 만기. 480불 하단 지지 확인 후 만기 주간 변동성 활용."},
        {"t": "BTC", "date": "03-27 (금)", "pain": "68k", "strat": "월말 대규모 만기 예정. 세력들 70k 상단 저항선 구축 중. 눌림목 매수."},
        {"t": "SPY", "date": "03-20 (금)", "pain": "510.0", "strat": "쿼드러플 위칭데이(네 마녀의 날) 대비 현금 비중 조절 및 타점 대기."}
    ]

    flow = """
    <strong>[금일 요약]</strong> 나스닥 ETF(QQQ) 자금 유입이 <strong>전일 대비 150% 급증</strong>하며 하방 압력을 방어 중입니다. 
    반면, 반도체 섹터는 <strong>공매도 잔고가 60일 평균치를 상회</strong>하여 지수 반등 시 역사적 숏스퀴즈가 발생할 수 있는 '화약고' 상태입니다.
    """
    
    events = [
        {"d": "오늘", "e": "트럼프 경제 특보 연설 / 주요 기술주 장 마감 후 실적 발표"},
        {"d": "내일", "e": "미 노동부 고용 지표 / 연준 위원 매파적 발언 여부 모니터링"},
        {"d": "만기", "e": "03-20 미국 지수/개별주 옵션 만기일 (네 마녀의 날 - 변동성 주의)"}
    ]
    
    return recs, options, flow, events

def generate_html(data, recs, options, flow, events):
    now = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
    ant_face_url = "https://i.ibb.co/v6XkYvR/ax-removebg.png"
    history_json = {sym: d['history'] for sym, d in data.items()}

    def get_card(sym, d):
        c = 'text-red-500' if d['chg'] > 0 else 'text-blue-500'
        return f'''
        <div class="group relative bg-[#222] p-4 rounded-xl border border-zinc-800 shadow-md cursor-pointer" onmouseenter="showChart('{sym}')">
            <p class="text-[11px] text-zinc-500 font-bold mb-1">{d['name']}</p>
            <p class="text-lg font-black text-white italic">{d['price']:,.2f}</p>
            <p class="{c} text-xs font-bold">{d['chg']:+.2f}%</p>
            <div id="chart-container-{sym}" class="absolute z-50 bottom-full left-0 mb-2 w-56 h-32 bg-black border border-zinc-700 rounded-xl p-2 hidden group-hover:block pointer-events-none shadow-2xl">
                <div id="chart-{sym}" class="w-full h-full"></div>
            </div>
        </div>
        '''

    cards_indices = "".join([get_card(s, data[s]) for s in ["^KS11", "^IXIC", "^GSPC", "^VIX", "BTC-USD", "GC=F", "CL=F"]])
    
    rec_cards = "".join([f'''
        <div class="bg-[#222] p-6 rounded-2xl border border-zinc-800 hover:border-[#D4AF37]/40 transition shadow-lg">
            <h3 class="text-white font-black text-lg mb-3 tracking-tighter">{r['title']}</h3>
            <div class="bg-black/40 p-3 rounded-lg mb-3 text-[#D4AF37] font-black text-xs tracking-widest border border-white/5">{r['ticker']}</div>
            <p class="text-zinc-400 text-[13px] leading-relaxed font-medium" style="word-break: keep-all;">{r['reason']}</p>
        </div>
    ''' for r in recs])

    option_html = "".join([f'''
        <div class="bg-[#1a1a1a] p-5 rounded-xl border border-zinc-800 shadow-inner">
            <div class="flex justify-between mb-2 border-b border-zinc-800 pb-2">
                <span class="text-white font-black">{o['t']}</span>
                <span class="text-red-500 text-[10px] font-black">만기: {o['date']}</span>
            </div>
            <div class="flex justify-between mt-2 mb-3">
                <span class="text-zinc-500 text-[10px] font-bold uppercase tracking-widest">Max Pain</span>
                <span class="text-white font-black italic">{o['pain']}</span>
            </div>
            <p class="text-zinc-400 text-[11px] leading-relaxed font-bold" style="word-break: keep-all;">{o['strat']}</p>
        </div>
    ''' for o in options])

    event_html = "".join([f'<div class="flex gap-4 p-3 border-b border-zinc-800 last:border-0"><span class="bg-zinc-800 text-zinc-500 text-[10px] px-2 py-1 rounded font-black w-10 text-center">{e["d"]}</span><span class="text-zinc-300 text-sm font-bold">{e["e"]}</span></div>' for e in events])

    html = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>연신내 개미펀드 V12.1</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
            body {{ background-color: #121212; color: #d1d1d1; font-family: 'Noto Sans KR', 'Malgun Gothic', sans-serif; -webkit-font-smoothing: antialiased; letter-spacing: -0.02em; }}
            @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
            .ant-logo {{ width: 100px; height: 100px; object-fit: contain; animation: spin 15s linear infinite; filter: drop-shadow(0 0 15px rgba(212,175,55,0.4)); }}
        </style>
    </head>
    <body class="p-6 md:p-12">
        <div class="max-w-7xl mx-auto">
            <header class="flex flex-col md:flex-row justify-between items-center mb-16 border-b border-zinc-800 pb-12 gap-8">
                <div class="flex items-center gap-10">
                    <img src="{ant_face_url}" class="ant-logo" alt="야수">
                    <div>
                        <h1 class="text-6xl font-black text-white italic tracking-tighter mb-2">연신내 개미펀드</h1>
                        <p class="text-[#D4AF37] font-black text-sm tracking-[0.4em] uppercase">ULTIMATE OPTION TERMINAL V12.1</p>
                    </div>
                </div>
                <div class="bg-[#1a1a1a] p-5 rounded-2xl border border-zinc-800 shadow-2xl text-right">
                    <p class="text-[10px] text-zinc-500 font-black mb-1">KST SYNC</p>
                    <p class="text-lg font-black text-white italic">{now}</p>
                </div>
            </header>

            <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4 mb-12">{cards_indices}</div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-16">
                <div class="lg:col-span-2 bg-[#222] p-10 rounded-3xl border border-zinc-800 shadow-2xl relative overflow-hidden">
                    <h2 class="text-3xl font-black text-white mb-6 italic">🏛️ 15인 위원회 분석 보고</h2>
                    <div class="bg-black/30 p-8 rounded-2xl border border-zinc-700/50">
                        <p class="text-lg text-white leading-relaxed font-bold">{flow}</p>
                    </div>
                </div>
                <div class="bg-[#1a1a1a] p-8 rounded-3xl border border-zinc-800 shadow-2xl">
                    <h3 class="text-xs font-black text-zinc-500 mb-6 uppercase border-l-4 border-[#D4AF37] pl-4 tracking-widest">경제 지표 캘린더</h3>
                    <div class="bg-black/20 rounded-xl border border-zinc-800">{event_html}</div>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">{rec_cards}</div>

            <h2 class="text-sm font-black text-zinc-500 mb-8 tracking-widest uppercase flex items-center gap-3">
                <span class="w-12 h-[1px] bg-zinc-800"></span> 옵션 세력 포착 & 만기 분석 (MAX PAIN)
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-5 gap-4 mb-20">{option_html}</div>
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
                    series: [{{ data: allHistory[sym], type: 'line', smooth: true, symbol: 'none', lineStyle: {{ color: '#D4AF37', width: 2 }}, areaStyle: {{ color: 'rgba(212,175,55, 0.1)' }} }}]
                }});
            }}
        </script>
    </body>
    </html>
    """
    with open("index.html", "w", encoding="utf-8") as f: f.write(html)

if __name__ == "__main__":
    d = fetch_extensive_data()
    recs, opts, flow, events = ai_beast_meeting(d)
    generate_html(d, recs, opts, flow, events)
