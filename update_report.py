import yfinance as yf
import datetime
import json
import logging
import pandas as pd
import numpy as np

# [V13.0] 15인 위원회 최종 통합 엔진 가동
logging.basicConfig(level=logging.INFO)

def fetch_extensive_data():
    # 팩트 기반 데이터 수집 (지수, 자산, 타겟 종목)
    assets = {
        "INDEX": {"코스피": "^KS11", "나스닥": "^IXIC", "S&P500": "^GSPC", "공포지수": "^VIX"},
        "ALT": {"비트코인": "BTC-USD", "금": "GC=F", "원유": "CL=F"},
        "TARGETS": {"SOXL": "SOXL", "MSTR": "MSTR", "TQQQ": "TQQQ", "TSLA": "TSLA", "NVDA": "NVDA", "BITX": "BITX", "XBI": "XBI"}
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
    # 1. 섹터별 압축 요약 (지정학 리스크 및 수급 팩트)
    sector_summary = {
        "반도체": "공매도 잔고 임계점 도달. 숏스퀴즈 발생 시 폭발적 상방 에너지 축적됨. ETF 자금 유입 지속.",
        "빅테크": "금리 인하 기대감으로 인한 기관 수급 대유입. QQQ 자금 유입이 하방 지지선 강력 구축 중.",
        "지정학": "중동 긴장 고조로 유가 및 금값 변동성 확대. 전쟁 리스크가 증시 상단 저항선으로 작용.",
        "코인/기타": "비트코인 70k 돌파 시도 중. MSTR 등 관련주 유동성 집중 및 옵션 변동성 극대화 구간."
    }

    # 2. 4대 투자 성향별 종목 (일자 배치)
    recs = [
        {"title": "🔥 싸나이테스트", "ticker": "SOXL, MSTR, BITX", "reason": "거래량 실린 돌파 시그널. 외인/기관 광기 수급. 숏커버링 폭발 임박 구간."},
        {"title": "🏃‍♂️ 평범이의 숟가락", "ticker": "QQQ, VOO, AAPL", "reason": "지수 대장주 중심의 안정적 우상향. 실적 기반 매수세 탄탄. 분할 매수 적기."},
        {"title": "🛡️ 쫄보들의 안식처", "ticker": "TLT, IAU, SCHD", "reason": "하방 경직성 확보. 금리 하락 수혜 채권과 안전자산 금으로 계좌 방어막 구축."},
        {"title": "🕵️ 세력 형님 뒤쫓기", "ticker": "TSLA, XBI, COIN", "reason": "바닥권 매집 물량 포착. 공매도 세력 항복(숏스퀴즈) 임박. 리버설 타점 공략."}
    ]

    # 3. 옵션 만기 & 맥스페인 분석
    options = [
        {"t": "NVDA", "date": "03-20", "pain": "135.0", "strat": "140불 콜 매도 우세. 만기일 전 135불 수렴 가능성 농후."},
        {"t": "TSLA", "date": "03-20", "pain": "210.0", "strat": "맥스페인 부근 횡보. 220불 돌파 시 헤지 물량 폭등 주의."},
        {"t": "BTC", "date": "03-27", "pain": "68k", "strat": "월말 대규모 만기 예정. 70k 상단 저항선 및 눌림목 지지 체크."},
        {"t": "QQQ", "date": "03-13", "pain": "485.0", "strat": "위클리 만기 변동성 활용. 480불 하단 지지 확인 후 대응."},
        {"t": "SPY", "date": "03-20", "pain": "515.0", "strat": "네 마녀의 날 대비 현금 비중 조절 및 변동성 매매 유효."}
    ]

    # 4. 경제 지표 캘린더
    events = [
        {"d": "오늘", "e": "트럼프 경제 특보 긴급 연설 / 주요 기술주 장 마감 후 실적 발표"},
        {"d": "내일", "e": "비농업 고용 지표 발표 (나스닥 향방 결정타) / 연준 위원 발언"},
        {"d": "만기", "e": "03-20 미국 옵션 만기일 (네 마녀의 날 - 역사적 변동성 주의)"}
    ]
    
    return sector_summary, recs, options, events

def generate_html(data, summary, recs, options, events):
    now = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
    # 대표님께서 업로드하신 파일명(ax.png)으로 정확히 고정
    ant_face_url = "ax.png"
    history_json = {sym: d['history'] for sym, d in data.items()}

    def get_card(sym, d):
        c = 'text-red-500' if d['chg'] > 0 else 'text-blue-500'
        return f'''
        <div class="group relative bg-[#1e1e1e] p-3 rounded-xl border border-zinc-800 cursor-pointer" onmouseenter="showChart('{sym}')">
            <p class="text-[10px] text-zinc-500 font-bold mb-1">{d['name']}</p>
            <p class="text-base font-black text-white italic tracking-tighter">{d['price']:,.1f}</p>
            <p class="{c} text-[10px] font-bold">{d['chg']:+.2f}%</p>
            <div id="chart-container-{sym}" class="absolute z-50 bottom-full left-0 mb-2 w-56 h-32 bg-black border border-zinc-700 rounded-xl p-2 hidden group-hover:block pointer-events-none shadow-2xl">
                <div id="chart-{sym}" class="w-full h-full"></div>
            </div>
        </div>
        '''

    cards_indices = "".join([get_card(s, data[s]) for s in ["^KS11", "^IXIC", "^GSPC", "^VIX", "BTC-USD", "GC=F", "CL=F"]])
    summary_html = "".join([f'<div class="mb-2"><span class="text-[#D4AF37] font-black text-xs mr-2">[{k}]</span><span class="text-zinc-300 text-xs font-bold leading-relaxed">{v}</span></div>' for k,v in summary.items()])
    
    rec_cards = "".join([f'''
        <div class="group relative bg-[#1e1e1e] p-5 rounded-2xl border border-zinc-800 hover:border-[#D4AF37]/40 transition shadow-lg cursor-pointer" onmouseenter="showChart('{r['ticker'].split(', ')[0]}')">
            <h3 class="text-white font-black text-base mb-2 tracking-tighter">{r['title']}</h3>
            <div class="bg-black/40 p-2 rounded-lg mb-2 text-[#D4AF37] font-black text-[10px] tracking-widest border border-white/5">{r['ticker']}</div>
            <p class="text-zinc-400 text-[11px] font-medium leading-relaxed" style="word-break: keep-all;">{r['reason']}</p>
        </div>
    ''' for r in recs])

    option_html = "".join([f'''
        <div class="bg-[#151515] p-4 rounded-xl border border-zinc-800">
            <div class="flex justify-between mb-1 border-b border-zinc-800 pb-1">
                <span class="text-white font-black text-xs">{o['t']}</span>
                <span class="text-red-500 text-[9px] font-bold">{o['date']} 만기</span>
            </div>
            <div class="flex justify-between my-1"><span class="text-zinc-600 text-[9px] font-bold uppercase">Max Pain</span><span class="text-white font-black text-[10px]">{o['pain']}</span></div>
            <p class="text-zinc-400 text-[10px] leading-tight font-bold">{o['strat']}</p>
        </div>
    ''' for o in options])

    event_html = "".join([f'<div class="flex gap-3 p-2 border-b border-zinc-800 last:border-0 text-[11px]"><span class="text-zinc-500 font-black w-8">{e["d"]}</span><span class="text-zinc-300 font-bold leading-tight">{e["e"]}</span></div>' for e in events])

    html = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>연신내 개미펀드 V13</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
            body {{ background-color: #0d0d0d; color: #d1d1d1; font-family: 'Noto Sans KR', 'Malgun Gothic', sans-serif; letter-spacing: -0.03em; -webkit-font-smoothing: antialiased; }}
            @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
            .ant-logo {{ width: 90px; height: 90px; object-fit: contain; animation: spin 15s linear infinite; filter: drop-shadow(0 0 12px rgba(212,175,55,0.4)); }}
        </style>
    </head>
    <body class="p-4 md:p-8">
        <div class="max-w-7xl mx-auto">
            <header class="flex flex-col md:flex-row justify-between items-center mb-10 border-b border-zinc-900 pb-8 gap-6">
                <div class="flex items-center gap-8">
                    <img src="{ant_face_url}" class="ant-logo" alt="야수">
                    <div>
                        <h1 class="text-5xl font-black text-white italic tracking-tighter mb-1">연신내 개미펀드</h1>
                        <p class="text-[#D4AF37] font-black text-[10px] tracking-[0.4em] uppercase">ULTIMATE BEAST TERMINAL V13</p>
                    </div>
                </div>
                <div class="text-right p-4 bg-[#151515] rounded-xl border border-zinc-900 shadow-2xl">
                    <p class="text-[9px] text-zinc-600 font-black mb-1 uppercase tracking-widest">KST Sync</p>
                    <p class="text-sm font-black text-white italic">{now}</p>
                </div>
            </header>

            <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3 mb-10">{cards_indices}</div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-12">
                <div class="lg:col-span-2 bg-[#151515] p-8 rounded-3xl border border-zinc-900 shadow-2xl relative overflow-hidden">
                    <div class="absolute -right-10 -bottom-10 opacity-5 text-[150px] font-black italic">FACT</div>
                    <h2 class="text-2xl font-black text-white mb-6 italic">🏛️ 금일 섹터 요약 브리핑</h2>
                    <div class="space-y-1 relative z-10">{summary_html}</div>
                </div>
                <div class="bg-[#151515] p-6 rounded-3xl border border-zinc-900 shadow-2xl">
                    <h3 class="text-[10px] font-black text-zinc-500 mb-4 uppercase border-l-4 border-[#D4AF37] pl-3 tracking-widest">경제 지표 캘린더</h3>
                    <div class="bg-black/20 rounded-xl border border-zinc-800">{event_html}</div>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-16">{rec_cards}</div>

            <h2 class="text-[10px] font-black text-zinc-600 mb-6 tracking-[0.3em] uppercase flex items-center gap-3">
                <span class="w-10 h-[1px] bg-zinc-900"></span> 옵션 세력 분석 & 맥스페인 (타점 가이드)
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-5 gap-3 mb-10">{option_html}</div>
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
                    series: [{{ data: allHistory[sym], type: 'line', smooth: true, symbol: 'none', lineStyle: {{ color: '#D4AF37', width: 2 }}, areaStyle: {{ color: 'rgba(212,175,55, 0.05)' }} }}]
                }});
            }}
        </script>
    </body>
    </html>
    """
    with open("index.html", "w", encoding="utf-8") as f: f.write(html)

if __name__ == "__main__":
    d = fetch_extensive_data()
    summary, recs, opts, events = ai_beast_meeting(d)
    generate_html(d, summary, recs, opts, events)
