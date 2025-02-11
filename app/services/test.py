import sys
import time  # ✅ 시간 측정을 위해 추가
from app.services.tarot_service import TarotReader

tarot_bot = TarotReader()
for response in tarot_bot.process_query("안녕"):
    print(response, end="")  # 첫 번째 질문

for response in tarot_bot.process_query("내가 방금 뭐라고 했지?"):
    print(response, end="")  # 챗봇이 기억하는지 확인

