import yfinance as yf
import datetime
import json
import logging
import sys

# 1. 15인 위원회 로깅 시스템 가동
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BeastTerminal_V17_5")

def fetch_top_tier_data():
    # 위원회 엄선 자산 및 환율/스테이블코인 데이터 수집
    assets = {
        "CURRENCY": {"원/달러": "USDKRW=X", "USDT_C": "USDT-USD"},
        "INDEX": {"코스피": "^KS11", "나스닥": "^IXIC", "S&P500": "^GSPC", "공포지수": "^VIX"},
        "CRYPTO": {"비트코인": "BTC-USD", "이더리움": "ETH-USD"},
        "WATCH": {"SOXL":"SOXL", "MSTR":"MSTR", "TQQQ":"TQQQ", "ETHU":"ETHU", "LABU":"LABU", "COST":"COST", "AVGO":"AVGO", "ORCL":"ORCL"}
    }
    data_pool = {}
    for cat, group in assets.items():
        for name, sym in group.items():
            try:
                t = yf.Ticker(sym)
                h = t.history(period="7d") # 주말 대비 넉넉하게 7일 수집
                if len(h) >= 2:
                    prices = h['Close'].round(2).tolist()
                    curr, prev = h['Close'].iloc[-1], h['Close'].iloc[-2]
                    chg = ((curr - prev) / prev) * 100
                    data_pool[sym] = {"name": name, "price": curr, "chg": chg, "history": prices}
                else:
                    data_pool[sym] = {"name": name, "price": 0.0, "chg": 0.0, "history": [0,0]}
            except:
                data_pool[sym] = {"name": name, "price": 0.0, "chg": 0.0, "history": [0,0]}
    return data_pool

def ai_beast_meeting():
    # 위원회 회의를 통해 엄선된 섹터별 리포트 도출
    recs = [
        {"title": "🔥 싸나이테스트 (엄선)", "ticker": "ETHU, SOXL, MSTR", "reason": "변동성 및 수급 교차 검증 완료. 숏스퀴즈 발생 확률 상위 1% 정예 종목군."},
        {"title": "🏃‍♂️ 평범이의 숟가락 (엄선)", "ticker": "TQQQ, NVDA, TSLA", "reason": "스마트 머니 유입 확인. 눌림목 구간 숟가락 얹기 최적화."},
        {"title": "🛡️ 쫄보들의 안식처 (엄선)", "ticker": "SCHD, TLT, IAU", "reason": "자산 방어 분과 회의 결과: 하방 경직성 철벽 포트폴리오."},
        {"title": "🕵️ 세력 형님 뒤쫓기 (엄선)", "ticker": "LABU, COIN, MARA", "reason": "온체인 대량 매집 시그널 포착. 리버설 타점 정밀 요격."}
    ]
    # 실적 발표 7일 (위원회가 선정한 롱 타겟 강조)
    earnings = [
        {"date": "03-05 (오늘)", "companies": [{"n": "Costco", "s": "COST", "d": "costco.com", "t": "장후", "rec": True}]},
        {"date": "03-09 (월)", "companies": [{"n": "Oracle", "s": "ORCL", "d": "oracle.com", "t": "장후", "rec": True}]},
        {"date": "03-11 (수)", "companies": [{"n": "Broadcom", "s": "AVGO", "d": "broadcom.com", "t": "장후", "rec": True}]}
    ]
    return recs, earnings

def generate_html(data, recs, earnings):
    try:
        now = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
        # 자바스크립트 충돌 방지를 위한 데이터 직렬화
        history_json = json.dumps({sym: d['history'] for sym, d in data.items()})

        # 환율 바(Bar) 조립
        usd_krw = data.get('USDKRW=X', {'price':0, 'chg':0})
        usdt_c = data.get('USDT-USD', {'price':0, 'chg':0})
        
        currency_html = f'''
        <div class="flex gap-6 p-4 bg-white dark:bg-[#151515] border-b border-zinc-200 dark:border-zinc-800 overflow-x-auto shadow-sm">
            <div class="flex items-center gap-3 whitespace-nowrap">
                <span class="text-[11px] font-bold text-zinc-500">💵 원/달러</span>
                <span class="text-sm font-black text-zinc-900 dark:text-white">{usd_krw['price']:,.2f}</span>
                <span class="text-[10px] font-bold {'text-red-500' if usd_krw['chg'] > 0 else 'text-blue-500'}">{usd_krw['chg']:+.2f}%</span>
            </div>
            <div class="w-[1px] h-4 bg-zinc-300 dark:bg-zinc-700"></div>
            <div class="flex items-center gap-3 whitespace-nowrap">
                <span class="text-[11px] font-bold text-zinc-500">🔗 USDT/USDC</span>
                <span class="text-sm font-black text-zinc-900 dark:text-white">${usdt_c['price']:,.4f}</span>
                <span class="bg-green-500/10 text-green-500 text-[9px] px-1.5 py-0.5 rounded font-black">STABLE</span>
            </div>
        </div>'''

        # 지수 카드 및 추천 섹터/실적 HTML 사전 조립 (충돌 방지 핵심)
        index_cards = ""
        for s in ["^KS11", "^IXIC", "^GSPC", "^VIX", "BTC-USD", "ETH-USD", "GC=F"]:
            d = data.get(s, {'name': s, 'price':0, 'chg':0})
            index_cards += f'''
            <div class="bg-white dark:bg-[#1e1e1e] p-4 rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-sm" onmouseenter="showChart('{s}')">
                <p class="text-[10px] text-zinc-500 font-bold mb-1">{d['name']}</p>
                <p class="text-lg font-black italic text-zinc-900 dark:text-white">{d['price']:,.1f}</p>
                <p class="{'text-red-500' if d['chg'] > 0 else 'text-blue-500'} text-[11px] font-bold">{d['chg']:+.2f}%</p>
                <div id="chart-container-{s}" class="absolute z-50 bottom-full left-0 mb-2 w-56 h-32 bg-black border border-zinc-700 rounded-xl p-2 hidden shadow-2xl pointer-events-none group-hover:block"><div id="chart-{s}" class="w-full h-full"></div></div>
            </div>'''

        rec_cards = "".join([f'''
            <div class="bg-white dark:bg-[#1e1e1e] p-6 rounded-2xl border border-zinc-200 dark:border-zinc-800 shadow-md">
                <h3 class="text-zinc-900 dark:text-white font-black text-lg mb-3 italic tracking-tighter">{r['title']}</h3>
                <div class="bg-[#D4AF37]/10 p-3 rounded-lg mb-3 text-[#D4AF37] font-black text-xs border border-[#D4AF37]/20">{r['ticker']}</div>
                <p class="text-zinc-500 dark:text-zinc-400 text-xs font-medium leading-relaxed">{r['reason']}</p>
            </div>''' for r in recs])

        earnings_html = ""
        for day in earnings:
            earnings_html += f'<p class="text-[10px] font-black text-[#D4AF37] mb-3 border-b border-zinc-100 dark:border-zinc-800 pb-1">{day["date"]}</p>'
            for c in day['companies']:
                style = "border-[#D4AF37] bg-[#D4AF37]/5" if c['rec'] else "border-zinc-100 dark:border-zinc-800"
                earnings_html += f'''
                <div class="flex items-center justify-between p-3 rounded-xl border {style} mb-3 shadow-sm">
                    <div class="flex items-center gap-3">
                        <img src="https://logo.clearbit.com/{c['d']}" class="w-8 h-8 rounded-lg bg-white p-1" onerror="this.src='https://via.placeholder.com/32?text={c['s']}'">
                        <div><p class="text-xs font-black text-zinc-900 dark:text-white">{c['n']}</p></div>
                    </div>
                    <span class="text-[10px] font-bold text-zinc-400">{c['t']}</span>
                </div>'''

        # 최종 HTML 완성 (중괄호 충돌 완전 해결)
        full_html = f"""
        <!DOCTYPE html>
        <html lang="ko" class="dark">
        <head>
            <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>연신내 개미펀드 V17.5</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
                body {{ font-family: 'Noto Sans KR', sans-serif; }}
                @keyframes spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
                .ant-logo {{ animation: spin 20s linear infinite; filter: drop-shadow(0 0 10px rgba(212,175,55,0.4)); }}
            </style>
            <script>
                tailwind.config = {{ darkMode: 'class' }};
                function toggleTheme() {{ document.documentElement.classList.toggle('dark'); }}
            </script>
        </head>
        <body class="bg-zinc-50 dark:bg-[#0d0d0d] text-zinc-900 dark:text-zinc-300">
            {currency_html}
            <div class="p-6 md:p-12 max-w-7xl mx-auto">
                <header class="flex flex-col md:flex-row justify-between items-center mb-12 border-b border-zinc-200 dark:border-zinc-900 pb-10 gap-8">
                    <div class="flex items-center gap-8">
                        <img src="ax.png" onerror="this.src='https://i.ibb.co/v6XkYvR/ax-removebg.png'" class="ant-logo w-24 h-24 object-contain">
                        <div>
                            <h1 class="text-5xl font-black text-zinc-900 dark:text-white italic tracking-tighter mb-2">연신내 개미펀드</h1>
                            <p class="text-red-500 font-black text-xs tracking-widest mb-1 uppercase">모든 투자는 본인의 책임입니다.</p>
                        </div>
                    </div>
                    <div class="flex items-center gap-4">
                        <button onclick="toggleTheme()" class="p-3 bg-white dark:bg-[#1e1e1e] border border-zinc-200 dark:border-zinc-800 rounded-full shadow-lg">🌓 테마 전환</button>
                        <div class="text-right p-4 bg-white dark:bg-[#151515] rounded-xl border border-zinc-200 dark:border-zinc-900">
                            <p class="text-sm font-black text-zinc-900 dark:text-white italic">{now}</p>
                        </div>
                    </div>
                </header>

                <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4 mb-12">{index_cards}</div>

                <div class="grid grid-cols-1 lg:grid-cols-4 gap-8 mb-16">
                    <div class="lg:col-span-3 grid grid-cols-1 md:grid-cols-2 gap-6">{rec_cards}</div>
                    <div class="bg-white dark:bg-[#151515] p-8 rounded-3xl border border-zinc-200 dark:border-zinc-900 shadow-xl">
                        <h3 class="text-[11px] font-black text-zinc-500 mb-6 uppercase border-l-4 border-[#D4AF37] pl-4 tracking-widest">실적 발표 (7D)</h3>
                        <div class="space-y-4">{earnings_html}</div>
                    </div>
                </div>
            </div>

            <script>
                const allHistory = {history_json};
                function showChart(sym) {{
                    const container = document.getElementById('chart-' + sym);
                    if(!container) return;
                    const chart = echarts.init(container);
                    chart.setOption({{
                        grid: {{ top: 10, bottom: 10, left: 10, right: 10 }},
                        xAxis: {{ type: 'category', show: false }},
                        yAxis: {{ type: 'value', show: false, min: 'dataMin', max: 'dataMax' }},
                        series: [{{ data: allHistory[sym], type: 'line', smooth: true, symbol: 'none', lineStyle: {{ color: '#D4AF37', width: 2 }}, areaStyle: {{ color: 'rgba(212, 175, 55, 0.1)' }} }}]
                    }});
                }}
            </script>
        </body>
        </html>"""
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(full_html)
        logger.info("V17.5 HTML successfully generated.")

    except Exception as e:
        logger.error(f"Generation Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    d = fetch_top_tier_data()
    r, e = ai_beast_meeting()
    generate_html(d, r, e)
