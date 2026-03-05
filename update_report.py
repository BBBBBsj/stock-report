import yfinance as yf
import datetime
import logging
import requests

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("YeonsinnaeAntFund")

# 1. 확장된 글로벌 시장 데이터 수집
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
    vix_price = 20.0 # 기본값
    
    for category, group in tickers.items():
        for name, symbol in group.items():
            try:
                ticker_obj = yf.Ticker(symbol)
                hist = ticker_obj.history(period="5d")
                
                if len(hist) >= 2:
                    current_price = hist['Close'].iloc[-1]
                    prev_price = hist['Close'].iloc[-2]
                    change_pct = ((current_price - prev_price) / prev_price) * 100
                    
                    if symbol == "^VIX":
                        vix_price = current_price # VIX 저장 (공포지수 계산용)
                        
                    market_data[category][name] = {
                        "price": f"{current_price:,.2f}",
                        "change": f"{change_pct:+.2f}%",
                        "color": "text-red-500" if change_pct > 0 else "text-blue-500"
                    }
                else:
                    market_data[category][name] = {"price": "N/A", "change": "-", "color": "text-stone-500"}
            except Exception as e:
                logger.error(f"{name} 수집 에러: {e}")
                market_data[category][name] = {"price": "Error", "change": "-", "color": "text-stone-500"}
                
    return market_data, vix_price

# 2. 강철의 공포 탐욕 지수 수집기 (CNN + VIX 백업)
def fetch_fear_and_greed(vix_price):
    score = 50
    try:
        url = "https://production.dataviz.cnn.io/index/feargreed/graphdata"
        headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            score = int(data['fear_and_greed']['score'])
        else:
            raise Exception("CNN Blocked")
    except Exception as e:
        logger.warning(f"CNN 접속 실패. VIX 백업 엔진 가동! (VIX: {vix_price})")
        # VIX를 역산하여 공포 탐욕 지수 추정 (VIX 높을수록 공포)
        estimated_score = 100 - (vix_price * 2.5)
        score = int(max(0, min(100, estimated_score))) # 0~100 사이 고정

    if score <= 25: 
        status = "극단적 공포"
        msg = "😱 시장에 피가 낭자합니다! 쫄보 개미들이 짐 싸서 도망가는 중!"
        action = "[적극 매수 찬스] 공포에 사서 환희에 팔아라!"
        picks = "🇺🇸 QQQ, SOXX 분할매수 시작<br>🇰🇷 삼성전자, 현대차 등 낙폭과대 우량주 줍줍"
    elif score <= 45: 
        status = "공포"
        msg = "😨 다들 눈치 보며 쫄아있습니다. 호들갑 떨지 말고 준비하세요."
        action = "[분할 매수 준비] 좋은 주식을 싸게 담을 바구니를 챙기세요."
        picks = "🇺🇸 빅테크 (AAPL, MSFT) 조정 시 매수<br>🇰🇷 배당주, 금융주 위주로 방어력 강화"
    elif score <= 55: 
        status = "중립"
        msg = "😐 평화로운 눈치 보기 장세. 세력들이 방향성을 탐색하고 있습니다."
        action = "[관망 및 현금 확보] 애매할 땐 쉬는 것도 투자입니다."
        picks = "🇺🇸 개별 실적주 단기 트레이딩<br>🇰🇷 K-방산, 조선 등 모멘텀 살아있는 섹터"
    elif score <= 75: 
        status = "탐욕"
        msg = "🤤 '가즈아!' 외치는 중! 파티장 음악 소리가 점점 커집니다."
        action = "[분할 매도 시작] 파티는 즐기되 출구 근처에서 춤추세요."
        picks = "🇺🇸 수익 난 종목 30% 익절 후 현금화<br>🇰🇷 테마주 뇌동매매 절대 금지"
    else: 
        status = "극단적 탐욕"
        msg = "🔥 탐욕의 끝판왕! 너도나도 영끌해서 주식시장으로 뛰어들고 있습니다."
        action = "[전면 경계 태세] 남들이 환희에 찰 때 조용히 빠져나오세요."
        picks = "🇺🇸 LMT, 금(GLD) 등 헷지 자산 비중 확대<br>🇰🇷 현금 비중 70% 이상 유지"
        
    return {"score": score, "status": status, "msg": msg, "action": action, "picks": picks}

# 3. HTML 렌더링 (ECharts 나침반 게이지 포함)
def generate_html(market_data, fg_data):
    now_kst = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')
    
    # 카드 생성기 함수
    def build_cards(data_dict):
        cards = ""
        for name, info in data_dict.items():
            # 색상 처리 (VIX는 오르면 빨간색, 나머지는 오르면 붉은색)
            bg_color = "#2C1E12"
            if name == "VIX (공포지수)":
                txt_color = "text-red-500" if "+" in info['change'] else "text-blue-500"
            else:
                txt_color = info['color']
                
            cards += f"""
            <div class="bg-[{bg_color}] border border-[#3C2A21] p-4 rounded-lg shadow-lg hover:border-[#D4AF37] transition">
                <p class="text-[#A3B18A] text-xs font-bold mb-1">{name}</p>
                <p class="text-xl font-bold text-[#EAE7B1] mb-1">{info['price']}</p>
                <p class="text-xs font-bold {txt_color}">{info['change']}</p>
            </div>
            """
        return cards

    eq_cards = build_cards(market_data["Global Equity"])
    cm_cards = build_cards(market_data["Crypto & Commodities"])

    # HTML 템플릿 (중괄호 충돌을 막기 위해 문자열 분리 방식 사용)
    html_top = """
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
            body { background-color: #120C07; color: #EAE7B1; font-family: 'Noto Sans KR', sans-serif; }
        </style>
    </head>
    <body class="p-4 md:p-8">
        <div class="max-w-6xl mx-auto">
            
            <header class="mb-8 border-b border-[#3C2A21] pb-4 flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
                <div>
                    <h1 class="text-4xl font-black text-[#D4AF37] tracking-tight">🐜 연신내 개미 펀드</h1>
                    <p class="text-[#A3B18A] text-sm mt-2 font-bold tracking-widest">YEONSINNAE ANT FUND • V2.0</p>
                </div>
                <div class="text-left md:text-right bg-[#1A120B] p-2 rounded border border-[#3C2A21]">
                    <p class="text-xs text-stone-500">최종 업데이트 (KST)</p>
                    <p class="font-bold text-md text-white">""" + now_kst + """</p>
                </div>
            </header>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
                <div class="bg-[#1A120B] border border-[#3C2A21] rounded-xl p-4 flex flex-col items-center justify-center shadow-2xl">
                    <h2 class="text-[#A3B18A] font-bold mb-2">시장 심리 나침반</h2>
                    <div id="gauge-chart" style="width: 100%; height: 250px;"></div>
                    <p class="text-2xl font-black text-white mt-[-20px]">""" + fg_data['status'] + """</p>
                </div>

                <div class="bg-[#2C1E12] border border-[#3C2A21] rounded-xl p-6 md:col-span-2 shadow-2xl">
                    <h2 class="text-xl text-[#D4AF37] font-black mb-4 flex items-center">
                        <span class="mr-2 text-2xl">🤖</span> AI 에이전트 긴급 회의록
                    </h2>
                    <div class="space-y-4">
                        <div class="bg-[#1A120B] p-4 rounded-lg border-l-4 border-red-500">
                            <p class="text-xs text-stone-400 mb-1">심리 행동대장 (Psyche)</p>
                            <p class="text-md font-bold text-white">""" + fg_data['msg'] + """</p>
                        </div>
                        <div class="bg-[#1A120B] p-4 rounded-lg border-l-4 border-[#D4AF37]">
                            <p class="text-xs text-stone-400 mb-1">매매 전략가 (Opus)</p>
                            <p class="text-md font-bold text-[#EAE7B1]">""" + fg_data['action'] + """</p>
                        </div>
                        <div class="bg-[#1A120B] p-4 rounded-lg border-l-4 border-green-500">
                            <p class="text-xs text-stone-400 mb-1">섹터 분석가 (Alpha)</p>
                            <p class="text-sm text-stone-300 leading-relaxed">""" + fg_data['picks'] + """</p>
                        </div>
                    </div>
                </div>
            </div>

            <h2 class="text-lg font-bold text-[#A3B18A] mb-4 border-b border-[#3C2A21] pb-2">🌐 글로벌 지수 현황</h2>
            <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3 mb-8">
                """ + eq_cards + """
            </div>

            <h2 class="text-lg font-bold text-[#A3B18A] mb-4 border-b border-[#3C2A21] pb-2">🪙 암호화폐 & 원자재</h2>
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3 mb-10">
                """ + cm_cards + """
            </div>
            
            <footer class="text-center text-stone-600 text-xs py-4 border-t border-[#3C2A21]">
                <p>Designed for Yeonsinnae Ant Fund. Powered by AI Agents.</p>
            </footer>
        </div>

        <script>
            var chartDom = document.getElementById('gauge-chart');
            var myChart = echarts.init(chartDom);
            var option = {
                series: [{
                    type: 'gauge',
                    startAngle: 180,
                    endAngle: 0,
                    min: 0,
                    max: 100,
                    splitNumber: 4,
                    itemStyle: {
                        color: function(params) {
                            var val = """ + str(fg_data['score']) + """;
                            if(val <= 25) return '#EF4444'; // Red
                            if(val <= 45) return '#F97316'; // Orange
                            if(val <= 55) return '#78716C'; // Stone
                            if(val <= 75) return '#4ADE80'; // Green
                            return '#16A34A'; // Dark Green
                        }()
                    },
                    progress: { show: true, width: 20 },
                    pointer: { show: false },
                    axisLine: { lineStyle: { width: 20, color: [[1, '#2C1E12']] } },
                    axisTick: { show: false },
                    splitLine: { show: false },
                    axisLabel: { show: false },
                    detail: {
                        valueAnimation: true,
                        formatter: '{value}',
                        color: '#EAE7B1',
                        fontSize: 45,
                        fontWeight: '900',
                        offsetCenter: [0, '-10%']
                    },
                    data: [{ value: """ + str(fg_data['score']) + """ }]
                }]
            };
            myChart.setOption(option);
            window.addEventListener('resize', function() {
                myChart.resize();
            });
        </script>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_top)

if __name__ == "__main__":
    logger.info("연신내 개미 펀드 V2 수집 시작...")
    m_data, vix = fetch_market_data()
    fg_data = fetch_fear_and_greed(vix)
    generate_html(m_data, fg_data)
    logger.info("리포트 업데이트 완료.")
