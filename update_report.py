import yfinance as yf
import datetime
import json
import logging

logging.basicConfig(level=logging.INFO)

# [데이터 수집 로직은 V16.0과 동일]
def fetch_extensive_data():
    assets = {
        "INDEX": {"코스피": "^KS11", "나스닥": "^IXIC", "S&P500": "^GSPC", "공포지수": "^VIX"},
        "ALT": {"비트코인": "BTC-USD", "이더리움": "ETH-USD", "금": "GC=F", "원유": "CL=F"},
        "WATCHLIST": {
            "SOXL": "SOXL", "MSTR": "MSTR", "TQQQ": "TQQQ", "ETHU": "ETHU", 
            "AVGO": "AVGO", "COST": "COST", "ORCL": "ORCL"
        }
    }
    data_pool = {}
    for cat, group in assets.items():
        for name, sym in group.items():
            try:
                t = yf.Ticker(sym)
                h = t.history(period="30d")
                if not h.empty:
                    prices = h['Close'].round(2).tolist()
                    curr, prev = h['Close'].iloc[-1], h['Close'].iloc[-2]
                    chg = ((curr - prev) / prev) * 100
                    data_pool[sym] = {"name": name, "price": curr, "chg": chg, "history": prices}
            except: pass
    return data_pool

def get_earnings_calendar():
    # 위원회 선정 TOP 3 기업에 'recommend': True 속성 부여
    return [
        {"date": "03-05 (오늘)", "companies": [
            {"n": "Best Buy", "s": "BBY", "d": "bestbuy.com", "t": "장전", "rec": False},
            {"n": "Target", "s": "TGT", "d": "target.com", "t": "장전", "rec": False},
            {"n": "Costco", "s": "COST", "d": "costco.com", "t": "장후", "rec": True}
        ]},
        {"date": "03-09 (월)", "companies": [
            {"n": "Oracle", "s": "ORCL", "d": "oracle.com", "t": "장후", "rec": True}
        ]},
        {"date": "03-11 (수)", "companies": [
            {"n": "Broadcom", "s": "AVGO", "d": "broadcom.com", "t": "장후", "rec": True},
            {"n": "Adobe", "s": "ADBE", "d": "adobe.com", "t": "장후", "rec": False}
        ]}
    ]

def generate_html(data, earnings):
    now = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
    
    # 실적 발표 리스트 생성 (롱 타겟 강조 로직)
    earnings_html = ""
    for day in earnings:
        earnings_html += f'<p class="text-[10px] font-black text-[#D4AF37] mb-2 border-b border-zinc-800 pb-1">{day["date"]}</p>'
        for c in day['companies']:
            # 롱 타겟일 경우 금색 테두리와 'LONG' 뱃지 추가
            border_css = "border-[#D4AF37] bg-[#D4AF37]/5" if c['rec'] else "border-zinc-100 dark:border-zinc-800"
            badge = '<span class="bg-[#D4AF37] text-black text-[8px] px-1 rounded font-black ml-2 animate-pulse">LONG</span>' if c['rec'] else ""
            
            earnings_html += f'''
            <div class="flex items-center justify-between p-2 rounded-lg border {border_css} mb-2 transition-all">
                <div class="flex items-center gap-3">
                    <img src="https://logo.clearbit.com/{c['d']}" class="w-6 h-6 rounded-md bg-white p-0.5" onerror="this.src='https://via.placeholder.com/24?text={c['s']}'">
                    <div>
                        <p class="text-[10px] font-black text-zinc-900 dark:text-white leading-none">{c['n']}{badge}</p>
                        <p class="text-[9px] text-zinc-500 font-bold">{c['s']}</p>
                    </div>
                </div>
                <span class="text-[9px] font-bold text-zinc-400">{c['t']}</span>
            </div>'''

    # [중략: 헤더 및 기타 레이아웃은 V16.0과 동일]
    # (toggleTheme 및 다크모드 설정 포함)

    html = f"""
    """
    with open("index.html", "w", encoding="utf-8") as f: f.write(html)

if __name__ == "__main__":
    d = fetch_extensive_data()
    e = get_earnings_calendar()
    generate_html(d, e)
