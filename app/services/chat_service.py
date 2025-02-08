from .tarot_service import TarotReader

tarot_reader = TarotReader()

class ChatService:
    def __init__(self):
        # 메시지 저장 리스트
        self.messages = [
            {
                "sender": "bot",
                "text": "타로 할머니에게 어서 오렴.👵🔮 궁금한 게 있다면 편하게 질문해보려무나. 타로카드 3장을 뽑아서 설명해줄게~📜🪄"
            }
        ]
        # (대화 흐름을 시간순으로 유지하기 위해 리스트로 저장)

    # 대화 시작 시 '초기 메시지' 반환
    def get_initial_message(self):
        return self.messages

    # 사용자 메시지 추가
    def add_user_message(self, text):
        self.messages.append({"sender": "user", "text": text})
        # self.messages 반환   -> user 입력 메시지로 수정
        return self.messages

    # 챗봇 메시지 추가
    def add_bot_message(self, text):
        self.messages.append({"sender": "bot", "text": text})
        # bot 응답 메시지 반환
        return self.messages[-1]
    
    # 전체 메시지 반환
    def get_all_messages(self):
        return self.messages
    
    # 챗봇 응답 생성
    def process_message(self, user_message, topic=None):
        bot_response = tarot_reader.process_query(topic=topic, text=user_message)  # 타로 해석 호출
        return bot_response