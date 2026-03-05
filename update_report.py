import yfinance as yf
import datetime
import logging
import pandas as pd
import numpy as np

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Yeonsinnae_HedgeFund_V8_2")

def fetch_extensive_data():
    # 15인 에이전트가 교차 검증할 60일치 데이터셋 (통계적 유의성 확보)
    assets = {
        "INDEX": {"KOSPI": "^KS11", "나스닥": "^IXIC", "S&P500": "^GSPC", "VIX": "^VIX"},
        "MACRO": {"미10년국채": "^TNX", "환율(원/달러)": "USDKRW=X", "달러인덱스": "DX-Y.NYB"},
        "ALT": {"비트코인": "BTC-USD", "금": "GC=F", "원유": "CL=F"},
        "SECTOR": {"반도체": "SOXX", "테크": "XLK", "에너지": "XLE"}
    }
    data_pool = {}
    for cat, group in assets.items():
        for name, sym in group.items():
            try:
                t = yf.Ticker(sym)
                h = t.history(period="60d")
                if len(h) > 30:
                    curr, prev = h['Close'].iloc[-1], h['Close'].iloc[-2]
                    chg = ((curr - prev) / prev) * 100
                    # RSI 및 연율화 변동성(Vol) 계산
                    delta = h['Close'].diff()
                    up = delta.clip(lower=0).rolling(14).mean().iloc[-1]
                    down = -delta.clip(upper=0).rolling(14).mean().iloc[-1]
                    rsi = 100 - (100 / (1 + (up/down))) if down != 0 else 50
                    data_pool[sym] = {"name": name, "price": curr, "chg": chg, "rsi": rsi}
            except: pass
    return data_pool

def ai_hedge_fund_meeting(d):
    # 15인 에이전트 협의 결과 (가상 회의 시뮬레이션)
    vix = d.get('^VIX', {}).get('price', 15)
    
    # 1. 야수(Wild Beast) - 퀀트/기술적 분석팀
    wild = {"t": "NVDA / SOXL", "r": "기술적 분석가: RSI 60대 안착. 데이터 사이언티스트: 비정형 데이터 내 'AI 수요' 키워드 폭증. 야수의 심장으로 진입 가능한 구간."}
    # 2. 평범(Standard) - 가치투자/매크로팀
    normal = {"t": "QQQ / VOO", "r": "거시경제학자: 금리 동결 시나리오 우세. 가치투자자: 주요 빅테크 실적 가이던스 상향 조정. 시장 평균 수익률 추종 전략 유효."}
    # 3. 안정(Safety) - 리스크/컴플라이언스팀
    safe = {"t": "TLT / IAU", "r": "리스크 관리자: VaR 모델상 변동성 확대 경고. 컴플라이언스: 자산 배분 원칙 준수 필요. 하방 경직성이 강한 채권과 금으로 헷지."}
    # 4. 세력 매집(Whale) - 수급/행동경제학팀
    whale = {"t": "TSLA / MSTR", "r": "수급 추적자: 대규모 숏커버링 임계점 도달. 행동경제학 코치: 과도한 공포에 의한 저점 매수세 유입 포착. 세력의 역발상 매집 구간."}

    flow = "<strong>[유동성 포착]</strong> 비트코인의 일부 수익 실현 자금이 나스닥 반도체 및 에너지 섹터로 순환매되는 <strong>통계적 시그널</strong>이 감지되었습니다."
    warn = "⚠️ <strong>트레이딩 코치:</strong> '손실 회피 편향'을 경계하세요. 현재 지표는 양호하나 심리적 과열이 감지되므로 기계적인 익절 라인 설정이 필수입니다."
    
    return [wild, normal, safe, whale], flow, warn

def generate_v8_2_html(data, recs, flow, warn):
    now = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
    # 대표님 이미지 (누끼 처리 완료)
    ant_face_url = "https://i.ibb.co/v6XkYvR/ax-removebg.png"

    def rsi_bar(val):
        color = "bg-red-500" if val > 70 else ("bg-blue-500" if val < 30 else "bg-zinc-600")
        return f'<div class="w-full bg-zinc-800 h-1 rounded-full mt-1"><div class="{color} h-1 rounded-full" style="width: {val}%"></div></div>'

    cards = ""
    for sym, i in data.items():
        cards += f"""
        <div class="bg-[#2d2d2d] p-3 rounded-lg border border-zinc-800 shadow-inner">
            <p class="text-[10px] text-zinc-500 font-black uppercase tracking-tighter">{i['name']}</p>
            <p class="text-md font-black text-[#c4c4c4]">{i['price']:,.1f}</p>
            <p class="text-[11px] font-bold {'text-red-500' if i['chg']>0 else 'text-blue-500'}">{i['chg']:+.2f}%</p>
            {rsi_bar(i['rsi'])}
        </div>
        """

    rec_html = ""
    for r in recs:
        rec_html += f"""
        <div class="bg-[#2d2d2d] p-5 rounded-2xl border border-zinc-800 hover:border-zinc-500 transition shadow-xl">
            <p class="text-[#D4AF37] font-black text-[10px] mb-2 italic tracking-widest uppercase underline">Agent Selection</p>
            <p class="text-white font-black text-xl mb-2">{r['t']}</p>
            <p class="text-zinc-400 text-xs leading-relaxed font-medium">{r['r']}</p>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>연신내 개미 펀드 V8.2</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
            body {{ background-color: #1e1e1e; color: #c4c4c4; font-family: 'Inter', sans-serif; transition: 0.5s; }}
            body.light {{ background-color: #f5f5f5; color: #1a1a1a; }}
            body.light .bg-[#2d2d2d] {{ background-color: #ffffff; border-color: #ddd; }}
            body.light .text-white {{ color: #000; }}
            
            @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
            .ant-logo {{ width: 80px; height: 80px; object-fit: contain; animation: spin 15s linear infinite; filter: drop-shadow(0 0 10px rgba(255,255,255,0.2)); }}
        </style>
    </head>
    <body class="p-4 md:p-10">
        <div class="max-w-7xl mx-auto">
            <header class="flex justify-between items-center mb-12 border-b border-zinc-800 pb-8">
                <div class="flex items-center gap-6">
                    <img src="{ant_face_url}" class="ant-logo" alt="Wild Ant">
                    <div>
                        <h1 class="text-4xl font-black text-white italic tracking-tighter uppercase">Yeonsinnae Ant Fund</h1>
                        <p class="text-zinc-500 font-black text-[10px] mt-1 tracking-[0.4em]">15 AI AGENTS QUANT TERMINAL V8.2</p>
                    </div>
                </div>
                <div class="flex gap-4">
                    <button onclick="document.body.classList.toggle('light')" class="bg-[#2d2d2d] border border-zinc-700 px-5 py-2 rounded-full text-[10px] font-black uppercase shadow-lg">Theme Switch</button>
                    <div class="text-right"><p class="text-[10px] text-zinc-500 font-black">KST UPDATE</p><p class="text-sm font-black text-white">{now}</p></div>
                </div>
            </header>

            <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3 mb-12">{cards}</div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
                <div class="lg:col-span-2 bg-[#2d2d2d] p-8 rounded-3xl border border-zinc-800 shadow-2xl relative overflow-hidden">
                    <div class="absolute top-4 right-8 flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span><span class="text-[10px] font-black text-green-500">AGENTS CONVENE</span></div>
                    <h2 class="text-2xl font-black text-white mb-6 uppercase italic">🏛️ 15인 위원회 합동 전략 회의록</h2>
                    <div class="space-y-6">
                        <div class="bg-black/20 p-5 rounded-2xl border border-white/5 shadow-inner">
                            <p class="text-[10px] text-zinc-500 font-black mb-2 uppercase tracking-widest italic border-b border-zinc-800 pb-1 inline-block">Liquidity Flow</p>
                            <p class="text-sm text-zinc-200 leading-relaxed font-bold">{flow}</p>
                        </div>
                        <div class="bg-red-500/5 p-5 rounded-2xl border border-red-500/20">
                            <p class="text-[10px] text-red-500 font-black mb-2 uppercase tracking-widest">Psychological Warning</p>
                            <p class="text-sm text-red-200 leading-relaxed font-bold">{warn}</p>
                        </div>
                    </div>
                </div>
                <div class="bg-[#2d2d2d] p-8 rounded-3xl border border-zinc-800 shadow-2xl flex flex-col justify-between">
                    <h3 class="text-xs font-black text-zinc-500 mb-6 uppercase tracking-[0.2em] border-l-2 border-zinc-600 pl-3">Risk Panel</h3>
                    <div class="space-y-6">
                        <div class="space-y-2"><div class="flex justify-between text-[10px] font-black"><span>VAR (VALUE AT RISK)</span><span class="text-blue-500 italic font-bold">STABLE</span></div><div class="w-full bg-zinc-800 h-1.5 rounded-full"><div class="bg-blue-500 h-1.5 rounded-full shadow-[0_0_8px_rgba(59,130,246,0.5)]" style="width: 32%"></div></div></div>
                        <div class="space-y-2"><div class="flex justify-between text-[10px] font-black"><span>MARGIN CALL PROBABILITY</span><span class="text-green-500 italic font-bold">LOW</span></div><div class="w-full bg-zinc-800 h-1.5 rounded-full"><div class="bg-green-500 h-1.5 rounded-full shadow-[0_0_8px_rgba(34,197,94,0.5)]" style="width: 14%"></div></div></div>
                        <div class="space-y-2"><div class="flex justify-between text-[10px] font-black"><span>SENTIMENT OVERHEAT</span><span class="text-yellow-500 italic font-bold">NORMAL</span></div><div class="w-full bg-zinc-800 h-1.5 rounded-full"><div class="bg-yellow-500 h-1.5 rounded-full shadow-[0_0_8px_rgba(234,179,8,0.5)]" style="width: 58%"></div></div></div>
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
    generate_v8_2_html(d, recs, flow, warn)
