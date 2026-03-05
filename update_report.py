import yfinance as yf
import datetime
import json
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Beast_V18_2")

def fetch_extensive_data():
    assets = {
        "CURR": {"원/달러": "USDKRW=X", "USDT": "USDT-USD", "USDC": "USDC-USD"},
        "INDEX": {"코스피": "^KS11", "나스닥": "^IXIC", "S&P500": "^GSPC", "공포지수": "^VIX"},
        "CRYPTO": {"비트코인": "BTC-USD", "이더리움": "ETH-USD"}
    }
    data_pool = {}
    for cat, group in assets.items():
        for name, sym in group.items():
            try:
                t = yf.Ticker(sym)
                h = t.history(period="7d")
                if len(h) >= 2:
                    prices = h['Close'].round(2).tolist()
                    curr, prev = h['Close'].iloc[-1], h['Close'].iloc[-2]
                    chg = ((curr - prev) / prev) * 100
                    data_pool[sym] = {"name": name, "price": curr, "chg": chg, "history": prices}
                else:
                    data_pool[sym] = {"name": name, "price": 0.0, "chg": 0.0, "history": [0,0]}
            except:
                data_pool[sym] = {"name": name, "price": 0.0, "chg": 0.0, "history": [0,0]}
    
    # 🚨 USDT/USDC 원화 환산 및 'history' 에러 완벽 해결
    krw_rate = data_pool.get("USDKRW=X", {}).get("price", 1400.0)
    
    usdt_usd = data_pool.get("USDT-USD", {}).get("price", 1.0)
    usdt_chg = data_pool.get("USDT-USD", {}).get("chg", 0.0)
    data_pool["USDT_KRW_CALC"] = {"name": "USDT(원)", "price": usdt_usd * krw_rate * 1.01, "chg": usdt_chg, "history": [0,0]}

    usdc_usd = data_pool.get("USDC-USD", {}).get("price", 1.0)
    usdc_chg = data_pool.get("USDC-USD", {}).get("chg", 0.0)
    data_pool["USDC_KRW_CALC"] = {"name": "USDC(원)", "price": usdc_usd * krw_rate * 1.01, "chg": usdc_chg, "history": [0,0]}

    return data_pool

def ai_meeting_results():
    summary = {
        "반도체/AI": "엔비디아 하단 지지선 확보. 레버리지(SOXL) 공매도 잔고 임계점 도달로 숏스퀴즈 화약고 상태.",
        "지정학/거시": "달러 강세 및 지정학적 리스크 지속. 안전자산과 코인 시장으로의 자금 양극화 현상 심화.",
        "빅테크": "ETF(QQQ) 자금 유입 가속화. 이번 주 실적 발표 기업 가이던스 상향 기대감 선반영.",
        "코인/레버리지": "이더리움 현물 수급 폭발. 가상자산 관련주(MSTR, MARA) 변동성 극대화 및 세력 매집 포착."
    }
    recs = [
        {"title": "🔥 싸나이테스트 (엄선)", "ticker": "ETHU, SOXL, MSTR", "reason": "변동성 상위 1% 정예. 숏스퀴즈 타점 및 광기 수급 포착."},
        {"title": "🏃‍♂️ 평범이의 숟가락 (엄선)", "ticker": "TQQQ, NVDA, TSLA", "reason": "추세 추종 매매 최적화. 스마트 머니 유입 및 눌림목 반등 구간."},
        {"title": "🛡️ 쫄보들의 안식처 (엄선)", "ticker": "SCHD, TLT, IAU", "reason": "위원회 자산 방어 분과 엄선. 하방 경직성 및 배당 안전성 1위."},
        {"title": "🕵️ 세력 형님 뒤쫓기 (엄선)", "ticker": "LABU, COIN, MARA", "reason": "온체인 대량 매집 시그널. 공매도 항복 임박한 리버설 타점 요격."}
    ]
    options = [
        {"t": "NVDA", "d": "03-20", "p": "135.0", "s": "콜옵션 프리미엄 과열. 135불 수렴 예상."},
        {"t": "TSLA", "d": "03-20", "p": "210.0", "s": "맥스페인 부근 횡보 유지. 돌파 시 헤지 매수 폭증."},
        {"t": "ETHU", "d": "03-27", "p": "15.0", "s": "이더리움 2배 옵션 신규 매수세 유입."},
        {"t": "SOXL", "d": "03-20", "p": "45.0", "s": "세력들 하단 42불 강력 지지 중."},
        {"t": "LABU", "d": "03-27", "p": "125.0", "s": "바이오 수급 유입 시작. 리버설 상방 압력 감지."}
    ]
    # 🚨 실적 발표 7일 (EPS, 매출, 위원회 View 추가 반영)
    earnings = [
        {"date": "03-05 (오늘/목)", "comps": [
            {"n": "Broadcom", "s": "AVGO", "d": "broadcom.com", "t": "장후", "rec": True, "eps": "$1.04", "rev": "$11.9B", "view": "🔥 AI모멘텀 (LONG)"},
            {"n": "Costco", "s": "COST", "d": "costco.com", "t": "장후", "rec": True, "eps": "$3.62", "rev": "$59.1B", "view": "🛡️ 안정적 (HOLD)"}
        ]},
        {"date": "03-06 (금)", "comps": [
            {"n": "Marvell", "s": "MRVL", "d": "marvell.com", "t": "장전", "rec": False, "eps": "$0.46", "rev": "$1.4B", "view": "가이던스 확인 요망"}
        ]},
        {"date": "03-09 (월)", "comps": [
            {"n": "Oracle", "s": "ORCL", "d": "oracle.com", "t": "장후", "rec": True, "eps": "$1.38", "rev": "$13.3B", "view": "클라우드 성장 기대"}
        ]},
        {"date": "03-10 (화)", "comps": [
            {"n": "Asana", "s": "ASAN", "d": "asana.com", "t": "장후", "rec": False, "eps": "-$0.10", "rev": "$168M", "view": "적자폭 축소 여부"}
        ]},
        {"date": "03-11 (수)", "comps": [
            {"n": "Adobe", "s": "ADBE", "d": "adobe.com", "t": "장후", "rec": False, "eps": "$4.38", "rev": "$5.1B", "view": "AI 수익화 증명 필요"}
        ]}
    ]
    return summary, recs, options, earnings

def generate_html(data, summary, recs, options, earnings):
    try:
        now = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
        
        usd_krw = data.get('USDKRW=X', {'price':0, 'chg':0})
        usdt_krw = data.get('USDT_KRW_CALC', {'price':0, 'chg':0})
        usdc_krw = data.get('USDC_KRW_CALC', {'price':0, 'chg':0})

        currency_html = f'''
        <div class="flex gap-6 p-4 bg-white dark:bg-[#151515] border-b border-zinc-200 dark:border-zinc-800 overflow-x-auto shadow-sm">
            <div class="flex items-center gap-3 whitespace-nowrap">
                <span class="text-[11px] font-bold text-zinc-500">💵 원/달러</span>
                <span class="text-sm font-black text-zinc-900 dark:text-white">{usd_krw['price']:,.2f} 원</span>
                <span class="text-[10px] font-bold {'text-red-500' if usd_krw['chg'] > 0 else 'text-blue-500'}">{usd_krw['chg']:+.2f}%</span>
            </div>
            <div class="w-[1px] h-4 bg-zinc-300 dark:bg-zinc-700"></div>
            <div class="flex items-center gap-3 whitespace-nowrap">
                <span class="text-[11px] font-bold text-zinc-500">🔗 USDT(테더)</span>
                <span class="text-sm font-black text-zinc-900 dark:text-white">{usdt_krw['price']:,.1f} 원</span>
                <span class="text-[10px] font-bold {'text-red-500' if usdt_krw['chg'] > 0 else 'text-blue-500'}">{usdt_krw['chg']:+.2f}%</span>
            </div>
            <div class="w-[1px] h-4 bg-zinc-300 dark:bg-zinc-700"></div>
            <div class="flex items-center gap-3 whitespace-nowrap">
                <span class="text-[11px] font-bold text-zinc-500">🔗 USDC(서클)</span>
                <span class="text-sm font-black text-zinc-900 dark:text-white">{usdc_krw['price']:,.1f} 원</span>
                <span class="text-[10px] font-bold {'text-red-500' if usdc_krw['chg'] > 0 else 'text-blue-500'}">{usdc_krw['chg']:+.2f}%</span>
            </div>
        </div>'''

        index_cards = ""
        for s in ["^KS11", "^IXIC", "^GSPC", "^VIX", "BTC-USD", "ETH-USD"]:
            d = data.get(s, {'name': s, 'price':0, 'chg':0, 'history': [0,0]})
            color = 'text-red-500' if d['chg'] > 0 else 'text-blue-500'
            index_cards += f'''
            <div class="bg-white dark:bg-[#1e1e1e] p-4 rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-sm transition-all" onmouseenter="showChart('{s}')">
                <p class="text-[10px] text-zinc-500 font-bold mb-1">{d['name']}</p>
                <p class="text-lg font-black italic text-zinc-900 dark:text-white">{d['price']:,.1f}</p>
                <p class="{color} text-[11px] font-bold">{d['chg']:+.2f}%</p>
                <div id="chart-container-{s}" class="absolute z-50 bottom-full left-0 mb-2 w-56 h-32 bg-black border border-zinc-700 rounded-xl p-2 hidden shadow-2xl pointer-events-none group-hover:block"><div id="chart-{s}" class="w-full h-full"></div></div>
            </div>'''

        summary_html = "".join([f'<div class="mb-2"><span class="text-[#D4AF37] font-black text-xs mr-2">[{k}]</span><span class="text-zinc-600 dark:text-zinc-300 text-xs font-bold leading-relaxed">{v}</span></div>' for k,v in summary.items()])

        rec_cards = "".join([f'''
            <div class="bg-white dark:bg-[#1e1e1e] p-6 rounded-2xl border border-zinc-200 dark:border-zinc-800 shadow-md">
                <h3 class="text-zinc-900 dark:text-white font-black text-lg mb-3 italic tracking-tighter">{r['title']}</h3>
                <div class="bg-[#D4AF37]/10 p-3 rounded-lg mb-3 text-[#D4AF37] font-black text-xs border border-[#D4AF37]/20">{r['ticker']}</div>
                <p class="text-zinc-500 dark:text-zinc-400 text-xs font-medium leading-relaxed">{r['reason']}</p>
            </div>''' for r in recs])

        options_html = "".join([f'''
            <div class="bg-white dark:bg-[#151515] p-4 rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-sm">
                <div class="flex justify-between mb-1 border-b border-zinc-100 dark:border-zinc-800 pb-1">
                    <span class="text-zinc-900 dark:text-white font-black text-xs">{o['t']}</span>
                    <span class="text-red-500 text-[9px] font-bold">{o['d']} 만기</span>
                </div>
                <div class="flex justify-between my-1"><span class="text-zinc-500 text-[9px] font-bold uppercase">MAX PAIN</span><span class="text-zinc-900 dark:text-white font-black text-[10px]">{o['p']}</span></div>
                <p class="text-zinc-600 dark:text-zinc-400 text-[10px] leading-tight font-bold">{o['s']}</p>
            </div>''' for o in options])

        # EPS & Revenue 렌더링 HTML 보강
        earnings_html = ""
        for day in earnings:
            earnings_html += f'<p class="text-[10px] font-black text-[#D4AF37] mb-3 border-b border-zinc-100 dark:border-zinc-800 pb-1">{day["date"]}</p>'
            for c in day['comps']:
                style = "border-[#D4AF37] bg-[#D4AF37]/5" if c['rec'] else "border-zinc-100 dark:border-zinc-800"
                view_color = "text-[#D4AF37]" if c['rec'] else "text-zinc-500"
                earnings_html += f'''
                <div class="flex items-center justify-between p-3 rounded-xl border {style} mb-3 shadow-sm hover:bg-zinc-50 dark:hover:bg-zinc-800/50 transition">
                    <div class="flex items-center gap-3">
                        <img src="https://logo.clearbit.com/{c['d']}" class="w-9 h-9 rounded-lg bg-zinc-100 dark:bg-white p-1" onerror="this.src='https://via.placeholder.com/36?text={c['s']}'">
                        <div>
                            <p class="text-xs font-black text-zinc-900 dark:text-white">{c['n']} <span class="text-[9px] text-zinc-400 font-bold ml-1">{c['s']}</span></p>
                            <p class="text-[10px] font-bold text-zinc-500 mt-0.5">EPS: <span class="text-blue-500 dark:text-blue-400">{c['eps']}</span> | Rev: <span class="text-zinc-700 dark:text-zinc-300">{c['rev']}</span></p>
                        </div>
                    </div>
                    <div class="text-right">
                        <span class="text-[9px] font-black text-zinc-400 bg-zinc-100 dark:bg-zinc-800 px-1.5 py-0.5 rounded">{c['t']}</span>
                        <p class="text-[9px] font-black {view_color} mt-1.5">{c['view']}</p>
                    </div>
                </div>'''

        base_html = """
        <!DOCTYPE html>
        <html lang="ko" class="dark">
        <head>
            <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>연신내 개미펀드 V18.2</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
                body { font-family: 'Noto Sans KR', sans-serif; transition: background-color 0.3s; }
                @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
                .ant-logo { animation: spin 20s linear infinite; filter: drop-shadow(0 0 10px rgba(212,175,55,0.4)); }
            </style>
            <script>
                tailwind.config = { darkMode: 'class' };
                function toggleTheme() { document.documentElement.classList.toggle('dark'); }
            </script>
        </head>
        <body class="bg-zinc-50 dark:bg-[#0d0d0d] text-zinc-900 dark:text-zinc-300">
            __CURRENCY__
            <div class="p-6 md:p-12 max-w-7xl mx-auto">
                <header class="flex flex-col md:flex-row justify-between items-center mb-12 border-b border-zinc-200 dark:border-zinc-900 pb-10 gap-8">
                    <div class="flex items-center gap-8">
                        <img src="ax.png" onerror="this.src='https://i.ibb.co/v6XkYvR/ax-removebg.png'" class="ant-logo w-24 h-24 object-contain" alt="야수">
                        <div>
                            <h1 class="text-5xl font-black text-zinc-900 dark:text-white italic tracking-tighter mb-2">연신내 개미펀드</h1>
                            <p class="text-red-500 font-black text-xs tracking-widest mb-1 uppercase">모든 투자는 본인의 책임입니다.</p>
                        </div>
                    </div>
                    <div class="flex items-center gap-4">
                        <button onclick="toggleTheme()" class="p-3 bg-white dark:bg-[#1e1e1e] border border-zinc-200 dark:border-zinc-800 rounded-full shadow-lg">🌓 테마 전환</button>
                        <div class="text-right p-4 bg-white dark:bg-[#151515] rounded-xl border border-zinc-200 dark:border-zinc-900 shadow-sm">
                            <p class="text-[9px] text-zinc-500 font-black mb-1">KST SYNC</p>
                            <p class="text-sm font-black text-zinc-900 dark:text-white italic">__NOW__</p>
                        </div>
                    </div>
                </header>

                <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-12">__INDEX__</div>

                <div class="grid grid-cols-1 lg:grid-cols-4 gap-8 mb-16">
                    <div class="lg:col-span-3">
                        <div class="bg-white dark:bg-[#151515] p-8 rounded-3xl border border-zinc-200 dark:border-zinc-900 shadow-xl mb-8 relative overflow-hidden">
                            <h2 class="text-2xl font-black text-zinc-900 dark:text-white mb-6 italic">🏛️ 위원회 섹터 요약</h2>
                            <div class="space-y-1 relative z-10">__SUMMARY__</div>
                        </div>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">__RECS__</div>
                        <h2 class="text-[10px] font-black text-zinc-500 mb-4 tracking-[0.3em] uppercase flex items-center gap-3">
                            <span class="w-10 h-[1px] bg-zinc-300 dark:bg-zinc-800"></span> 옵션 세력 분석 & MAX PAIN
                        </h2>
                        <div class="grid grid-cols-2 md:grid-cols-5 gap-3">__OPTIONS__</div>
                    </div>
                    
                    <div class="bg-white dark:bg-[#151515] p-8 rounded-3xl border border-zinc-200 dark:border-zinc-900 shadow-xl h-fit">
                        <h3 class="text-[11px] font-black text-zinc-500 mb-6 uppercase border-l-4 border-[#D4AF37] pl-4 tracking-widest">실적 발표 & 펀더멘털 (7D)</h3>
                        <div class="space-y-4">__EARNINGS__</div>
                    </div>
                </div>
            </div>

            <script>
                const allHistory = __HISTORY__;
                function showChart(sym) {
                    const container = document.getElementById('chart-' + sym);
                    if(!container) return;
                    const chart = echarts.init(container);
                    chart.setOption({
                        grid: { top: 10, bottom: 10, left: 10, right: 10 },
                        xAxis: { type: 'category', show: false },
                        yAxis: { type: 'value', show: false, min: 'dataMin', max: 'dataMax' },
                        series: [{ data: allHistory[sym], type: 'line', smooth: true, symbol: 'none', lineStyle: { color: '#D4AF37', width: 2 }, areaStyle: { color: 'rgba(212, 175, 55, 0.1)' } }]
                    });
                }
            </script>
        </body>
        </html>
        """
        
        history_json = json.dumps({sym: d.get('history', [0,0]) for sym, d in data.items()})
        final_html = base_html.replace("__CURRENCY__", currency_html)
        final_html = final_html.replace("__NOW__", now)
        final_html = final_html.replace("__INDEX__", index_cards)
        final_html = final_html.replace("__SUMMARY__", summary_html)
        final_html = final_html.replace("__RECS__", rec_cards)
        final_html = final_html.replace("__OPTIONS__", options_html)
        final_html = final_html.replace("__EARNINGS__", earnings_html)
        final_html = final_html.replace("__HISTORY__", history_json)

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(final_html)
        logger.info("V18.2 HTML successfully generated.")

    except Exception as e:
        logger.error(f"Generation Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    d = fetch_extensive_data()
    s, r, o, e = ai_meeting_results()
    generate_html(d, s, r, o, e)
