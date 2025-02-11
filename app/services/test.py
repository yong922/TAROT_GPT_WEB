import sys
import time  # ✅ 시간 측정을 위해 추가
from app.services.tarot_service import TarotReader

tarot_reader = TarotReader()

test_message = "오늘의 운세를 알려줘."

print("🔍 Chunk 단위 응답 테스트 시작...\n")

start_time = time.time()  # ✅ 시작 시간 기록

# ✅ chunk 단위로 데이터가 오는 속도 확인
for chunk in tarot_reader.process_query(test_message):
    elapsed_time = time.time() - start_time  # ✅ 경과 시간 계산
    print(f"({elapsed_time:.2f}s) 🟢 Chunk: {chunk}", flush=True)  # ✅ 시간 출력 + 즉시 출력
    start_time = time.time()  # ✅ 다음 chunk 타이밍 기록
