import yfinance as yf
import datetime
import json
import logging
import sys

# 로깅 설정 (에러 추적용)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BeastTerminal")

def fetch_top_tier_data():
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
                # 안전하게 7일치 데이터를 가져와서 마지막 2일을 비교
                h = t.history(period="7d")
                if len(h) >= 2:
                    prices = h['Close'].round(2).tolist()
                    curr, prev = h['Close'].iloc[-1], h['Close'].iloc[-2]
                    chg = ((curr - prev) / prev) * 100
                    data_pool[sym] = {"name": name, "price": curr, "chg": chg, "history": prices}
                else:
                    # 데이터가 부족할 경우 기본값 세팅 (에러 방지)
                    data_pool[sym] = {"name": name, "price": 0.0, "chg": 0.0, "history": [0,0]}
            except Exception as e:
                logger.error(f"Error fetching {sym}: {e}")
                data_pool[sym] = {"name": name, "price": 0.0, "chg": 0.0, "history": [0,0]}
    return data_pool

def ai_beast_meeting():
    # 15인 위원회 엄선 결과 (고정 리포트)
    recs = [
        {"title": "🔥 싸나이테스트 (엄선)", "ticker": "ETHU, SOXL, MSTR", "reason": "변동성 및 수급 교차 검증 완료. 숏스퀴즈 발생 확률 상위 1% 종목군."},
        {"title": "🏃‍♂️ 평범이의 숟가락 (엄선)", "ticker": "TQQQ, NVDA, TSLA", "reason": "개미들의 스마트 머니 유입 확인. 눌림목 구간에서 숟가락 얹기 최적화."},
        {"title": "🛡️ 쫄보들의 안식처 (엄선)", "ticker": "SCHD, TLT, IAU", "reason": "자산 방어 분과 회의 결과. 하방 경직성이 가장 뛰어난 철벽 포트폴리오."},
        {"title": "🕵️ 세력 형님 뒤쫓기 (엄선)", "ticker": "LABU, COIN, MARA", "reason": "온체인 데이터 및 대량 매집 시그널 포착. 세력들의 매집 단가 부근 안착."}
    ]
    earnings = [
        {"date": "03-05 (오늘)", "companies": [{"n": "Costco", "s": "COST", "d": "costco.com", "t": "장후", "rec": True}]},
        {"date": "03-09 (월)", "companies": [{"n": "Oracle", "s": "ORCL", "d": "oracle.com", "t": "장후", "rec": True}]},
        {"date": "03-11 (수)", "companies": [{"n": "Broadcom", "s": "AVGO", "d": "broadcom.com", "t": "장후", "rec": True}]}
    ]
    return recs, earnings

def generate_html(data, recs, earnings):
    try:
        now = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
        ant_face_url = "ax.png"
        history_json = {sym: d['history'] for sym, d in data.items()}

        # 환율 및 스테이블코인 (데이터 부재 시 대비)
        usd_krw = data.get('USDKRW=X', {'price':0, 'chg':0})
        usdt_c = data.get('USDT-USD', {'price':0, 'chg':0})

        # [HTML 구조는 V17.0과 동일하되 중괄호 { } 탈출 처리 강화]
        html = f"""
        <!DOCTYPE html>
        <html lang="ko" class="dark">
        <head>
            <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>연신내 개미펀드 V17.1</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
                body {{ font-family: 'Noto Sans KR', sans-serif; }}
                @keyframes spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
                .ant-logo {{ animation: spin 20s linear infinite; }}
            </style>
            <script>
                tailwind.config = {{ darkMode: 'class' }};
                function toggleTheme() {{ document.documentElement.classList.toggle('dark'); }}
            </script>
        </head>
        <body class="bg-zinc-50 dark:bg-[#0d0d0d] text-zinc-900 dark:text-zinc-300">
            <div class="flex gap-6 p-4 bg-white dark:bg-[#151515] border-b border-zinc-200 dark:border-zinc-800 overflow-x-auto shadow-sm">
                <div class="flex items-center gap-3">
                    <span class="text-[11px] font-bold text-zinc-500">💵 원/달러</span>
                    <span class="text-sm font-black text-zinc-900 dark:text-white">{usd_krw['price']:,.2f}</span>
                </div>
                <div class="flex items-center gap-3">
                    <span class="text-[11px] font-bold text-zinc-500">🔗 USDT/USDC</span>
                    <span class="text-sm font-black text-zinc-900 dark:text-white">${usdt_c['price']:,.4f}</span>
                </div>
            </div>
            
            <div class="p-6 md:p-12 max-w-7xl mx-auto">
                <header class="flex flex-col md:flex-row justify-between items-center mb-12 border-b border-zinc-200 dark:border-zinc-900 pb-10 gap-8">
                    <div class="flex items-center gap-8">
                        <img src="{ant_face_url}" onerror="this.src='https://i.ibb.co/v6XkYvR/ax-removebg.png'" class="ant-logo w-24 h-24 object-contain" alt="야수">
                        <div>
                            <h1 class="text-5xl font-black text-zinc-900 dark:text-white italic tracking-tighter mb-2">연신내 개미펀드</h1>
                            <p class="text-red-500 font-black text-xs tracking-widest mb-1 uppercase">모든 투자는 본인의 책임입니다.</p>
                        </div>
                    </div>
                    <div class="flex items-center gap-4">
                        <button onclick="toggleTheme()" class="p-3 bg-white dark:bg-[#1e1e1e] border border-zinc-200 dark:border-zinc-800 rounded-full">🌓 테마 전환</button>
                        <div class="text-right p-4 bg-white dark:bg-[#151515] rounded-xl border border-zinc-200 dark:border-zinc-900">
                            <p class="text-sm font-black text-zinc-900 dark:text-white italic">{now}</p>
                        </div>
                    </div>
                </header>

                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
                    {"".join([f'''
                    <div class="bg-white dark:bg-[#1e1e1e] p-6 rounded-2xl border border-zinc-200 dark:border-zinc-800 shadow-md transition-all hover:scale-[1.02]">
                        <h3 class="text-zinc-900 dark:text-white font-black text-lg mb-3 italic tracking-tighter">{r['title']}</h3>
                        <div class="bg-[#D4AF37]/10 p-3 rounded-lg mb-3 text-[#D4AF37] font-black text-xs border border-[#D4AF37]/20">{r['ticker']}</div>
                        <p class="text-zinc-500 dark:text-zinc-400 text-xs font-medium leading-relaxed" style="word-break:keep-all;">{r['reason']}</p>
                    </div>
                    ''' for r in recs])}
                </div>

                <div class="bg-white dark:bg-[#151515] p-8 rounded-3xl border border-zinc-200 dark:border-zinc-900 shadow-xl max-w-md">
                    <h3 class="text-[11px] font-black text-zinc-500 mb-6 uppercase border-l-4 border-[#D4AF37] pl-4 tracking-widest">실적 발표 캘린더 (7D)</h3>
                    {"".join([f'''
                    <div class="mb-4">
                        <p class="text-[10px] font-black text-[#D4AF37] mb-3 border-b border-zinc-800 pb-1">{day["date"]}</p>
                        {"".join([f'''
                        <div class="flex items-center justify-between p-3 rounded-xl border {'border-[#D4AF37] bg-[#D4AF37]/5' if c['rec'] else 'border-zinc-100 dark:border-zinc-800'} mb-2 shadow-sm">
                            <div class="flex items-center gap-3">
                                <img src="https://logo.clearbit.com/{{c['d']}}" class="w-8 h-8 rounded-lg bg-white p-1" onerror="this.src='https://via.placeholder.com/32?text={{c['s']}}'">
                                <div><p class="text-xs font-black text-zinc-900 dark:text-white">{{c['n']}}</p></div>
                            </div>
                            <span class="text-[10px] font-bold text-zinc-400">{{c['t']}}</span>
                        </div>
                        ''' for c in day['companies']])}
                    </div>
                    ''' for day in earnings])}
                </div>
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
                        series: [{{ data: allHistory[sym], type: 'line', smooth: true, symbol: 'none', lineStyle: {{ color: '#D4AF37', width: 2 }}, areaStyle: {{ color: 'rgba(212, 175, 55, 0.1)' }} }}]
                    }});
                }}
            </script>
        </body>
        </html>
        """
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
        logger.info("HTML generated successfully.")
    except Exception as e:
        logger.error(f"HTML Generation Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    d = fetch_top_tier_data()
    r, e = ai_beast_meeting()
    generate_html(d, r, e)
