import yfinance as yf
import datetime
import logging

# [상단 fetch_extensive_data 및 기본 로직은 V9.0과 동일]

def generate_v9_5_html(data, recs, flow, warn):
    now = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
    ant_face_url = "https://i.ibb.co/v6XkYvR/ax-removebg.png"

    # [중략: 카드 생성 로직]

    html = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>연신내 개미펀드 V9.5</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Inter:wght@400;900&display=swap');
            body {{ background-color: #1e1e1e; color: #c4c4c4; font-family: 'Inter', sans-serif; }}
            h1, h2, h3 {{ font-family: 'Black Han Sans', sans-serif; }}
            @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
            .ant-logo {{ width: 90px; height: 90px; object-fit: contain; animation: spin 12s linear infinite; filter: drop-shadow(0 0 15px rgba(255,255,255,0.3)); }}
        </style>
    </head>
    <body class="p-4 md:p-10">
        <div class="max-w-7xl mx-auto">
            <header class="flex flex-col md:flex-row justify-between items-center mb-12 border-b border-zinc-800 pb-8 gap-6">
                <div class="flex items-center gap-6">
                    <img src="{ant_face_url}" class="ant-logo" alt="야수 개미 로고">
                    <div>
                        <h1 class="text-5xl font-black text-white italic tracking-tighter">연신내 개미펀드</h1>
                        <p class="text-red-500 font-black text-xs mt-1 tracking-[0.5em] uppercase">야수 모드: 가동 중 (코스피 폭등 감지)</p>
                    </div>
                </div>
                <div class="bg-[#2d2d2d] px-6 py-2 rounded-xl border border-zinc-700 shadow-2xl">
                    <p class="text-[10px] text-zinc-500 font-black">최종 동기화 시간</p>
                    <p class="text-sm font-black text-white">{now}</p>
                </div>
            </header>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-12">
                <div class="lg:col-span-2 bg-[#2d2d2d] p-8 rounded-3xl border border-zinc-800 shadow-2xl relative overflow-hidden">
                    <h2 class="text-3xl font-black text-white mb-6 italic">🏛️ 15인 위원회 긴급 전략 회의록</h2>
                    <div class="space-y-6">
                        <div class="bg-red-500/10 p-6 rounded-2xl border border-red-500/20">
                            <p class="text-xs text-red-500 font-black mb-2 uppercase underline">시장 자금 흐름 브리핑</p>
                            <p class="text-lg text-white leading-relaxed font-black">{flow}</p>
                        </div>
                        <div class="bg-zinc-800/50 p-6 rounded-2xl border border-zinc-700">
                            <p class="text-xs text-zinc-500 font-black mb-2">트레이딩 코치 잔소리</p>
                            <p class="text-sm text-zinc-300 font-bold">{warn}</p>
                        </div>
                    </div>
                </div>
                <div class="bg-[#2d2d2d] p-8 rounded-3xl border border-zinc-800 shadow-2xl">
                    <h3 class="text-xs font-black text-zinc-500 mb-8 uppercase border-l-4 border-red-600 pl-4">실시간 위험 감지 판넬</h3>
                    <div class="space-y-8">
                        <div class="space-y-2"><div class="flex justify-between text-xs font-black"><span>공포/탐욕 수치</span><span class="text-white">극도의 탐욕</span></div><div class="w-full bg-zinc-800 h-2 rounded-full"><div class="bg-red-500 h-2 rounded-full" style="width: 88%"></div></div></div>
                        <div class="space-y-2"><div class="flex justify-between text-xs font-black"><span>세력 매집 강도</span><span class="text-white">폭발적</span></div><div class="w-full bg-zinc-800 h-2 rounded-full"><div class="bg-white h-2 rounded-full" style="width: 95%"></div></div></div>
                    </div>
                </div>
            </div>
            </div>
    </body>
    </html>
    """
    with open("index.html", "w", encoding="utf-8") as f: f.write(html)
