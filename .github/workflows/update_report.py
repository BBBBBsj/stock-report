import yfinance as yf
import datetime
import logging

# ---------------------------------------------------------
# 1. Pro Mode: 로깅 및 환경 설정
# ---------------------------------------------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("YeonsinnaeAlphaFund")

# ---------------------------------------------------------
# 2. Pro Mode: 핵심 매크로 데이터 수집 엔진
# ---------------------------------------------------------
def fetch_market_data():
    """yfinance를 이용해 월가 핵심 지표를 실시간(지연) 수집합니다."""
    # S&P 500, 나스닥, 비트코인, VIX(변동성), WTI 원유
    tickers = {
        "S&P 500": "^GSPC",
        "NASDAQ": "^IXIC",
        "Bitcoin": "BTC-USD",
        "VIX (공포지수)": "^VIX",
        "WTI Crude (원유)": "CL=F"
    }
    
    market_data = {}
    
    for name, symbol in tickers.items():
        try:
            logger.info(f"데이터 수집 중: {name} ({symbol})")
            ticker_obj = yf.Ticker(symbol)
            hist = ticker_obj.history(period="5d") # 안정성을 위해 5일치 확보
            
            if len(hist) >= 2:
                current_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[-2]
                change_pct = ((current_price - prev_price) / prev_price) * 100
                
                # 소수점 및 기호 포맷팅
                price_fmt = f"{current_price:,.2f}"
                change_fmt = f"{change_pct:+.2f}%"
                
                # 색상 결정 (VIX는 오르면 빨간색/위험)
                if name == "VIX (공포지수)":
                    color_class = "text-red-500" if change_pct > 0 else "text-blue-500"
                else:
                    color_class = "text-red-500" if change_pct > 0 else "text-blue-500"

                market_data[name] = {"price": price_fmt, "change": change_fmt, "color": color_class}
            else:
                market_data[name] = {"price": "N/A", "change": "N/A", "color": "text-stone-500"}
                
        except Exception as e:
            logger.error(f"{name} 데이터 수집 실패: {e}")
            market_data[name] = {"price": "Error", "change": "-", "color": "text-stone-500"}
            
    return market_data

# ---------------------------------------------------------
# 3. Pro Mode: 우디 & 엘리트 HTML 대시보드 렌더링
# ---------------------------------------------------------
def generate_elite_dashboard(data):
    now_utc = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 딕셔너리 데이터를 HTML 카드로 변환하는 로직
    cards_html = ""
    for name, info in data.items():
        cards_html += f"""
        <div class="bg-[#2C1E12] border border-[#3C2A21] p-5 rounded-xl shadow-2xl transition hover:border-[#D4AF37]">
            <p class="text-[#A3B18A] text-xs font-bold tracking-widest uppercase mb-2">{name}</p>
            <p class="text-3xl font-serif font-bold text-[#EAE7B1] mb-1">{info['price']}</p>
            <p class="text-sm font-bold {info['color']}">{info['change']}</p>
        </div>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Yeonsinnae Alpha Fund | Pro Dashboard</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Noto+Sans+KR:wght@300;400;700&display=swap');
            body {{ background-color: #120C07; color: #EAE7B1; font-family: 'Noto Sans KR', sans-serif; }}
            .font-serif {{ font-family: 'Playfair Display', serif; }}
            .gold-text {{ color: #D4AF37; }}
            .olive-accent {{ color: #A3B18A; }}
            .panel {{ background: linear-gradient(145deg, #1A120B, #2C1E12); border: 1px solid #3C2A21; }}
        </style>
    </head>
    <body class="p-4 md:p-10 selection:bg-[#D4AF37] selection:text-black">
        <div class="max-w-6xl mx-auto">
            
            <header class="mb-10 flex flex-col md:flex-row justify-between items-end border-b border-[#3C2A21] pb-6">
                <div>
                    <h1 class="text-4xl md:text-5xl font-serif font-bold gold-text mb-2 tracking-tight">Yeonsinnae Alpha Fund</h1>
                    <p class="olive-accent text-sm tracking-[0.2em] uppercase font-bold">AI Securities Team • Institutional Report</p>
                </div>
                <div class="mt-4 md:mt-0 text-right">
                    <p class="text-[#8D99AE] text-xs uppercase tracking-wider">System Update (UTC)</p>
                    <p class="font-mono text-lg text-[#EAE7B1] font-bold">{now_utc}</p>
                </div>
            </header>

            <div class="grid grid-cols-2 md:grid-cols-5 gap-4 mb-10">
                {cards_html}
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                
                <div class="panel p-8 rounded-2xl md:col-span-2 shadow-2xl">
                    <div class="flex justify-between items-center mb-6">
                        <h2 class="text-2xl font-serif gold-text flex items-center">
                            <span class="mr-3 text-3xl">🛡️</span> Defense Strategy
                        </h2>
                        <span class="bg-[#120C07] text-[#D4AF37] px-4 py-1 rounded-full text-sm font-bold border border-[#D4AF37]">현금 보유량 100% 유지</span>
                    </div>
                    
                    <div class="space-y-6 text-[#D1D5DB] leading-relaxed">
                        <div class="border-l-4 border-[#A3B18A] pl-4">
                            <h3 class="text-lg font-bold text-white mb-1">인간지표 분석 (Psyche)</h3>
                            <p class="text-sm">현재 시장은 IREN 유상증자 사태로 촉발된 투심 악화 트라우마가 짙게 깔려 있습니다. '분노'를 넘어선 '침묵의 공포(Capitulation)' 구간에 진입했습니다. 섣부른 바닥 잡기를 금지합니다.</p>
                        </div>
                        <div class="border-l-4 border-[#D4AF37] pl-4">
                            <h3 class="text-lg font-bold text-white mb-1">파생상품 옵션 (Opus)</h3>
                            <p class="text-sm">현재 네거티브 감마(Negative Gamma) 구역. 마켓 메이커의 하방 압력이 존재합니다. S&P 500 맥스페인 레벨인 <strong>6,750</strong> 지지 여부를 최우선으로 확인하십시오.</p>
                        </div>
                    </div>
                </div>

                <div class="panel p-8 rounded-2xl shadow-2xl">
                    <h2 class="text-2xl font-serif gold-text mb-6 flex items-center">
                        <span class="mr-3 text-3xl">🎯</span> Sector Alpha
                    </h2>
                    
                    <ul class="space-y-4">
                        <li class="flex justify-between items-center pb-3 border-b border-[#3C2A21]">
                            <div>
                                <p class="font-bold text-[#EAE7B1]">방위 / 에너지</p>
                                <p class="text-xs text-[#8D99AE]">LMT, XOM</p>
                            </div>
                            <span class="text-red-500 font-bold font-mono">BULL</span>
                        </li>
                        <li class="flex justify-between items-center pb-3 border-b border-[#3C2A21]">
                            <div>
                                <p class="font-bold text-[#EAE7B1]">기술 / 반도체</p>
                                <p class="text-xs text-[#8D99AE]">트럼프 관세 리스크</p>
                            </div>
                            <span class="text-blue-500 font-bold font-mono">BEAR</span>
                        </li>
                        <li class="flex justify-between items-center pb-3 border-b border-[#3C2A21]">
                            <div>
                                <p class="font-bold text-[#EAE7B1]">암호화폐 채굴</p>
                                <p class="text-xs text-[#8D99AE]">IREN 유증 여파 지속</p>
                            </div>
                            <span class="text-stone-500 font-bold font-mono">WAIT</span>
                        </li>
                    </ul>
                </div>
            </div>

            <footer class="mt-12 text-center text-[#8D99AE] text-xs pt-6 border-t border-[#3C2A21]">
                <p>AI Securities Team Automated Engine. Strictly for internal use.</p>
            </footer>
        </div>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    logger.info("엘리트 대시보드 HTML 생성 완료.")

# ---------------------------------------------------------
# 4. 실행
# ---------------------------------------------------------
if __name__ == "__main__":
    logger.info("AI 증권팀 프로 모드 엔진 가동 시작...")
    data = fetch_market_data()
    generate_elite_dashboard(data)
    logger.info("프로세스 종료.")
