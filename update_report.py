import yfinance as yf
import pandas as pd
import datetime
import logging
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("YeonsinnaeAntFund")

def fetch_market_data():
    tickers = {
        "Global Equity": {
            "KOSPI (한국)": "^KS11", "Nikkei (일본)": "^N225", "Shanghai (중국)": "000001.SS",
            "STOXX50 (유럽)": "^STOXX50E", "S&P 500 (미국)": "^GSPC", "NASDAQ (미국)": "^IXIC", "VIX (공포지수)": "^VIX"
        },
        "Crypto & Commodities": {
            "Bitcoin": "BTC-USD", "Ethereum": "ETH-USD", "Gold (금)": "GC=F", "Silver (은)": "SI=F", "WTI Crude (원유)": "CL=F", "Copper (구리)": "HG=F"
        }
    }
    market_data = {"Global Equity": {}, "Crypto & Commodities": {}}
    vix_p, wti_p, ndx_c = 20.0, 70.0, 0.0

    for cat, group in tickers.items():
        for name, sym in group.items():
            try:
                t = yf.Ticker(sym)
                h = t.history(period="20d")
                if len(h) >= 15:
                    curr, prev = h['Close'].iloc[-1], h['Close'].iloc[-2]
                    chg = ((curr - prev) / prev) * 100
                    d = h['Close'].diff()
                    g = (d.where(d > 0, 0)).rolling(14).mean().iloc[-1]
                    l = (-d.where(d < 0, 0)).rolling(14).mean().iloc[-1]
                    rsi = 100 - (100 / (1 + (g/l))) if l != 0 else 100
                    if sym == "^VIX": vix_p = curr
                    if sym == "CL=F": wti_p = curr
                    if sym == "^IXIC": ndx_c = chg
                    market_data[cat][name] = {"price": f"{curr:,.2f}", "change": f"{chg:+.2f}%", "rsi": f"{rsi:.1f}", "is_up": chg > 0, "val": abs(chg)}
            except: market_data[cat][name] = {"price": "Error", "change": "-", "rsi": "-", "is_up": True, "val": 0}
    return market_data, vix_p, wti_p, ndx_c

def generate_html(data, vix, wti, ndx):
    score = int(max(0, min(100, 100 - (vix * 2.5))))
    status = "중립"
    if score <= 25: status = "극단적 공포"
    elif score <= 45: status = "공포"
    elif score <= 75: status = "탐욕"
    else: status = "극단적 탐욕"

    brief = "국내 박스권 횡보 중이며 미국 기술주 중심의 쏠림이 강합니다."
    geo = "이란-이스라엘 분쟁 등 중동 리스크가 유가에 하방 압력을 줄 수 있습니다."
    if wti > 80: geo = "⚠️ 중동 지정학 리스크 고조! 원유 및 안전자산 비중을 늘리세요."
    
    alerts = "✅ 시장 특이사항 없음"
    if ndx < -1.5: alerts = "🚨 기술주 급락 주의! CME 증거금 인상 검토 중 루머가 있습니다."

    now = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')
    
    def cards(d):
        res = ""
        for n, i in d.items():
            c = "text-red-500" if i['is_up'] else "text-blue-500"
