import yfinance as yf
import datetime
import json
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Beast_V18")

def fetch_extensive_data():
    assets = {
        "CURR": {"원/달러": "USDKRW=X", "USDT": "USDT-USD", "USDC": "USDC-USD", "USDT_KRW": "USDT-KRW", "USDC_KRW": "USDC-KRW"},
        "INDEX": {"코스피": "^KS11", "나스닥": "^IXIC", "S&P500": "^GSPC", "공포지수": "^VIX"},
        "CRYPTO": {"비트코인": "BTC-USD", "이더리움": "ETH-USD"}
    }
    data_pool = {}
    for cat, group in assets.items():
        for name, sym in group.items():
            try:
                t = yf.Ticker(sym)
                h = t.history(period="7d")
                if len(h) >= 2:
                    prices = h['Close'].round(2).tolist()
                    curr, prev = h['Close'].iloc[-1], h['Close'].iloc[-2]
                    chg = ((curr - prev) / prev) * 100
                    data_pool[sym] = {"name": name, "price": curr, "chg": chg, "history": prices}
                else:
                    data_pool[sym] = {"name": name, "price": 0.0, "chg": 0.0, "history": [0,0]}
            except:
                data_pool[sym] = {"name": name, "price": 0.0, "chg": 0.0, "history": [0,0]}
    
    # USDT/USDC 원화 변환 로직 (김치 프리미엄 또는 직접 환산)
    krw_rate = data_pool.get("USDKRW=X", {}).get("price", 1400.0)
    
    usdt_krw = data_pool.get("USDT-KRW", {}).get("price", 0.0)
    if usdt_krw < 1000: # 데이터가 없거나 비정상일 경우 환율로 직접 계산
        usdt_krw = data_pool.get("USDT-USD", {}).get("price", 1.0) * krw_rate * 1.01 # 1% 김프 가정보정
    data_pool["USDT_KRW_CALC"] = {"name": "USDT(원)", "price": usdt_krw, "chg": data_pool.get("USDT-USD", {}).get("chg", 0)}

    usdc_krw = data_pool.get("USDC-KRW", {}).get("price", 0.0)
    if usdc_krw < 1000:
        usdc_krw = data_pool.get("USDC-USD", {}).get("price", 1.0) * krw_rate * 1.01
    data_pool["USDC_KRW_CALC"] = {"name": "USDC(원)", "price": usdc_krw, "chg": data_pool.get("USDC-USD", {}).get("chg", 0)}

    return data_pool

def ai_meeting_results():
    # 1. 섹터별 요약 브리핑
    summary = {
        "반도체/AI": "엔비디아 하단 지지선 확보. 레버리지(SOXL) 공매도 잔고 임계점 도달로 숏스퀴즈 화약고 상태.",
        "지정학/거시": "달러 강세 및 지정학적 리스크 지속. 안전자산과 코인 시장으로의 자금 양극화 현상 심화.",
        "빅테크": "ETF(QQQ) 자금 유입 가속화. 이번 주 실적 발표 기업(AVGO 등) 가이던스 상향 기대감 선반영.",
        "코인/레버리지": "이더리움 현물 수급 폭발. 가상자산 관련주(MSTR, MARA) 변동성 극대화 및 세력 매집 포착."
    }
    # 2. 4대 성향별 엄선 종목
    recs = [
        {"title": "🔥 싸나이테스트 (엄선)", "ticker": "ETHU, SOXL, MSTR", "reason": "변동성 상위 1% 정예. 숏스퀴즈 타점 및 광기 수급 포착."},
        {"title": "🏃‍♂️ 평범이의 숟가락 (엄선)", "ticker": "TQQQ, NVDA, TSLA", "reason": "추세 추종 매매 최적화. 스마트 머니 유입 및 눌림목 반등 구간."},
        {"title": "🛡️ 쫄보들의 안식처 (엄선)", "ticker": "SCHD, TLT, IAU", "reason": "위원회 자산 방어 분과 엄선. 하방 경직성 및 배당 안전성 1위."},
        {"title": "🕵️ 세력 형님 뒤쫓기 (엄선)", "ticker": "LABU, COIN, MARA", "reason": "온체인 대량 매집 시그널. 공매도 항복 임박한 리버설 타점 요격."}
    ]
    # 3. 주요 옵션 세력 타점 (TOP 5)
    options = [
        {"t": "NVDA", "d": "03-20", "p": "135.0", "s": "콜옵션 프리미엄 과열. 135불 수렴 예상."},
        {"t": "TSLA", "d": "03-20", "p": "210.0", "s": "맥스페인 부근 횡보 유지. 돌파 시 헤지 매수 폭증."},
        {"t": "ETHU", "d": "03-27", "p": "15.0", "s": "이더리움 2배 옵션 신규 매수세 유입."},
        {"t": "SOXL", "d": "03-20", "p": "45.0", "s": "세력들 하단 42불 강력 지지 중."},
        {"t": "LABU", "d": "03-27", "p": "125.0", "s": "바이오 수급 유입 시작. 리버설 상방 압력 감지."}
    ]
    # 4. 실적 발표 7일 (2026년 3월 5일 목요일 기준 정확한 캘린더)
    earnings = [
        {"date": "03-05 (오늘/목)", "comps": [
            {"n": "Broadcom", "s": "AVGO", "d": "broadcom.com", "t": "장후", "rec": True},
            {"n": "Costco", "s": "COST", "d": "costco.com", "t": "장후", "rec": True}
        ]},
        {"date": "03-06 (금)", "comps": [{"n": "Marvell", "s
