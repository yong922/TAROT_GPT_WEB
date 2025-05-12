import pytest
from unittest.mock import patch, MagicMock
from app.routes.chat_routes import tarot_reader


@pytest.fixture
def mock_current_user():
    mock_user = MagicMock()
    mock_user.id = "testuser"
    mock_user.nickname = "테스트유저"
    return mock_user


def test_chat_page_loads(client, mock_current_user):
    """
    ✅ /chat/ 페이지가 로그인된 유저에게 정상적으로 열리는지 확인
    
    - 로그인 세션 -> 채팅 메인 페이지 진입
    - mock_user로 로그인 유저가 정상적으로 인식되는지 확인
    - 페이지 로드 시 유저 닉네임이 포함된 응답을 받는지 확인
    """
    with patch("flask_login.utils._get_user", return_value=mock_current_user), \
         patch("app.routes.chat_routes.get_chat_list", return_value=[]):
        response = client.get("/chat/")
        assert response.status_code == 200
        assert "테스트유저" in response.get_data(as_text=True)


def test_set_topic_updates_state(client):
    """ 
    ✅ 모델의 토픽 변수 설정 API 
    - POST 요청이 성공적으로 처리되는지 (200 ok)
    - conversation_state["topic"]이 업데이트 되는지
    """
    response = client.post("/chat/set_topic", json={"topic": "연애운"})

    assert response.status_code == 200
    assert tarot_reader.conversation_state["topic"] == "연애운"
    
    data = response.get_json()
    assert data["status"] == "success"
    assert data["message"] == "토픽이 설정되었습니다."


def test_draw_tarot_returns_cards(client):
    """
    ✅ 사용자가 타로카드를 뽑을 때 리딩&이미지URL 잘 반환하는지

    - 타로 카드 추출 → 리딩 보여주는 메인 로직
    - draw_tarot_cards() 결과 반환
    - "cards" 키에 카드 리딩 결과 포함
    """
    with patch.object(tarot_reader, "draw_tarot_cards", return_value=["The Fool", "The Magician", "The High Priestess"]), \
         patch("app.routes.chat_routes.get_images_url", return_value={
             "The Fool": "/static/imgs/tarot_front_images/The Fool.png",
             "The Magician": "/static/imgs/tarot_front_images/The Magician.png",
             "The High Priestess": "/static/imgs/tarot_front_images/The High Priestess.png"
         }):
        response = client.post("/chat/draw_tarot")
        data = response.get_json()

        assert response.status_code == 200
        assert data["cards"] == ["The Fool", "The Magician", "The High Priestess"]
        assert data["card_images_url"] == {
            "The Fool": "/static/imgs/tarot_front_images/The Fool.png",
            "The Magician": "/static/imgs/tarot_front_images/The Magician.png",
            "The High Priestess": "/static/imgs/tarot_front_images/The High Priestess.png"
        }


def test_get_latest_chat(client, mock_current_user):
    """ 
    ✅ 가장 최근의 chat_id 조회
    """
    with patch("flask_login.utils._get_user", return_value=mock_current_user), \
         patch("app.routes.chat_routes.get_latest_chat_id", return_value=42):
        response = client.get("/chat/get_latest_chat_id")
        data = response.get_json()

        assert response.status_code == 200
        assert data["chat_id"] == 42


@pytest.mark.parametrize(
    "chat_id_key, expected_status, expected_count, expected_messages, description", [
        ("chat1_id", 200, 2, [
            {"sender": "human", "message": "chat1 msg1 human message"},
            {"sender": "ai", "message": "chat1 msg2 ai message response"}
        ], "존재하는 chat_id - 메시지 있음"),
        ("non_existent_id", 200, 0, [], "존재하지 않는 chat_id"),
        ("empty_chat_id", 200, 0, [], "존재하는 chat_id - 메시지 없음")
    ]
)
def test_fetch_chat_messages_parametrize(client,history_test_data, empty_chat, 
                                         chat_id_key, expected_status, expected_count, 
                                         expected_messages, description):
    """
    채팅 메시지 조회 테스트를 여러 경우에 대해 수행:
    1. 존재하는 chat_id - 메시지 있음
    2. 존재하지 않는 chat_id
    3. 존재하는 chat_id - 메시지 없음
    """
    chat_id_map = {
        "chat1_id": history_test_data["chat1_id"],
        "non_existent_id": 9999,
        "empty_chat_id": empty_chat
    }
    chat_id = chat_id_map[chat_id_key]
    
    response = client.get(f"/chat/{chat_id}")
    data = response.get_json()

    assert response.status_code == expected_status, f"실패: {description}"
    assert isinstance(data, list), f"응답이 리스트가 아님: {description}"
    assert len(data) == expected_count, f"메시지 수 불일치: {description}"

    for i, expected_msg in enumerate(expected_messages):
        assert data[i]["sender"] == expected_msg["sender"], f"sender 불일치: {description}"
        assert data[i]["message"] == expected_msg["message"], f"message 불일치: {description}"


def test_delete_chat_success(client):
    """
    ✅ 특정 채팅 기록 삭제 API
    """
    with patch("app.routes.chat_routes.delete_chat_from_db", return_value=True):
        response = client.delete("/chat/delete_chat/999")
        data = response.get_json()

        assert response.status_code == 200
        assert data["success"] is True


def test_save_bot_response_empty_chat_history(client):
    """
    ✅ chat_history가 비어있을 때 'empty' 반환하는지 테스트
    """
    with patch("app.routes.chat_routes.tarot_reader.memory.chat_memory.messages", []):
        response = client.post("/chat/save_bot_response", json={"chat_id": 1})
        data = response.get_json()

        assert response.status_code == 200
        assert data["status"] == "empty"
        assert data["message"] == "No chat history found."


def test_save_bot_response_success(client):
    """
    ✅ chat_history가 있을 때 'success' 반환하는지 테스트
    """
    fake_messages = [MagicMock(content="This is a test bot message.")]
    with patch("app.routes.chat_routes.tarot_reader.memory.chat_memory.messages", fake_messages), \
         patch("app.routes.chat_routes.save_message"):
        response = client.post("/chat/save_bot_response", json={"chat_id": 1})
        data = response.get_json()

        assert response.status_code == 200
        assert data["status"] == "success"
        assert data["message"] == "Bot response saved."