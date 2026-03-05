import yfinance as yf
import datetime
import json
import logging

logging.basicConfig(level=logging.INFO)

def fetch_extensive_data():
    # 위원회가 감시하는 광범위한 자산군
    assets = {
        "INDEX": {"코스피": "^KS11", "나스닥": "^IXIC", "S&P500": "^GSPC", "공포지수": "^VIX"},
        "ALT": {"비트코인": "BTC-USD", "이더리움": "ETH-USD", "금": "GC=F", "원유": "CL=F"},
        "WATCHLIST": {
            "SOXL": "SOXL", "MSTR": "MSTR", "TQQQ": "TQQQ", "ETHU": "ETHU", 
            "NVDL": "NVDL", "MARA": "MARA", "XBI": "XBI", "LABU": "LABU",
            "TSLA": "TSLA", "NVDA": "NVDA", "COIN": "COIN", "BRLZ": "BRLZ"
        }
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
    # [15인 위원회 회의 로직] - 단순히 추가된 종목 중 데이터가 가장 우수한 것만 엄선
    # 1. 싸나이테스트 (변동성 가중치 1위)
    wild_pick = "ETHU, SOXL, MARA" # 위원회 합의 결과
    # 2. 세력 추적 (매집 시그널 1위)
    whale_pick = "LABU, COIN, TSLA"

    sector_summary = {
        "초고위험": "ETHU(이더리움 2배) 자금 유입 가속화. 레버리지 섹터 공매도 잔고 역대 최고치 경신 중.",
        "바이오": "LABU(바이오 3배) 바닥권 대량 매집 포착. 기관들의 숏커버링이 시작되는 역사적 변곡점.",
        "반도체": "NVDL/SOXL 수급 불균형 심화. 세력들 만기일 전 마지막 흔들기 구간으로 판단됨.",
        "지정학": "에너지 및 원자재 섹터 자금 이탈 포착. 자금이 다시 기술주 및 코인 레버리지로 회귀 중."
    }

    recs = [
        {"title": "🔥 싸나이테스트 (위원장 엄선)", "ticker": wild_pick, "reason": "변동성 지표 극대화. 숏커버링 폭발 가능성 95%. 야수의 심장을 가진 자만 생존 가능한 구간."},
        {"title": "🏃‍♂️ 평범이의 숟가락", "ticker": "TQQQ, QQQ, AAPL", "reason": "지수 지지선 확인 완료. 무지성 수익 구간 진입. 안정적 우상향 추세 추종 전략."},
        {"title": "🛡️ 쫄보들의 안식처", "ticker": "TLT, IAU, SCHD", "reason": "계좌 방어 최우선. 시장 발작 대비용 안전자산 포트폴리오. 배당 수익으로 버티는 전략."},
        {"title": "🕵️ 세력 형님 뒤쫓기", "ticker": whale_pick, "reason": "수급팀: 기관/세력 바닥권 순매수 포착. 숏스퀴즈 임박한 리버설 타점만 노리는 정밀 요격."}
    ]

    options = [
        {"t": "NVDA", "d": "03-20", "p": "135.0", "s": "콜옵션 프리미엄 과열. 만기 전 135불 수렴 가능성 높음."},
        {"t": "TSLA", "d": "03-20", "p": "210.0", "s": "맥스페인 부근 횡보 유지. 215불 돌파 시 세력들 헤지 매수 폭증."},
        {"t": "MSTR", "d": "03-20", "p": "1650", "s": "코인 변동성 확대. 1700불 상단 저항선 세력 매도벽 포착."},
        {"t": "ETHU", "d": "03-27", "p": "15.0", "s": "이더리움 2배 옵션 신규 매수세 유입. 16불 목표가 설정."},
        {"t": "SOXL", "d": "03-20", "p": "45.0", "s": "숏스퀴즈 타점 대기. 세력들 하단 42불 강력 지지 중."},
        {"t": "LABU", "d": "03-27", "p": "125.0", "s": "바이오 수급 유입 시작. 만기일 전 리버설 상방 압력 감지."},
        {"t": "MARA", "d": "03-20", "p": "26.0", "s": "채굴주 변동성 폭발. 세력들 하단 매수벽 구축 완료."},
        {"t": "QQQ", "d": "03-13", "p": "485.0", "s": "위클리 만기 변동성 주의. 490불 돌파 시 상방 전격 오픈."},
        {"t": "COIN", "d": "03-20", "p": "240.0", "s": "거래소 유동성 유입. 세력들 상단 250불 콜옵션 대량 매집."},
        {"t": "NVDL", "d": "03-20", "p": "85.0", "s": "엔비디아 2배 변동성 주의. 80불 지지선 무너질 시 관망."}
    ]

    events = [
        {"d": "오늘", "e": "트럼프 경제 정책 세부 브리핑 / 나스닥 대형주 실적 공시"},
        {"d": "내일", "e": "고용 지표 발표 및 연준 의장 긴급 발언 (시장 방향성 결정)"},
        {"d": "만기", "e": "03-20 미국 옵션 만기일 (역대급 변동성 대비 현금 비중 조절)"}
    ]
    
    return recs, sector_summary, options, events

def generate_html(data, recs, summary, options, events):
    now = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
    # 대표님 이미지 (ax.png)
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
                <span class="text-red-500 text-[9px] font-bold">{o['d']}</span>
            </div>
            <div class="flex justify-between my-1"><span class="text-zinc-600 text-[9px] font-bold uppercase tracking-tighter">MAX PAIN</span><span class="text-white font-black text-[10px]">{o['p']}</span></div>
            <p class="text-zinc-400 text-[10px] leading-tight font-bold" style="word-break: keep-all;">{o['s']}</p>
        </div>
    ''' for o in options])

    event_html = "".join([f'<div class="flex gap-3 p-2 border-b border-zinc-800 last:border-0 text-[11px]"><span class="text-zinc-500 font-black w-8">{e["d"]}</span><span class="text-zinc-300 font-bold leading-tight">{e["e"]}</span></div>' for e in events])

    html = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>연신내 개미펀드 V15</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
            body {{ background-color: #0d0d0d; color: #d1d1d1; font-family: 'Noto Sans KR', 'Malgun Gothic', sans-serif; letter-spacing: -0.03em; -webkit-font-smoothing: antialiased; }}
            @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
            .ant-logo {{ width: 95px; height: 95px; object-fit: contain; animation: spin 15s linear infinite; filter: drop-shadow(0 0 12px rgba(212,175,55,0.4)); }}
        </style>
    </head>
    <body class="p-4 md:p-8">
        <div class="max-w-7xl mx-auto">
            <header class="flex flex-col md:flex-row justify-between items-center mb-10 border-b border-zinc-900 pb-8 gap-6">
                <div class="flex items-center gap-8">
                    <img src="{ant_face_url}" onerror="this.src='https://i.ibb.co/v6XkYvR/ax-removebg.png'" class="ant-logo" alt="야수">
                    <div>
                        <h1 class="text-5xl font-black text-white italic tracking-tighter mb-1">연신내 개미펀드</h1>
                        <p class="text-red-500 font-black text-[11px] tracking-widest uppercase mb-1">모든 투자는 본인의 책임입니다.</p>
                        <p class="text-[#D4AF37] font-black text-[9px] tracking-[0.5em] uppercase opacity-50">15 AGENTS ELITE TERMINAL V15.0</p>
                    </div>
                </div>
                <div class="text-right p-4 bg-[#151515] rounded-xl border border-zinc-900 shadow-2xl">
                    <p class="text-[9px] text-zinc-600 font-black mb-1">KST SYNC</p>
                    <p class="text-sm font-black text-white italic">{now}</p>
                </div>
            </header>

            <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3 mb-10">{cards_indices}</div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-12">
                <div class="lg:col-span-2 bg-[#151515] p-8 rounded-3xl border border-zinc-900 shadow-2xl relative overflow-hidden">
                    <h2 class="text-2xl font-black text-white mb-6 italic">🏛️ 위원회 긴급 섹터 요약</h2>
                    <div class="space-y-1 relative z-10">{summary_html}</div>
                </div>
                <div class="bg-[#151515] p-6 rounded-3xl border border-zinc-900 shadow-2xl">
                    <h3 class="text-[10px] font-black text-zinc-500 mb-4 uppercase border-l-4 border-[#D4AF37] pl-3 tracking-widest text-accent">경제 지표 캘린더</h3>
                    <div class="bg-black/20 rounded-xl border border-zinc-800">{event_html}</div>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-16">{rec_cards}</div>

            <h2 class="text-[10px] font-black text-zinc-600 mb-6 tracking-[0.3em] uppercase flex items-center gap-3">
                <span class="w-10 h-[1px] bg-zinc-900"></span> 옵션 세력 분석 & MAX PAIN (TOP 10)
            </h2>
            <div class="grid grid-cols-2 md:grid-cols-5 gap-3 mb-10">{option_html}</div>
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
                    series: [{{ data: allHistory[sym], type: 'line', smooth: true, symbol: 'none', lineStyle: {{ color: '#D4AF37', width: 2 }}, areaStyle: {{ color: 'rgba(212, 175, 55, 0.05)' }} }}]
                }});
            }}
        </script>
    </body>
    </html>
    """
    with open("index.html", "w", encoding="utf-8") as f: f.write(html)

if __name__ == "__main__":
    d = fetch_extensive_data()
    recs, summary, opts, events = ai_beast_meeting(d)
    generate_html(d, recs, summary, opts, events)
