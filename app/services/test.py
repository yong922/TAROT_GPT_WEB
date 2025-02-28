import json
from langchain.memory import ConversationBufferMemory

def format_chat_history(chat_history):
    """
    ✅ ConversationBufferMemory 데이터를 JSON 형식으로 변환하는 함수
    - HumanMessage, AIMessage 객체에서 content만 추출하여 저장
    """
    formatted_history = []
    for i, message in enumerate(chat_history):
        role = "user" if i % 2 == 0 else "bot"
        content = message.content  # ✅ content 부분만 추출
        formatted_history.append({"role": role, "message": content})

    return json.dumps({"history": formatted_history}, ensure_ascii=False) # ✅ JSON 변환


# ✅ Memory 객체 생성
memory = ConversationBufferMemory(
    memory_key="chat_history",
    input_key="text",
    return_messages=True  # ✅ 리스트 형태로 반환됨
)

# ✅ 대화 추가 (사용자 & 챗봇)
memory.chat_memory.add_user_message("오늘의 운세를 봐줘")
memory.chat_memory.add_ai_message("좋아! 카드를 뽑을게...")
memory.chat_memory.add_user_message("내 연애운은 어때?")
memory.chat_memory.add_ai_message("The Lovers 카드가 나왔어!")

# ✅ 메모리 데이터 출력 (변환 전)
memory_data = memory.load_memory_variables({})
print("\n🔹 [1] 변환 전 Memory 데이터 확인:")
print(memory_data)

# ✅ chat_history만 출력
chat_history = memory_data["chat_history"]
print("\n🔹 [2] 변환 전 chat_history 형식:")
print(chat_history)

# ✅ JSON 변환 후 출력
json_chat_history = format_chat_history(chat_history)
print("\n🔹 [3] JSON 변환 후 최종 저장 데이터:")
print(json_chat_history)
