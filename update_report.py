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
    geo = "지정학 리스크가 유가에 영향을 줄 수 있으니 주의하세요."
    if wti > 80: geo = "⚠️ 중동 지정학 리스크 고조! 원유 및 안전자산 비중을 늘리세요."
    
    alerts = "✅ 시장 특이사항 없음"
    if ndx < -1.5: alerts = "🚨 기술주 급락 주의! CME 증거금 인상 검토 중 루머가 있습니다."

    now = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')
    
    def cards(d):
        res = ""
        for n, i in d.items():
            c = "text-red-500 font-bold" if i['is_up'] else "text-blue-500 font-bold"
            bold = "font-black" if i['val'] > 1.5 else ""
            res += f'<div class="card p-4 rounded-xl border border-zinc-800 transition-all hover:scale-105"><p class="text-muted text-xs font-bold">{n}</p><p class="text-xl font-bold {bold}">{i["price"]}</p><p class="{c} text-xs {bold}">{i["change"]} (RSI {i["rsi"]})</p></div>'
        return res

    html = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>연신내 개미 펀드</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>
        <style>
            :root {{ --bg: #120C07; --card: #1A120B; --text: #EAE7B1; --muted: #A3B18A; --accent: #D4AF37; --border: #3C2A21; }}
            body.light {{ --bg: #F3F4F6; --card: #FFFFFF; --text: #1F2937; --muted: #6B7280; --accent: #B45309; --border: #D1D5DB; }}
            body {{ background: var(--bg); color: var(--text); transition: 0.3s; font-family: sans-serif; }}
            .card {{ background: var(--card); border-color: var(--border); }}
            .text-muted {{ color: var(--muted); }} .text-accent {{ color: var(--accent); }}
        </style>
    </head>
    <body>
        <div class="max-w-6xl mx-auto p-4 md:p-8">
            <header class="flex flex-col md:flex-row justify-between mb-8 border-b border-zinc-800 pb-4 gap-4">
                <div><h1 class="text-4xl font-black text-accent">🐜 연신내 개미 펀드</h1><p class="text-muted font-bold mt-1">GLOBAL MACRO REPORT V4.0</p></div>
                <div class="flex gap-4 items-center">
                    <button onclick="toggleTheme()" class="card px-4 py-2 rounded-full border font-bold shadow-lg">🌗 테마 전환</button>
                    <div class="card p-2 border text-right text-xs"><p class="text-muted">Last Update (KST)</p><p class="font-bold">{now}</p></div>
                </div>
            </header>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div class="card p-4 rounded-xl border flex flex-col items-center shadow-2xl">
                    <p class="text-muted font-bold mb-2">공포 탐욕 나침반</p>
                    <div id="g" style="width:100%;height:180px"></div>
                    <p class="text-2xl font-black">{status}</p>
                </div>
                <div class="card p-6 rounded-xl border md:col-span-2 shadow-2xl">
                    <h2 class="text-xl font-bold text-accent mb-4 border-b border-zinc-800 pb-2">📊 AI 에이전트 긴급 회의록</h2>
                    <p class="mb-3 text-sm"><strong>📈 유동성 분석:</strong> {brief}</p>
                    <p class="mb-3 text-sm"><strong>🌍 지정학 리스크:</strong> {geo}</p>
                    <p class="text-red-500 font-bold text-sm bg-red-500/10 p-2 rounded">{alerts}</p>
                </div>
            </div>

            <h2 class="text-muted font-bold mb-4 border-b border-zinc-800 pb-1 uppercase text-xs tracking-widest">🌐 글로벌 증시 지표</h2>
            <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3 mb-10">{cards(data['Global Equity'])}</div>

            <h2 class="text-muted font-bold mb-4 border-b border-zinc-800 pb-1 uppercase text-xs tracking-widest">🪙 암호화폐 & 원자재</h2>
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">{cards(data['Crypto & Commodities'])}</div>
        </div>

        <script>
            function toggleTheme() {{
                document.body.classList.toggle('light');
                const isLight = document.body.classList.contains('light');
                localStorage.setItem('theme', isLight ? 'light' : 'dark');
            }}
            
            // 로드 시 테마 복구 (기본 다크)
            if (localStorage.getItem('theme') === 'light') {{
                document.body.classList.add('light');
            }}

            var m = echarts.init(document.getElementById('g'));
            var scoreVal = {score};
            m.setOption({{
                series: [{{
                    type: 'gauge', startAngle: 180, endAngle: 0, min: 0, max: 100,
                    itemStyle: {{ color: scoreVal < 40 ? '#EF4444' : '#16A34A' }},
                    progress: {{ show: true, width: 12 }}, pointer: {{ show: false }},
                    axisLine: {{ lineStyle: {{ width: 12, color: [[1, 'rgba(128,128,128,0.1)']] }} }},
                    axisTick: {{ show: false }}, splitLine: {{ show: false }}, axisLabel: {{ show: false }},
                    detail: {{ valueAnimation: true, formatter: '{{value}}', color: 'inherit', fontSize: 32, fontWeight: '900', offsetCenter: [0, '-10%'] }},
                    data: [{{ value: scoreVal }}]
                }}]
            }});
            window.addEventListener('resize', () => m.resize());
        </script>
    </body>
    </html>
    """
    with open("index.html", "w", encoding="utf-8") as f: f.write(html)

if __name__ == "__main__":
    d, v, w, n = fetch_market_data()
    generate_html(d, v, w, n)
