from app.services.tarot_service import TarotReader 
from langchain.prompts import ChatPromptTemplate
from unittest.mock import patch, MagicMock

# 유닛 테스트
class TestTarotReaderUnits:
    def test_init(self):
        """TarotReader 초기화 테스트"""
        reader = TarotReader()
        assert reader.conversation_state["is_card_drawn"] == False
        assert reader.conversation_state["cards"] is None
        assert reader.conversation_state["card_keywords"] is None
        assert reader.model is not None
        assert reader.memory is not None

    def test_draw_tarot_cards(self):
        """타로 카드 뽑기 테스트"""
        reader = TarotReader()
        cards = reader.draw_tarot_cards()
        
        # 3장의 카드가 뽑혔는지 확인
        assert len(cards) == 3
        
        # 뽑힌 카드가 사용 가능한 타로 카드 목록에 있는지 확인
        valid_cards = [
            "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor", 
            "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit", 
            "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance", 
            "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"
        ]
        for card in cards:
            assert card in valid_cards

        # conversation_state가 적절히 업데이트되었는지 확인
        assert reader.conversation_state["cards"] is not None
        assert reader.conversation_state["card_keywords"] is not None

    def test_create_prompt_first_reading(self):
        """첫 리딩 프롬프트 생성 테스트"""
        reader = TarotReader()
        prompt = reader.create_prompt(is_first_reading=True)
        
        # 프롬프트 템플릿이 제대로 생성되었는지 확인
        assert isinstance(prompt, ChatPromptTemplate)

        # prompt 문자열 확인
        expected_template = reader.base_template + reader.first_reading_prompt
        actual_template = prompt.messages[0].prompt.template
        assert expected_template == actual_template

        # input 변수 key 확인
        expected_inputs = {"text", "chat_history", "cards", "topic", "card_keywords"}
        assert set(prompt.input_variables) == expected_inputs

    def test_create_prompt_follow_up(self):
        """후속 질문 프롬프트 생성 테스트"""
        reader = TarotReader()
        prompt = reader.create_prompt(is_first_reading=False)
        
        # 프롬프트 템플릿이 제대로 생성되었는지 확인
        assert isinstance(prompt, ChatPromptTemplate)

        # prompt 문자열 확인
        expected_template = reader.base_template + reader.follow_up_prompt
        actual_template = prompt.messages[0].prompt.template
        assert expected_template == actual_template

        # input 변수 key 확인
        expected_inputs = {"text", "chat_history", "cards", "topic", "card_keywords"}
        assert set(prompt.input_variables) == expected_inputs


#  테스트
class TestTarotReaderIntegration:
    @patch('app.services.tarot_service.RunnableSequence')
    @patch('app.services.tarot_service.StrOutputParser')
    @patch('app.services.tarot_service.ChatOpenAI')
    def test_process_query_first_time(self, mock_chat_openai, mock_str_parser, mock_runnable_sequence):
        """첫 번째 쿼리 처리 통합 테스트"""
        stream_chunks = ["이것은 ", "테스트 ", "응답입니다."]
        mock_chain = MagicMock()
        
        def fake_stream(*args, **kwargs):
            for chunk in stream_chunks:
                yield chunk
                
        mock_chain.stream.side_effect = fake_stream
        mock_runnable_sequence.return_value = mock_chain
        mock_str_parser.return_value = MagicMock()
        mock_model = MagicMock()
        mock_chat_openai.return_value = mock_model
        
        reader = TarotReader()
        
        assert reader.conversation_state["is_card_drawn"] is False
        assert reader.conversation_state["cards"] is None
        
        responses = list(reader.process_query("내 미래에 대해 알려주세요", "testuser", "미래운"))
        assert responses == stream_chunks
        assert reader.conversation_state["is_card_drawn"] is True
        
        call_kwargs = mock_chain.stream.call_args[1]
        assert "input" in call_kwargs
        input_dict = call_kwargs["input"]
        assert input_dict["text"] == "내 미래에 대해 알려주세요"
        assert input_dict["topic"] == "미래운"

    @patch('app.services.tarot_service.RunnableSequence')
    @patch('app.services.tarot_service.StrOutputParser')
    @patch('app.services.tarot_service.ChatOpenAI')
    def test_process_query_follow_up(self, mock_chat_openai, mock_str_parser, mock_runnable_sequence):
        """후속 쿼리 처리 통합 테스트"""
        stream_chunks = ["후속 ", "테스트 ", "응답입니다."]
        mock_chain = MagicMock()

        def fake_stream(*args, **kwargs):
            for chunk in stream_chunks:
                yield chunk

        mock_chain.stream.side_effect = fake_stream
        mock_runnable_sequence.return_value = mock_chain
        mock_str_parser.return_value = MagicMock()
        mock_model = MagicMock()
        mock_chat_openai.return_value = mock_model

        reader = TarotReader()

        reader.draw_tarot_cards()
        reader.conversation_state["is_card_drawn"] = True
        prev_cards = reader.conversation_state["cards"]

        with patch.object(reader, "create_prompt", wraps=reader.create_prompt) as mock_create_prompt:
            responses = list(reader.process_query("후속 질문이야", "user123", "미래운"))

        assert responses == stream_chunks
        mock_create_prompt.assert_called_once_with(is_first_reading=False)
        assert reader.conversation_state["cards"] == prev_cards
