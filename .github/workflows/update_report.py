import yfinance as yf
import pandas as pd
import datetime
import logging
import requests

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("YeonsinnaeAntFund")

# 1. 확장된 글로벌 시장 데이터 수집 & RSI 계산
def fetch_market_data():
    tickers = {
        "Global Equity": {
            "KOSPI (한국)": "^KS11",
            "Nikkei (일본)": "^N225",
            "Shanghai (중국)": "000001.SS",
            "STOXX50 (유럽)": "^STOXX50E",
            "S&P 500 (미국)": "^GSPC",
            "NASDAQ (미국)": "^IXIC",
            "VIX (공포지수)": "^VIX"
        },
        "Crypto & Commodities": {
            "Bitcoin": "BTC-USD",
            "Ethereum": "ETH-USD",
            "Gold (금)": "GC=F",
            "Silver (은)": "SI=F",
            "WTI Crude (원유)": "CL=F",
            "Copper (구리)": "HG=F"
        }
    }
    
    market_data = {"Global Equity": {}, "Crypto & Commodities": {}}
    vix_price = 20.0 
    wti_price = 70.0
    ndx_change = 0.0

    for category, group in tickers.items():
        for name, symbol in group.items():
            try:
                # 20일치 데이터를 가져와서 RSI 계산
                ticker_obj = yf.Ticker(symbol)
                hist = ticker_obj.history(period="20d")
                
                if len(hist) >= 15:
                    current_price = hist['Close'].iloc[-1]
                    prev_price = hist['Close'].iloc[-2]
                    change_pct = ((current_price - prev_price) / prev_price) * 100
                    
                    # 간단한 RSI 계산 로직
                    delta = hist['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean().iloc[-1]
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean().iloc[-1]
                    rs = gain / loss if loss != 0 else 100
                    rsi = 100 - (100 / (1 + rs)) if loss != 0 else 100
                    
                    # 변수 저장 (시황 분석용)
                    if symbol == "^VIX": vix_price = current_price
                    if symbol == "CL=F": wti_price = current_price
                    if symbol == "^IXIC": ndx_change = change_pct

                    # 위험도(변동성)에 따른 색상 진하기(Intensity) 설정
                    abs_change = abs(change_pct)
                    intensity_class = ""
                    if abs_change >= 2.0: intensity_class = "font-black tracking-tighter" # 위험도 높음 (아주 굵게)
                    elif abs_change >= 1.0: intensity_class = "font-bold" # 보통
                    else: intensity_class = "font-normal opacity-80" # 위험도 낮음 (약간 흐리게)

                    market_data[category][name] = {
                        "price": f"{current_price:,.2f}",
                        "change": f"{change_pct:+.2f}%",
                        "rsi": f"{rsi:.1f}",
                        "is_up": change_pct > 0,
                        "intensity": intensity_class
                    }
                else:
                    market_data[category][name] = {"price": "N/A", "change": "-", "rsi": "-", "is_up": True, "intensity": ""}
            except Exception as e:
                logger.error(f"{name} 수집 에러: {e}")
                market_data[category][name] = {"price": "Error", "change": "-", "rsi": "-", "is_up": True, "intensity": ""}
                
    return market_data, vix_price, wti_price, ndx_change

# 2. 공포 탐욕 지수
def fetch_fear_and_greed(vix_price):
    score = int(max(0, min(100, 100 - (vix_price * 2.5)))) # VIX 기반 계산
    status = "중립"
    if score <= 25: status = "극단적 공포"
    elif score <= 45: status = "공포"
    elif score <= 75: status = "탐욕"
    elif score > 75: status = "극단적 탐욕"
    return score, status

# 3. AI 에이전트 시황 브리핑 생성기
def generate_agent_briefing(vix, wti, ndx, score):
    market_brief = "<strong>[국내]</strong> 외인 수급 부재로 인한 박스권 횡보. <strong>[미국]</strong> M7 위주의 쏠림 현상 지속. <strong>[글로벌]</strong> 신흥국 자금 이탈 모니터링 필요."
    if ndx < -1.5:
        market_brief = "<strong>[미국]</strong> 기술주 전반에 차익실현 매물 출회 및 밸류에이션 부담 가중. <strong>[국내]</strong> 나스닥 하락 여파로 반도체 섹터 투심 악화 우려."
    
    geo_risk = "현재 두드러지는 글로벌 지정학적 타격은 제한적입니다."
    if wti > 80 or vix > 20:
        geo_risk = "⚠️ <strong>[지정학 리스크]</strong> 이란-이스라엘 분쟁 격화 등 중동 긴장감 고조. 원유 공급망 타격 우려로 인플레이션 헷지 자산(금, 달러) 주목."

    alerts = []
    if vix > 22: alerts.append("🚨 <strong>CME 증거금 인상 가능성:</strong> 변동성 확대로 파생상품 증거금 인상 검토 루머가 있습니다. 레버리지 축소 권장!")
    if ndx < -2.0: alerts.append("🚨 <strong>기술주 투매 경계:</strong> AI/반도체 섹터 전반에 매도세가 거셉니다. 섣부른 물타기 금지!")
    if score <= 25: alerts.append("💡 <strong>개미들 투매 중:</strong> 시장에 피가 낭자합니다. 우량주 분할 매수용 현금 탄창을 장전하십시오.")
    elif score >= 75: alerts.append("💡 <strong>비이성적 과열:</strong> 모두가 환희에 차 있습니다. 수익 난 종목은 분할 익절하여 현금을 확보하십시오.")
    
    if not alerts: alerts.append("✅ 현재 시장에 특별한 시스템적 이상 징후는 발견되지 않았습니다. 개별 종목 장세에 집중하세요.")
    
    return market_brief, geo_risk, "<br>".join(alerts)

# 4. HTML 렌더링
def generate_html(market_data, score, status, brief, geo, alerts):
    now_kst = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')
    
    def build_cards(data_dict):
        cards = ""
        for name, info in data_dict.items():
            if name == "VIX (공포지수)": color_class = "text-up" if info['is_up'] else "text-down"
            else: color_class = "text-up" if info['is_up'] else "text-down"
                
            rsi_val = float(info['rsi']) if info['rsi'] != '-' else 50
            rsi_color = "text-red-500" if rsi_val >= 70 else ("text-blue-500" if rsi_val <= 30 else "text-muted")
            
            cards += f"""
            <div class="card p-4 rounded-xl shadow-lg transition-all hover:scale-105 border">
                <div class="flex justify-between items-start mb-2">
                    <p class="text-muted text-xs font-bold">{name}</p>
                    <span class="text-[10px] px-1.5 py-0.5 rounded bg-black/10 dark:bg-white/10 {rsi_color}">RSI {info['rsi']}</span>
                </div>
                <p class="text-xl font-bold text-main mb-1 {info['intensity']}">{info['price']}</p>
                <p class="text-sm {color_class} {info['intensity']}">{info['change']}</p>
            </div>
            """
        return cards

    eq_cards = build_cards(market_data["Global Equity"])
    cm_cards = build_cards(market_data["Crypto & Commodities"])

    html_content = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>연신내 개미 펀드 대시보드</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700;900&display=swap');
            :root { --bg-body: #120C07; --bg-card: #1A120B; --bg-panel: #241910; --text-main: #EAE7B1; --text-muted: #A3B18A; --border-color: #3C2A21; --accent: #D4AF37; --up-color: #EF4444; --down-color: #3B82F6; }
            [data-theme="light"] { --bg-body: #F3F4F6; --bg-card: #FFFFFF; --bg-panel: #E5E7EB; --text-main: #1F2937; --text-muted: #6B7280; --border-color: #D1D5DB; --accent: #B45309; --up-color: #DC2626; --down-color: #2563EB; }
            body { background-color: var(--bg-body); color: var(--text-main); font-family: 'Noto Sans KR', sans-serif; transition: all 0.3s; }
            .card { background-color: var(--bg-card); border-color: var(--border-color); }
            .panel { background-color: var(--bg-panel); border-color: var(--border-color); }
            .text-main { color: var(--text-main); }
            .text-muted { color: var(--text-muted); }
            .text-accent { color: var(--accent); }
            .text-up { color: var(--up-color); }
            .text-down { color: var(--down-color); }
            .border { border-color: var(--border-color); }
        </style>
    </head>
    <body class="p-4 md:p-8">
        <div class="max-w-7xl mx-auto">
            <header class="mb-8 border-b pb-4 flex flex-col md:flex-row justify-between items-start md:items-end gap-4 border">
                <div>
                    <h1 class="text-4xl font-black text-accent tracking-tight">🐜 연신내 개미 펀드</h1>
                    <p class="text-muted text-sm mt-2 font-bold tracking-widest">GLOBAL MACRO DASHBOARD</p>
                </div>
                <div class="flex items-center gap-4">
                    <button onclick="toggleTheme()" class="card px-4 py-2 rounded-full font-bold shadow-md border text-sm flex items-center gap-2">
                        <span id="theme-icon">🌙 블랙 모드</span>
                    </button>
                    <div class="text-right card p-2 rounded border">
                        <p class="text-xs text-muted">업데이트 (KST)</p>
                        <p class="font-bold text-md text-main">""" + now_kst + """</p>
                    </div>
                </div>
            </header>

            <div class="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-10">
                <div class="card rounded-2xl p-4 flex flex-col items-center justify-center shadow-xl border">
                    <h2 class="text-muted font-bold mb-2">시장 심리 나침반</h2>
                    <div id="gauge-chart" style="width: 100%; height: 220px;"></div>
                    <p class="text-2xl font-black text-main mt-[-20px]">""" + status + """</p>
                </div>
                <div class="panel rounded-2xl p-6 lg:col-span-2 shadow-xl border">
                    <h2 class="text-xl text-accent font-black mb-4 flex items-center">📊 AI 퀀트 시황 요약</h2>
                    <div class="space-y-4 text-sm leading-relaxed">
                        <div class="border-l-4 border-accent pl-3">
                            <h3 class="font-bold text-muted mb-1">글로벌 자금 흐름 (Liquidity)</h3>
                            <p class="text-main">""" + brief + """</p>
                        </div>
                        <div class="border-l-4 border-red-500 pl-3">
                            <h3 class="font-bold text-muted mb-1">지정학적 리스크 (Macro)</h3>
                            <p class="text-main">""" + geo + """</p>
                        </div>
                    </div>
                </div>
                <div class="card rounded-2xl p-6 shadow-xl border border-red-900/50">
                    <h2 class="text-xl text-red-500 font-black mb-4 flex items-center">🚨 포트폴리오 경고등</h2>
                    <div class="text-sm text-main space-y-3 leading-relaxed">""" + alerts + """</div>
                </div>
            </div>

            <h2 class="text-lg font-bold text-muted mb-4 border-b pb-2 border">🌐 글로벌 핵심 지수 (RSI 탑재)</h2>
            <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4 mb-8">""" + eq_cards + """</div>

            <h2 class="text-lg font-bold text-muted mb-4 border-b pb-2 border">🪙 대체 자산 (크립토 & 원자재)</h2>
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-10">""" + cm_cards + """</div>
        </div>

        <script>
            function toggleTheme() {
                const body = document.body;
                const icon = document.getElementById('theme-icon');
                if (body.getAttribute('data-theme') === 'light') {
                    body.removeAttribute('data-theme');
                    localStorage.setItem('theme', 'dark');
                    icon.innerText = '🌙 블랙 모드';
                } else {
                    body.setAttribute('data-theme', 'light');
                    localStorage.setItem('theme', 'light');
                    icon.innerText = '☀️ 실버 모드';
                }
            }
            if(localStorage.getItem('theme') === 'light') {
                document.body.setAttribute('data-theme', 'light');
                document.getElementById('theme-icon').innerText = '☀️ 실버 모드';
            }

            var chartDom = document.getElementById('gauge-chart');
            var myChart = echarts.init(chartDom);
            var option = {
                series: [{
                    type: 'gauge', startAngle: 180, endAngle: 0, min: 0, max: 100, splitNumber: 4,
                    itemStyle: {
                        color: function(params) {
                            var val = """ + str(score) + """;
                            if(val <= 25) return '#EF4444'; if(val <= 45) return '#F97316';
                            if(val <= 55) return '#78716C'; if(val <= 75) return '#4ADE80';
                            return '#16A34A';
                        }()
                    },
                    progress: { show: true, width: 20 }, pointer: { show: false },
                    axisLine: { lineStyle: { width: 20, color: [[1, 'rgba(128,128,128,0.2)']] } },
                    axisTick: { show: false }, splitLine: { show: false }, axisLabel: { show: false },
                    detail: { valueAnimation: true, formatter: '{value}', color: 'inherit', fontSize: 40, fontWeight: '900', offsetCenter: [0, '-10%'] },
                    data: [{ value: """ + str(score) + """ }]
                }]
            };
            myChart.setOption(option);
            window.addEventListener('resize', function() { myChart.resize(); });
        </script>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    logger.info("V3 엔진 가동...")
    m_data, vix, wti, ndx = fetch_market_data()
    score, status = fetch_fear_and_greed(vix)
    brief, geo, alerts = generate_agent_briefing(vix, wti, ndx, score)
    generate_html(m_data, score, status, brief, geo, alerts)
    logger.info("업데이트 완료.")
