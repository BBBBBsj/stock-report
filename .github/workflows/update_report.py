import yfinance as yf
import datetime
import logging
import requests

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("YeonsinnaeAlphaFund")

# 1. 주가 데이터 수집
def fetch_market_data():
    tickers = {"S&P 500": "^GSPC", "NASDAQ": "^IXIC", "Bitcoin": "BTC-USD", "VIX": "^VIX", "WTI Crude": "CL=F"}
    market_data = {}
    
    for name, symbol in tickers.items():
        try:
            ticker_obj = yf.Ticker(symbol)
            hist = ticker_obj.history(period="5d")
            
            if len(hist) >= 2:
                current_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[-2]
                change_pct = ((current_price - prev_price) / prev_price) * 100
                
                market_data[name] = {
                    "price": f"{current_price:,.2f}",
                    "change": f"{change_pct:+.2f}%",
                    "color": "text-red-500" if change_pct > 0 else "text-blue-500"
                }
            else:
                market_data[name] = {"price": "N/A", "change": "N/A", "color": "text-stone-500"}
        except Exception as e:
            logger.error(f"{name} 수집 에러: {e}")
            market_data[name] = {"price": "Error", "change": "-", "color": "text-stone-500"}
            
    return market_data

# 2. CNN 공포 탐욕 지수 수집 (뒷문 API 활용)
def fetch_fear_and_greed():
    try:
        # CNN이 내부적으로 데이터를 그릴 때 사용하는 JSON 데이터 주소 (우회 기법)
        url = "https://production.dataviz.cnn.io/index/feargreed/graphdata"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        score = int(data['fear_and_greed']['score'])
        rating = data['fear_and_greed']['rating'].upper()
        
        # 점수에 따른 색상 지정
        if score < 25: color = "text-red-500" # Extreme Fear
        elif score < 45: color = "text-orange-400" # Fear
        elif score <= 55: color = "text-stone-400" # Neutral
        elif score <= 75: color = "text-green-400" # Greed
        else: color = "text-green-600" # Extreme Greed
            
        return {"score": score, "rating": rating, "color": color}
    except Exception as e:
        logger.error(f"공포 탐욕 지수 수집 에러: {e}")
        return {"score": "N/A", "rating": "ERROR", "color": "text-stone-500"}

# 3. HTML 렌더링 (나중에 프론트엔드 수정하기 쉽게 템플릿화)
def generate_html(market_data, fg_data):
    now_kst = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')
    
    # 지수 카드 HTML 생성
    cards_html = ""
    for name, info in market_data.items():
        cards_html += f"""
        <div class="bg-[#2C1E12] border border-[#3C2A21] p-5 rounded-xl shadow-lg">
            <p class="text-[#A3B18A] text-xs font-bold mb-2">{name}</p>
            <p class="text-2xl font-bold text-[#EAE7B1] mb-1">{info['price']}</p>
            <p class="text-sm font-bold {info['color']}">{info['change']}</p>
        </div>
        """

    # 전체 HTML 조립
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Yeonsinnae Alpha Fund</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {{ background-color: #120C07; color: #EAE7B1; font-family: sans-serif; }}
        </style>
    </head>
    <body class="p-4 md:p-8">
        <div class="max-w-5xl mx-auto">
            
            <header class="mb-8 border-b border-[#3C2A21] pb-4 flex justify-between items-end">
                <div>
                    <h1 class="text-3xl font-bold text-[#D4AF37]">Yeonsinnae Alpha Fund</h1>
                    <p class="text-[#A3B18A] text-sm mt-1">Institutional Market Dashboard</p>
                </div>
                <div class="text-right">
                    <p class="text-xs text-stone-500">Last Update (KST)</p>
                    <p class="font-bold text-lg">{now_kst}</p>
                </div>
            </header>

            <div class="bg-[#1A120B] border border-[#3C2A21] p-6 rounded-xl mb-8 flex justify-between items-center">
                <div>
                    <p class="text-sm text-stone-400 mb-1">Fear & Greed Index</p>
                    <p class="text-4xl font-bold {fg_data['color']}">{fg_data['score']}</p>
                </div>
                <div class="text-right">
                    <p class="text-xl font-bold {fg_data['color']}">{fg_data['rating']}</p>
                    <p class="text-xs text-stone-500 mt-1">Powered by CNN Data</p>
                </div>
            </div>

            <div class="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
                {cards_html}
            </div>

            <div class="bg-[#2C1E12] border border-[#3C2A21] p-6 rounded-xl">
                <h2 class="text-xl text-[#D4AF37] font-bold mb-4">현재 대응 전략</h2>
                <p class="text-stone-300 leading-relaxed">
                    현금 비중 100% 유지. 시장의 심리가 극단적 공포({fg_data['rating']}) 구간에 머물고 있습니다.<br>
                    추가적인 VIX 급등 여부를 모니터링하며, 반등 시그널 확인 전까지 신규 진입을 보류합니다.
                </p>
            </div>
            
        </div>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    logger.info("데이터 수집 시작...")
    m_data = fetch_market_data()
    fg_data = fetch_fear_and_greed()
    generate_html(m_data, fg_data)
    logger.info("리포트 업데이트 완료.")
