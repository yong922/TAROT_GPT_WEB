from app import create_app  # Flask 앱을 불러옴
from app.models import ChatHistory, db

app = create_app()  # Flask 애플리케이션 인스턴스 생성

def test_save_chat_history():
    """DB에 JSON 데이터가 정상적으로 저장되는지 테스트"""
    with app.app_context():  # ✅ Flask 애플리케이션 컨텍스트 활성화
        test_chat = ChatHistory(
            user_id="test_id",
            topic="미래운",
            message=[
                {"role": "user", "text": "올해 취직이 가능할까?"},
                {"role": "bot", "text": "네, 긍정적인 변화가 예상됩니다!"}
            ]
        )

        db.session.add(test_chat)
        db.session.commit()

        print("✅ 대화 저장 완료!")
        print(f"Chat ID: {test_chat.chat_id}")

# 실행
if __name__ == "__main__":
    test_save_chat_history()