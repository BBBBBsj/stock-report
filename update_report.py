import yfinance as yf
import datetime
import json
import logging

logging.basicConfig(level=logging.INFO)

def fetch_extensive_data():
    # 데이터 수집 범위를 고위험 섹터(레버리지, 바이오, 코인주)로 대폭 확장
    assets = {
        "INDEX": {"코스피": "^KS11", "나스닥": "^IXIC", "S&P500": "^GSPC", "공포지수": "^VIX"},
        "ALT": {"비트코인": "BTC-USD", "이더리움": "ETH-USD", "금": "GC=F", "원유": "CL=F"},
        "TARGETS": {
            "SOXL": "SOXL", "MSTR": "MSTR", "TQQQ": "TQQQ", "ETHU": "ETHU", 
            "NVDL": "NVDL", "MARA": "MARA", "XBI": "XBI", "LABU": "LABU",
            "TSLA": "TSLA", "NVDA": "NVDA", "COIN": "COIN"
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
    # 1. 섹터별 팩트 요약 (위험도 상향)
    sector_summary = {
        "초고위험": "이더리움 2배(ETHU) 및 비트코인 채굴주(MARA) 수급 폭발. 야수들의 자금이 레버리지로 집중됨.",
        "바이오": "XBI/LABU 바닥권 매집 포착. 금리 인하 기대감에 세력들 바이오 섹터 숏커버링 본격화.",
        "반도체": "SOXL 공매도 잔고 임계점. 엔비디아 실적 발표 전후로 역사적 숏스퀴즈 시나리오 가동 중.",
        "지정학": "중동 발 에너지원 확보 경쟁 및 전쟁 리스크 지속. 안전자산(금)과 위험자산(코인) 동반 상승 기현상."
    }

    # 2. 투자 성향별 4대 천왕 (종목 대폭 추가)
    recs = [
        {"title": "🔥 싸나이테스트 (경주마)", "ticker": "ETHU, SOXL, MARA, NVDL", "reason": "퀀트: 변동성 지수 폭발. 수급: 외인 무지성 풀매수. 한강 아니면 펜트하우스, 야성 그 자체."},
        {"title": "🏃‍♂️ 평범이의 숟가락", "ticker": "TQQQ, QQQ, AAPL, MSFT", "reason": "거시: 우상향 추세 확정. 기관: 하단 지지선 강력 구축. 남들 벌 때 소외되지 않는 안전 빵 전략."},
        {"title": "🛡️ 쫄보들의 안식처", "ticker": "TLT, IAU, XLF, SCHD", "reason": "리스크: 하방 경직성 확보. 배당과 금으로 계좌 방어. 시장이 발작해도 발 뻗고 자는 전략."},
        {"title": "🕵️ 세력 형님 뒤쫓기", "ticker": "LABU(바이오3배), COIN, TSLA", "reason": "수급: 세력들 바닥 매집 완료 시그널. 공매도 세력 손절(숏스퀴즈) 임박한 리버설 타점."}
    ]

    # 3. 주요 옵션 분석 (10개로 확장)
    options = [
        {"t": "NVDA", "d": "03-20", "p": "135.0", "s": "콜옵션 대량 매집 확인. 140불 돌파 시세 분출 기대."},
        {"t": "TSLA", "d": "03-20", "p": "210.0", "s": "맥스페인 부근 횡보. 세력들 변동성 죽이기 작업 중."},
        {"t": "MSTR", "d": "03-20", "p": "1600", "s": "코인 변동성 직결. 콜옵션 프리미엄 과열 구간 주의."},
        {"t": "ETHU", "d": "03-27", "p": "15.0", "s": "이더리움 시세 수렴. 만기 전 상방 압력 강함."},
        {"t": "SOXL", "d": "03-20", "p": "45.0", "s": "숏스퀴즈 타점 대기. 세력들 하단 40불 지지 강력."},
        {"t": "AAPL", "d": "03-20", "p": "230.0", "s": "기관 풋매도 우세. 하방 막혀있는 안정적 흐름."},
        {"t": "MARA", "d": "03-20", "p": "25.0", "s": "채굴주 변동성 폭발. 옵션 시장 세력 매수세 대입."},
        {"t": "LABU", "d": "03-27", "p": "120.0", "s": "바이오 수급 유입. 만기일 전 리버설 타점 포착."},
        {"t": "QQQ", "d": "03-13", "p": "485.0", "s": "위클리 만기 변동성. 490불 돌파 시 상방 오픈."},
        {"t": "BITX", "d": "03-27", "p": "40.0", "s": "비트코인 2배 옵션 광기. 세력들 상단 매도 벽 구축."}
    ]

    events = [
        {"d": "오늘", "e": "트럼프 경제 정책 세부 브리핑 / 이더리움 현물 수급 보고서"},
        {"d": "내일", "e": "고용 지표 발표 및 연준 의장 발언 (나스닥 향방 결정)"},
        {"d": "만기", "e": "03-20 미국 쿼드러플 위칭데이 (역대급 변동성 예고)"}
    ]
    
    return sector_summary, recs, options, events

def generate_html(data, summary, recs, options, events):
    now = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
    # 이미지 경로: ax.png가 있으면 사용, 없으면 글자 출력
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
    summary_html = "".join([f'<div class="mb-2"><span class="text-[#D4AF37] font-black text-xs mr-2">[{k}]</span><span class="text-zinc-300 text-xs font-bold">{v}</span></div>' for k,v in summary.items()])
    
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
        <title>연신내 개미펀드 V14</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
            body {{ background-color: #0d0d0d; color: #d1d1d1; font-family: 'Noto Sans KR', 'Malgun Gothic', sans-serif; letter-spacing: -0.03em; -webkit-font-smoothing: antialiased; }}
            @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
            .ant-logo {{ width: 95px; height: 95px; object-fit: contain; animation: spin 15s linear infinite; filter: drop-shadow(0 0 12px rgba(212,175,55,0.4)); }}
            .beast-font {{ font-weight: 900; font-style: italic; }}
        </style>
    </head>
    <body class="p-4 md:p-8">
        <div class="max-w-7xl mx-auto">
            <header class="flex flex-col md:flex-row justify-between items-center mb-10 border-b border-zinc-900 pb-8 gap-6">
                <div class="flex items-center gap-8">
                    <img src="{ant_face_url}" onerror="this.outerHTML='<div class=\\'ant-logo flex items-center justify-center text-[#D4AF37] font-black text-xl border-2 border-[#D4AF37] rounded-full\\'>야수</div>'" class="ant-logo" alt="야수">
                    <div>
                        <h1 class="text-5xl font-black text-white italic tracking-tighter mb-1">연신내 개미펀드</h1>
                        <p class="text-[#D4AF37] font-black text-[10px] tracking-[0.4em] uppercase tracking-widest">BEAST MODE TERMINAL V14.0</p>
                    </div>
                </div>
                <div class="text-right p-4 bg-[#151515] rounded-xl border border-zinc-900"><p class="text-[9px] text-zinc-600 font-black mb-1 uppercase">KST Sync</p><p class="text-sm font-black text-white italic">{now}</p></div>
            </header>

            <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3 mb-10">{cards_indices}</div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-12">
                <div class="lg:col-span-2 bg-[#151515] p-8 rounded-3xl border border-zinc-900 shadow-2xl relative overflow-hidden">
                    <h2 class="text-2xl font-black text-white mb-6 italic">🏛️ 금일 섹터 요약 브리핑 (Fact Only)</h2>
                    <div class="space-y-1 relative z-10">{summary_html}</div>
                </div>
                <div class="bg-[#151515] p-6 rounded-3xl border border-zinc-900 shadow-2xl">
                    <h3 class="text-[10px] font-black text-zinc-500 mb-4 uppercase border-l-4 border-[#D4AF37] pl-3 tracking-widest">나스닥 경제 지표 캘린더</h3>
                    <div class="bg-black/20 rounded-xl border border-zinc-800">{event_html}</div>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-16">{rec_cards}</div>

            <h2 class="text-[10px] font-black text-zinc-600 mb-6 tracking-[0.3em] uppercase flex items-center gap-3">
                <span class="w-10 h-[1px] bg-zinc-900"></span> 세력 옵션 타점 & MAX PAIN (TOP 10)
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
    summary, recs, opts, events = ai_beast_meeting(d)
    generate_html(d, summary, recs, opts, events)
