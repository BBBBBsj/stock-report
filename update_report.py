import yfinance as yf
import datetime
import json
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Beast_V20_3")

def fetch_extensive_data():
    assets = {
        "CURR": {"원/달러": "USDKRW=X", "USDT": "USDT-USD", "USDC": "USDC-USD"},
        "INDEX": {"코스피": "^KS11", "나스닥": "^IXIC", "S&P500": "^GSPC", "공포지수": "^VIX"},
        "CRYPTO": {"비트코인": "BTC-USD", "이더리움": "ETH-USD"},
        "COMM": {"금(Gold)": "GC=F", "은(Silver)": "SI=F", "WTI유": "CL=F", "구리": "HG=F"},
        # 🚨 V20.3: 에러나는 2년/3년물 버리고 연준(Fed) 공식 침체 지표인 3개월물(^IRX) 전격 도입!
        "BONDS": {"미 국채 3개월물": "^IRX", "미 국채 10년물": "^TNX"},
        "WATCH": {"NVDL":"NVDL", "BITX":"BITX", "ETHU":"ETHU", "SOXL":"SOXL", "MSTR":"MSTR", "TQQQ":"TQQQ", "TSLA":"TSLA", "SCHD":"SCHD", "INTC":"INTC", "SNOW":"SNOW", "RIVN":"RIVN", "LABU":"LABU", "VKTX":"VKTX", "CONL":"CONL", "NVDA":"NVDA", "AVGO":"AVGO"}
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
                else:
                    data_pool[sym] = {"name": name, "price": 0.0, "chg": 0.0, "history": [0]*30}
            except:
                data_pool[sym] = {"name": name, "price": 0.0, "chg": 0.0, "history": [0]*30}
    
    krw_rate = data_pool.get("USDKRW=X", {}).get("price", 1400.0)
    
    usdt_usd = data_pool.get("USDT-USD", {}).get("price", 1.0)
    data_pool["USDT_KRW_CALC"] = {"name": "USDT(원)", "price": usdt_usd * krw_rate * 1.01, "chg": data_pool.get("USDT-USD", {}).get("chg", 0.0), "history": [0]*30}

    usdc_usd = data_pool.get("USDC-USD", {}).get("price", 1.0)
    data_pool["USDC_KRW_CALC"] = {"name": "USDC(원)", "price": usdc_usd * krw_rate * 1.01, "chg": data_pool.get("USDC-USD", {}).get("chg", 0.0), "history": [0]*30}

    return data_pool

def ai_meeting_results():
    eco_events = [
        {"d": "03-06 (금)", "t": "미국 2월 고용보고서 (NFP)", "desc": "고용 냉각 시 금리 인하 기대감 상승.", "odds": "LONG 65% : SHORT 35%"},
        {"d": "03-12 (목)", "t": "미국 2월 소비자물가지수 (CPI)", "desc": "인플레이션 재반등 우려. 시장 경계감 극대화.", "odds": "LONG 40% : SHORT 60%"},
        {"d": "03-18 (수)", "t": "FOMC 기준금리 결정 & 연설", "desc": "동결 유력하나 점도표 변화가 핵심.", "odds": "LONG 50% : SHORT 50%"}
    ]

    human_indicator = [
        {"site": "에펨코리아 (해외주식)", "status": "환희 (LONG 80%)", "desc": "TQQQ, SOXL 수익 인증 폭주 중. 조정 징후."},
        {"site": "DC 미주갤", "status": "광기 (LONG 90%)", "desc": "엔비디아, 코인 레버리지 가즈아 도배. 과열 상태."},
        {"site": "일간베스트 (주게)", "status": "혼돈 (LONG 50%)", "desc": "인버스(숏) 물린 유저 조롱과 신규 진입 교차."},
        {"site": "글로벌 SNS (X)", "status": "탐욕 (LONG 75%)", "desc": "AI 버블론 축소, 연말 산타랠리 선반영 여론 지배적."}
    ]

    ultra_beast = {
        "title": "🌌 超越 야수 (재미용 - 초극대 변동성)",
        "ticker": "LABU, VKTX, CONL",
        "reason": "한강뷰 vs 한강물",
        "chart_sym": "LABU"
    }

    summary = {
        "반도체/AI": "엔비디아 하단 지지선 확보. 레버리지(SOXL) 공매도 잔고 임계점 도달로 숏스퀴즈 화약고 상태.",
        "지정학/거시": "달러 강세 및 지정학적 리스크 지속. 국채 금리 상승세가 기술주 밸류에이션을 압박 중.",
        "빅테크": "ETF(QQQ) 자금 유입 가속화. 브로드컴 어닝 서프라이즈 이후 기술주 전반 실적 기대감 고조.",
        "코인/레버리지": "이더리움 현물 수급 폭발. 가상자산 관련주 및 레버리지 종목 변동성 극대화 포착."
    }
    
    recs = [
        {"title": "🔥 싸나이테스트 (엄선)", "ticker": "ETHU, SOXL, MSTR", "reason": "변동성 상위 1% 정예. 숏스퀴즈 타점 및 광기 수급 포착.", "chart_sym": "ETHU"},
        {"title": "🏃‍♂️ 평범이의 숟가락 (엄선)", "ticker": "TQQQ, NVDA, TSLA", "reason": "추세 추종 매매 최적화. 스마트 머니 유입 및 눌림목 반등 구간.", "chart_sym": "TQQQ"},
        {"title": "🛡️ 쫄보들의 안식처 (엄선)", "ticker": "SCHD, TLT, IAU", "reason": "위원회 자산 방어 분과 엄선. 하방 경직성 및 배당 안전성 1위.", "chart_sym": "SCHD"},
        {"title": "🕵️ 세력 형님 뒤쫓기 (엄선)", "ticker": "INTC, SNOW, RIVN", "reason": "장기 바닥권 소외주. 최근 다크풀 및 기관 대량 매집 징후 포착. 폭발 직전.", "chart_sym": "INTC"}
    ]
    options = [
        {"t": "NVDA", "d": "03-20", "p": "135.0", "s": "콜옵션 프리미엄 과열. 135불 수렴 예상.", "chart_sym": "NVDA"},
        {"t": "TSLA", "d": "03-20", "p": "210.0", "s": "맥스페인 부근 횡보 유지. 돌파 시 헤지 매수 폭증.", "chart_sym": "TSLA"},
        {"t": "LABU", "d": "03-27", "p": "125.0", "s": "바이오 수급 유입 시작. 리버설 상방 압력 감지.", "chart_sym": "LABU"},
        {"t": "MSTR", "d": "03-20", "p": "1650", "s": "비트코인 변동성 직결. 콜 프리미엄 과열 주의.", "chart_sym": "MSTR"},
        {"t": "AVGO", "d": "03-20", "p": "140.0", "s": "어닝 서프라이즈 이후 콜옵션 대량 매집 포착.", "chart_sym": "AVGO"}
    ]
    earnings = [
        {"date": "03-05 (목)", "comps": [
            {"n": "Costco", "s": "COST", "d": "costco.com", "t": "장후", "rec": True, "eps": "$3.62", "rev": "$59.1B", "view": "🛡️ 방어력 입증"},
            {"n": "Marvell", "s": "MRVL", "d": "marvell.com", "t": "장후", "rec": False, "eps": "$0.46", "rev": "$1.4B", "view": "AI 매출 확인"},
            {"n": "Kroger", "s": "KR", "d": "kroger.com", "t": "장전", "rec": False, "eps": "$1.13", "rev": "$37.1B", "view": "소비 둔화 우려"},
            {"n": "Burlington", "s": "BURL", "d": "burlington.com", "t": "장전", "rec": True, "eps": "$3.25", "rev": "$3.3B", "view": "할인점 강세"},
            {"n": "Ross Stores", "s": "ROST", "d": "rossstores.com", "t": "장후", "rec": False, "eps": "$1.65", "rev": "$5.8B", "view": "마진 축소 주의"}
        ]},
        {"date": "03-06 (금)", "comps": [
            {"n": "Foot Locker", "s": "FL", "d": "footlocker.com", "t": "장전", "rec": False, "eps": "$0.32", "rev": "$2.2B", "view": "재고 소진 여부"},
            {"n": "Big Lots", "s": "BIG", "d": "biglots.com", "t": "장전", "rec": False, "eps": "-$0.25", "rev": "$1.0B", "view": "파산 리스크"},
            {"n": "Macy's", "s": "M", "d": "macys.com", "t": "장전", "rec": False, "eps": "$1.98", "rev": "$8.0B", "view": "가이던스 하향 우려"},
            {"n": "Nordstrom", "s": "JWN", "d": "nordstrom.com", "t": "장후", "rec": True, "eps": "$0.88", "rev": "$4.3B", "view": "럭셔리 소비 반등"},
            {"n": "Dick's", "s": "DKS", "d": "dickssportinggoods.com", "t": "장전", "rec": True, "eps": "$3.35", "rev": "$3.8B", "view": "견조한 실적 예상"}
        ]},
        {"date": "03-09 (월)", "comps": [
            {"n": "Oracle", "s": "ORCL", "d": "oracle.com", "t": "장후", "rec": True, "eps": "$1.38", "rev": "$13.3B", "view": "🔥 클라우드 모멘텀"},
            {"n": "Asana", "s": "ASAN", "d": "asana.com", "t": "장후", "rec": False, "eps": "-$0.10", "rev": "$168M", "view": "적자 지속"},
            {"n": "MongoDB", "s": "MDB", "d": "mongodb.com", "t": "장후", "rec": True, "eps": "$0.45", "rev": "$430M", "view": "DB 수요 폭발"},
            {"n": "GitLab", "s": "GTLB", "d": "gitlab.com", "t": "장후", "rec": True, "eps": "$0.15", "rev": "$158M", "view": "AI 통합 시너지"},
            {"n": "SentinelOne", "s": "S", "d": "sentinelone.com", "t": "장후", "rec": False, "eps": "-$0.04", "rev": "$169M", "view": "보안 섹터 둔화"}
        ]}
    ]
    return eco_events, human_indicator, ultra_beast, summary, recs, options, earnings

def generate_html(data, eco_events, human_indicator, ultra_beast, summary, recs, options, earnings):
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

        eco_html = ""
        for ev in eco_events:
            eco_html += f'''
            <div class="bg-white dark:bg-[#1e1e1e] p-4 rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-sm relative overflow-hidden">
                <div class="flex justify-between items-start mb-1">
                    <p class="text-red-500 text-[10px] font-black uppercase tracking-widest">{ev['d']}</p>
                    <span class="text-[8px] font-black bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-300 px-1.5 py-0.5 rounded">{ev['odds']}</span>
                </div>
                <p class="text-zinc-900 dark:text-white text-sm font-black mb-2">{ev['t']}</p>
                <p class="text-zinc-500 dark:text-zinc-400 text-[10px] font-bold leading-relaxed">{ev['desc']}</p>
            </div>'''

        human_html = ""
        for h in human_indicator:
            color = "text-red-500" if "LONG" in h['status'] else "text-blue-500"
            bg = "bg-red-50 dark:bg-red-500/10" if "LONG" in h['status'] else "bg-blue-50 dark:bg-blue-500/10"
            human_html += f'''
            <div class="p-4 rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-[#1e1e1e]">
                <p class="text-[10px] font-black text-zinc-500 mb-1">{h['site']}</p>
                <p class="text-sm font-black {color} {bg} inline-block px-2 py-1 rounded mb-2">{h['status']}</p>
                <p class="text-[10px] text-zinc-600 dark:text-zinc-400 font-bold leading-relaxed">{h['desc']}</p>
            </div>'''

        # 🚨 V20.3: 10년물(^TNX) - 3개월물(^IRX) 스프레드 계산 로직 완벽 방어
        yield_10y = data.get('^TNX', {}).get('price', 0)
        yield_3m = data.get('^IRX', {}).get('price', 0)
        
        if yield_10y == 0 or yield_3m == 0:
            spread_status = "⚠️ 통신 지연 - 채권 스프레드 수집중..."
            spread_color = "text-yellow-500 bg-yellow-50 border-yellow-200 dark:bg-yellow-500/10 dark:border-yellow-900"
        else:
            spread = yield_10y - yield_3m
            if spread < 0:
                spread_status = f"🚨 역전 ({spread:.2f}%p) - 장단기 금리(3M/10Y) 역전! 연준(Fed) 경기침체 경고 시그널."
                spread_color = "text-red-500 bg-red-50 border-red-200 dark:bg-red-500/10 dark:border-red-900"
            else:
                spread_status = f"✅ 정상 ({spread:.2f}%p) - 10년물이 단기채보다 높음. 시장 충격 가능성 제한적."
                spread_color = "text-green-500 bg-green-50 border-green-200 dark:bg-green-500/10 dark:border-green-900"

        bonds_html = f'''
        <div class="col-span-1 md:col-span-2 p-3 mb-2 rounded-xl border {spread_color} flex items-center gap-2 shadow-sm">
            <p class="text-[11px] font-black">{spread_status}</p>
        </div>
        '''

        bond_rules = {
            "^IRX": {"name": "단기채 (3개월물)"},
            "^TNX": {"name": "장기채 (10년물)"}
        }
        for sym, info in bond_rules.items():
            d = data.get(sym, {'price':0, 'chg':0, 'history':[0]*30})
            color = 'text-red-500' if d['chg'] > 0 else 'text-blue-500'
            bonds_html += f'''
            <div class="group relative bg-white dark:bg-[#1e1e1e] p-3 rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-sm" onmouseenter="showChart('{sym}')">
                <div class="flex justify-between items-center mb-1">
                    <p class="text-[10px] font-black text-zinc-600 dark:text-zinc-400">{info['name']}</p>
                    <p class="{color} text-[9px] font-bold bg-zinc-100 dark:bg-black px-1 rounded">{d['chg']:+.2f}%</p>
                </div>
                <p class="text-lg font-black italic text-zinc-900 dark:text-white mb-1">{d['price']:,.3f}%</p>
                <div id="chart-container-{sym}" class="absolute z-50 bottom-full left-0 mb-2 w-56 h-32 bg-black border border-zinc-700 rounded-xl p-2 hidden shadow-2xl pointer-events-none group-hover:block"><div id="chart-{sym}" class="w-full h-full"></div></div>
            </div>'''

        index_cards = ""
        for s in ["^KS11", "^IXIC", "^GSPC", "^VIX", "BTC-USD", "ETH-USD"]:
            d = data.get(s, {'name': s, 'price':0, 'chg':0, 'history': [0]*30})
            color = 'text-red-500' if d['chg'] > 0 else 'text-blue-500'
            index_cards += f'''
            <div class="group relative bg-white dark:bg-[#1e1e1e] p-4 rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-sm transition-all" onmouseenter="showChart('{s}')">
                <p class="text-[10px] text-zinc-500 font-bold mb-1">{d['name']}</p>
                <p class="text-lg font-black italic text-zinc-900 dark:text-white">{d['price']:,.1f}</p>
                <p class="{color} text-[11px] font-bold">{d['chg']:+.2f}%</p>
                <div id="chart-container-{s}" class="absolute z-50 bottom-full left-0 mb-2 w-56 h-32 bg-black border border-zinc-700 rounded-xl p-2 hidden shadow-2xl pointer-events-none group-hover:block"><div id="chart-{s}" class="w-full h-full"></div></div>
            </div>'''

        comm_cards = ""
        for s in ["GC=F", "SI=F", "CL=F", "HG=F"]:
            d = data.get(s, {'name': s, 'price':0, 'chg':0, 'history': [0]*30})
            color = 'text-red-500' if d['chg'] > 0 else 'text-blue-500'
            comm_cards += f'''
            <div class="group relative bg-zinc-50 dark:bg-[#151515] p-3 rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-sm" onmouseenter="showChart('{s}')">
                <p class="text-[9px] text-zinc-500 font-bold mb-1">{d['name']}</p>
                <p class="text-base font-black italic text-zinc-900 dark:text-white">{d['price']:,.2f}</p>
                <p class="{color} text-[10px] font-bold">{d['chg']:+.2f}%</p>
                <div id="chart-container-{s}" class="absolute z-50 bottom-full left-0 mb-2 w-56 h-32 bg-black border border-zinc-700 rounded-xl p-2 hidden shadow-2xl pointer-events-none group-hover:block"><div id="chart-{s}" class="w-full h-full"></div></div>
            </div>'''

        summary_html = "".join([f'<div class="mb-2"><span class="text-[#D4AF37] font-black text-xs mr-2">[{k}]</span><span class="text-zinc-600 dark:text-zinc-300 text-xs font-bold leading-relaxed">{v}</span></div>' for k,v in summary.items()])

        ultra_beast_html = f'''
        <div class="group relative bg-zinc-900 p-8 rounded-3xl border-4 border-dashed border-red-600 shadow-2xl shadow-red-500/20 animate-pulse mb-8 text-center overflow-visible" onmouseenter="showChart('{ultra_beast['chart_sym']}')">
            <div class="absolute -right-10 -top-10 text-[200px] text-red-500 opacity-5 font-black italic">!</div>
            <h2 class="text-2xl font-black text-white italic tracking-tighter mb-4">{ultra_beast['title']}</h2>
            <div class="bg-red-500/20 p-4 rounded-xl mb-6 text-red-500 font-black text-lg border-2 border-red-500/30 tracking-[0.3em] inline-block">{ultra_beast['ticker']}</div>
            <p class="text-red-500 text-3xl font-black italic leading-relaxed drop-shadow-[0_0_15px_rgba(239,68,68,0.8)] tracking-tighter">{ultra_beast['reason']}</p>
            <div id="chart-container-{ultra_beast['chart_sym']}" class="absolute z-50 top-full left-1/2 -translate-x-1/2 mt-4 w-64 h-40 bg-black border border-red-500 rounded-xl p-2 hidden shadow-2xl pointer-events-none group-hover:block"><div id="chart-{ultra_beast['chart_sym']}" class="w-full h-full"></div></div>
        </div>'''

        rec_cards = "".join([f'''
            <div class="group relative bg-white dark:bg-[#1e1e1e] p-6 rounded-2xl border border-zinc-200 dark:border-zinc-800 shadow-md" onmouseenter="showChart('{r['chart_sym']}')">
                <h3 class="text-zinc-900 dark:text-white font-black text-lg mb-3 italic tracking-tighter">{r['title']}</h3>
                <div class="bg-[#D4AF37]/10 p-3 rounded-lg mb-3 text-[#D4AF37] font-black text-xs border border-[#D4AF37]/20">{r['ticker']}</div>
                <p class="text-zinc-500 dark:text-zinc-400 text-xs font-medium leading-relaxed" style="word-break:keep-all;">{r['reason']}</p>
                <div id="chart-container-{r['chart_sym']}" class="absolute z-50 bottom-full left-0 mb-2 w-56 h-32 bg-black border border-zinc-700 rounded-xl p-2 hidden shadow-2xl pointer-events-none group-hover:block"><div id="chart-{r['chart_sym']}" class="w-full h-full"></div></div>
            </div>''' for r in recs])

        options_html = "".join([f'''
            <div class="group relative bg-white dark:bg-[#151515] p-4 rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-sm overflow-visible" onmouseenter="showChart('{o['chart_sym']}')">
                <div class="absolute right-1 top-1 text-red-500/10 text-4xl font-black">!</div>
                <div class="flex justify-between mb-1 border-b border-zinc-100 dark:border-zinc-800 pb-1 relative z-10">
                    <span class="text-zinc-900 dark:text-white font-black text-xs">{o['t']}</span>
                    <span class="text-red-500 text-[9px] font-bold">{o['d']} 만기</span>
                </div>
                <div class="flex justify-between my-1 relative z-10"><span class="text-zinc-500 text-[9px] font-bold uppercase">MAX PAIN</span><span class="text-zinc-900 dark:text-white font-black text-[10px]">{o['p']}</span></div>
                <p class="text-zinc-600 dark:text-zinc-400 text-[10px] leading-tight font-bold relative z-10">{o['s']}</p>
                <div id="chart-container-{o['chart_sym']}" class="absolute z-50 bottom-full left-0 mb-2 w-48 h-24 bg-black border border-zinc-700 rounded-xl p-2 hidden shadow-2xl pointer-events-none group-hover:block"><div id="chart-{o['chart_sym']}" class="w-full h-full"></div></div>
            </div>''' for o in options])

        earnings_html = ""
        for day in earnings:
            earnings_html += f'<p class="text-[10px] font-black text-[#D4AF37] mb-3 border-b border-zinc-100 dark:border-zinc-800 pb-1">{day["date"]}</p>'
            for c in day['comps']:
                style = "border-[#D4AF37] bg-[#D4AF37]/5" if c['rec'] else "border-zinc-100 dark:border-zinc-800"
                view_color = "text-[#D4AF37]" if c['rec'] else "text-zinc-500"
                badge = '<span class="bg-[#D4AF37] text-black text-[8px] px-1 rounded font-black ml-2 animate-pulse">LONG</span>' if c['rec'] else ""
                fallback_img = f"https://ui-avatars.com/api/?name={c['n']}&background=2d3748&color=fff&size=64&bold=true"
                earnings_html += f'''
                <div class="flex items-center justify-between p-3 rounded-xl border {style} mb-3 shadow-sm hover:bg-zinc-50 dark:hover:bg-zinc-800/50 transition">
                    <div class="flex items-center gap-3 w-1/2">
                        <img src="https://logo.clearbit.com/{c['d']}" class="w-8 h-8 rounded-lg bg-zinc-100 dark:bg-white p-1 object-contain" onerror="this.onerror=null; this.src='{fallback_img}'">
                        <div class="truncate">
                            <p class="text-[11px] font-black text-zinc-900 dark:text-white truncate">{c['n']}{badge}</p>
                            <p class="text-[9px] font-bold text-zinc-500 mt-0.5">EPS: <span class="text-blue-500 dark:text-blue-400">{c['eps']}</span> | Rev: <span class="text-zinc-700 dark:text-zinc-300">{c['rev']}</span></p>
                        </div>
                    </div>
                    <div class="text-right w-1/2">
                        <span class="text-[9px] font-black text-zinc-400 bg-zinc-100 dark:bg-zinc-800 px-1.5 py-0.5 rounded">{c['t']}</span>
                        <p class="text-[9px] font-black {view_color} mt-1.5 truncate">{c['view']}</p>
                    </div>
                </div>'''

        base_html = """
        <!DOCTYPE html>
        <html lang="ko" class="dark">
        <head>
            <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>연신내 개미펀드 V20.3</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
                body { font-family: 'Noto Sans KR', sans-serif; transition: background-color 0.3s; }
                @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
                .ant-logo { animation: spin 8s linear infinite; transition: transform 0.3s; filter: drop-shadow(0 0 10px rgba(212,175,55,0.4)); }
                .ant-logo:hover { animation-play-state: paused; transform: scale(1.1); }
            </style>
            <script>
                tailwind.config = { darkMode: 'class' };
                function toggleTheme() { 
                    const doc = document.documentElement;
                    const btn = document.getElementById('theme-btn');
                    if(doc.classList.contains('dark')) {
                        doc.classList.remove('dark');
                        btn.innerText = '다크 모드 전환';
                    } else {
                        doc.classList.add('dark');
                        btn.innerText = '라이트 모드 전환';
                    }
                }
            </script>
        </head>
        <body class="bg-zinc-50 dark:bg-[#0d0d0d] text-zinc-900 dark:text-zinc-300">
            __CURRENCY__
            <div class="p-6 md:p-12 max-w-7xl mx-auto">
                <header class="flex flex-col md:flex-row justify-between items-center mb-8 border-b border-zinc-200 dark:border-zinc-900 pb-8 gap-8 gap-y-6">
                    <div class="flex items-center gap-8">
                        <img src="ax.png" onerror="this.onerror=null; this.src='ax.jpg'; this.onerror=function(){this.onerror=null; this.src='https://i.ibb.co/v6XkYvR/ax-removebg.png'};" class="ant-logo w-24 h-24 object-contain" alt="야수">
                        <div>
                            <h1 class="text-5xl font-black text-zinc-900 dark:text-white italic tracking-tighter mb-2">연신내 개미펀드</h1>
                            <p class="text-red-500 font-black text-xs tracking-widest mb-1 uppercase">모든 투자는 본인의 책임입니다.</p>
                        </div>
                    </div>
                    <div class="flex items-center gap-4 bg-white dark:bg-[#151515] p-3 rounded-xl border border-zinc-200 dark:border-zinc-900 shadow-sm">
                        <button id="theme-btn" onclick="toggleTheme()" class="px-4 py-2 text-[10px] font-black text-zinc-600 dark:text-zinc-300 bg-zinc-100 dark:bg-[#1e1e1e] border border-zinc-200 dark:border-zinc-800 rounded-full shadow-lg hover:bg-[#D4AF37] hover:text-black transition">라이트 모드 전환</button>
                        <div class="text-right pl-3 border-l border-zinc-100 dark:border-zinc-800">
                            <p class="text-[9px] text-zinc-500 font-black mb-1 tracking-widest uppercase">KST SYNC</p>
                            <p class="text-sm font-black text-zinc-900 dark:text-white italic">__NOW__</p>
                        </div>
                    </div>
                </header>

                <h2 class="text-[10px] font-black text-zinc-500 mb-4 tracking-[0.3em] uppercase flex items-center gap-3">
                    <span class="w-10 h-[1px] bg-zinc-300 dark:bg-zinc-800"></span> 글로벌 매크로 & 연준(Fed) 주요 일정
                </h2>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">__ECO_EVENTS__</div>

                <div class="bg-white dark:bg-[#151515] p-6 rounded-3xl border border-zinc-200 dark:border-zinc-900 shadow-xl mb-8 relative">
                    <div class="absolute -right-5 -top-5 text-[100px] opacity-5 font-black">👥</div>
                    <h2 class="text-[11px] font-black text-zinc-500 mb-4 tracking-[0.3em] uppercase flex items-center gap-3 relative z-10">
                        <span class="w-10 h-[1px] bg-zinc-300 dark:bg-zinc-800"></span> 🧠 인간지표 & 개미 센티먼트 (커뮤니티 통합)
                    </h2>
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 relative z-10">__HUMAN__</div>
                    <div class="mt-4 p-4 bg-red-50 dark:bg-red-500/10 rounded-xl border border-red-100 dark:border-red-500/20 relative z-10">
                        <p class="text-[11px] font-black text-red-500">🔥 위원회 경고: 현재 커뮤니티 전반에 롱(LONG) 환희 포착. 단기 조정(숏스퀴즈 반대 급부)에 극도로 대비하십시오.</p>
                    </div>
                </div>

                <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-4">__INDEX__</div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
                    <div>
                        <h2 class="text-[10px] font-black text-zinc-500 mb-3 tracking-[0.3em] uppercase flex items-center gap-3">
                            <span class="w-10 h-[1px] bg-zinc-300 dark:bg-zinc-800"></span> 국채 금리 스프레드 (시장 충격 지표)
                        </h2>
                        <div class="grid grid-cols-2 gap-4">__BONDS__</div>
                    </div>
                    <div>
                        <h2 class="text-[10px] font-black text-zinc-500 mb-3 tracking-[0.3em] uppercase flex items-center gap-3">
                            <span class="w-10 h-[1px] bg-zinc-300 dark:bg-zinc-800"></span> 원자재 (Commodities)
                        </h2>
                        <div class="grid grid-cols-2 gap-4">__COMMODITIES
