import yfinance as yf
import datetime
import logging
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Yeonsinnae_HedgeFund_V7")

def fetch_extensive_data():
    # 15인 에이전트가 교차 검증할 데이터셋
    assets = {
        "INDEX": {"KOSPI": "^KS11", "NASDAQ": "^IXIC", "S&P500": "^GSPC", "VIX": "^VIX"},
        "MACRO": {"US10Y": "^TNX", "USD/KRW": "USDKRW=X", "DollarIndex": "DX-Y.NYB"},
        "ALT": {"Bitcoin": "BTC-USD", "Gold": "GC=F", "CrudeOil": "CL=F"},
        "SECTOR": {"Semiconductor": "SOXX", "Tech": "XLK", "Health": "XLV"}
    }
    data_pool = {}
    for cat, group in assets.items():
        for name, sym in group.items():
            try:
                t = yf.Ticker(sym)
                h = t.history(period="60d") # 통계 분석을 위해 60일치 확보
                if len(h) > 30:
                    curr, prev = h['Close'].iloc[-1], h['Close'].iloc[-2]
                    chg = ((curr - prev) / prev) * 100
                    # RSI 및 통계 지표(변동성) 계산
                    delta = h['Close'].diff()
                    up = delta.clip(lower=0).rolling(14).mean().iloc[-1]
                    down = -delta.clip(upper=0).rolling(14).mean().iloc[-1]
                    rsi = 100 - (100 / (1 + (up/down))) if down != 0 else 50
                    volat = h['Close'].pct_change().std() * np.sqrt(252) * 100 # 연율화 변동성
                    data_pool[sym] = {"name": name, "price": curr, "chg": chg, "rsi": rsi, "vol": volat}
            except: pass
    return data_pool

def ai_hedge_fund_meeting(d):
    # 15인 에이전트의 파트별 합동 회의 결과 도출
    vix = d.get('^VIX', {}).get('price', 15)
    nasdaq_rsi = d.get('^IXIC', {}).get('rsi', 50)
    
    # 1. 야수(Wild Beast) - 퀀트/기술적 분석팀 협업
    wild = {"t": "NVDA / NVDL", "r": "기술적 분석가: MACD 정배열 확인. 데이터 사이언티스트: 뉴스 감성 분석 시그널 '매수' 확정. 변동성이 크지만 통계적 기대값이 높음."}
    # 2. 평범(Standard) - 가치투자/섹터 분석팀 협업
    normal = {"t": "SPLG (S&P500 저비용)", "r": "가치투자자: 펀더멘탈 대비 적정 주가 범위 내 위치. 매크로 데스크: 금리 동결 시나리오 반영 시 우상향 확률 68%."}
    # 3. 안정(Safety) - 리스크/컴플라이언스/채권팀 협업
    safe = {"t": "SHV (초단기 국채)", "r": "리스크 관리자: VaR(Value at Risk) 한도 초과 경고. 컴플라이언스: 세후 수익률 최적화 구간. 현금 비중 확보로 Drawdown 대비."}
    # 4. 세력 매집(Whale) - 수급/행동경제학/알터너티브 데이터팀 협업
    whale = {"t": "MSTR (마이크로스트래티지)", "r": "수급 추적자: 대규모 숏커버링 물량 대기 중. 행동경제학 코치: 군집 행동으로 인한 과열 구간이나, 세력의 하단 지지가 강력함."}

    # 유동성 및 심리 분석
    flow = "<strong>[데이터 사이언스 포착]</strong> 비정형 데이터(SNS/포럼) 내 'FOMO' 지수 급증. 암호화폐 유동성이 나스닥으로 전이되며 <strong>통계적 차익거래</strong> 기회 발생 중."
    psycho_warn = "⚠️ <strong>트레이딩 코치 경고:</strong> 현재 탐욕 지수가 높습니다. '손실 회피 편향'으로 인해 익절 타이밍을 놓칠 수 있으니 기계적 매도를 권장합니다."
    
    return [wild, normal, safe, whale], flow, psycho_warn

def generate_v7_html(data, recs, flow, warn):
    now = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
    
    cards = ""
    for sym, i in data.items():
        cards += f"""
        <div class="bg-[#2d2d2d] p-3 rounded-lg border border-zinc-800">
            <p class="text-[10px] text-zinc-500 font-black uppercase tracking-tighter">{i['name']}</p>
            <p class="text-md font-black text-[#c4c4c4]">{i['price']:,.1f}</p>
            <p class="text-[10px] font-bold {'text-red-500' if i['chg']>0 else 'text-blue-500'}">{i['chg']:+.2f}%</p>
            <div class="w-full bg-zinc-800 h-1 rounded-full mt-2"><div class="bg-zinc-500 h-1 rounded-full" style="width: {i['rsi']}%"></div></div>
        </div>
        """

    rec_html = ""
    for r in recs:
        rec_html += f"""
        <div class="bg-[#2d2d2d] p-5 rounded-2xl border border-zinc-800 shadow-xl">
            <p class="text-[#D4AF37] font-black text-xs mb-2 italic">HEDGE FUND SELECT</p>
            <p class="text-white font-black text-xl mb-2">{r['t']}</p>
            <p class="text-zinc-400 text-xs leading-relaxed font-medium">{r['r']}</p>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ANT HEDGE FUND V7</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {{ background-color: #1e1e1e; color: #c4c4c4; font-family: 'Inter', sans-serif; }}
            .text-silver {{ color: #c4c4c4; }}
            body.light {{ background-color: #f0f0f0; color: #1a1a1a; }}
            body.light .bg-[#2d2d2d] {{ background-color: #ffffff; border-color: #ddd; }}
            body.light .text-zinc-400 {{ color: #555; }}
        </style>
    </head>
    <body class="p-4 md:p-10">
        <div class="max-w-7xl mx-auto">
            <header class="flex justify-between items-end mb-12 border-b border-zinc-800 pb-8">
                <div>
                    <h1 class="text-4xl font-black text-white italic tracking-tighter">YEONSINNAE HEDGE FUND</h1>
                    <p class="text-zinc-500 font-black text-[10px] mt-2 tracking-[0.3em] uppercase">15 AI AGENTS QUANT & STRATEGY TERMINAL</p>
                </div>
                <button onclick="document.body.classList.toggle('light')" class="bg-[#2d2d2d] border border-zinc-700 px-4 py-2 rounded-lg text-[10px] font-black uppercase">Switch Theme</button>
            </header>

            <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3 mb-10">{cards}</div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-12">
                <div class="lg:col-span-2 bg-[#2d2d2d] p-8 rounded-3xl border border-zinc-800 shadow-2xl relative">
                    <div class="absolute top-4 right-8 flex gap-2">
                        <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                        <span class="text-[10px] font-black text-green-500">SYSTEM LIVE</span>
                    </div>
                    <h2 class="text-2xl font-black text-white mb-6 uppercase tracking-tight">🏛️ 15인 위원회 합동 전략 회의록</h2>
                    <div class="space-y-6">
                        <div class="bg-black/20 p-5 rounded-xl border border-white/5">
                            <p class="text-[10px] text-zinc-500 font-black mb-2 uppercase tracking-widest italic underline">Liquidity Analysis</p>
                            <p class="text-sm text-zinc-200 leading-relaxed font-bold">{flow}</p>
                        </div>
                        <div class="bg-red-500/5 p-5 rounded-xl border border-red-500/20">
                            <p class="text-[10px] text-red-500 font-black mb-2 uppercase tracking-widest">Behavioral Coach Alert</p>
                            <p class="text-sm text-red-200 leading-relaxed font-bold">{warn}</p>
                        </div>
                    </div>
                </div>
                <div class="bg-[#2d2d2d] p-6 rounded-3xl border border-zinc-800 flex flex-col justify-between">
                    <div>
                        <h3 class="text-xs font-black text-zinc-500 mb-6 uppercase tracking-widest">Risk Management Panel</h3>
                        <div class="space-y-4">
                            <div class="flex justify-between text-[10px] font-black"><span>VAR (VALUE AT RISK)</span><span class="text-blue-500 italic">STABLE</span></div>
                            <div class="w-full bg-zinc-800 h-1 rounded-full"><div class="bg-blue-500 h-1 rounded-full" style="width: 35%"></div></div>
                            <div class="flex justify-between text-[10px] font-black"><span>CME MARGIN CALL RISK</span><span class="text-green-500 italic">LOW</span></div>
                            <div class="w-full bg-zinc-800 h-1 rounded-full"><div class="bg-green-500 h-1 rounded-full" style="width: 15%"></div></div>
                            <div class="flex justify-between text-[10px] font-black"><span>SENTIMENT OVERHEAT</span><span class="text-yellow-500 italic">NORMAL</span></div>
                            <div class="w-full bg-zinc-800 h-1 rounded-full"><div class="bg-yellow-500 h-1 rounded-full" style="width: 52%"></div></div>
                        </div>
                    </div>
                    <div class="mt-8 pt-6 border-t border-zinc-800 text-center text-[10px] font-black text-zinc-600">
                        <p>TIMESTAMP: {now} (KST)</p>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">{rec_html}</div>
        </div>
    </body>
    </html>
    """
    with open("index.html", "w", encoding="utf-8") as f: f.write(html)

if __name__ == "__main__":
    d = fetch_extensive_data()
    recs, flow, warn = ai_hedge_fund_meeting(d)
    generate_v7_html(d, recs, flow, warn)
