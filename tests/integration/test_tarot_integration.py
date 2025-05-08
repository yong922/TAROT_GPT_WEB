from unittest.mock import MagicMock, patch
import time  # 누락된 임포트 추가
from app.services.tarot_service import TarotReader

class TestTarotReaderIntegration:
    @patch('app.services.tarot_service.RunnableSequence')
    @patch('app.services.tarot_service.StrOutputParser')
    @patch('app.services.tarot_service.ChatOpenAI')
    def test_process_query_first_time(self, mock_chat_openai, mock_str_parser, mock_runnable_sequence):
        """첫 번째 쿼리 처리 통합 테스트"""
        
        # 테스트 데이터 설정
        stream_chunks = ["이것은 ", "테스트 ", "응답입니다."]
        
        # Mock RunnableSequence 설정
        mock_chain = MagicMock()
        
        def fake_stream(*args, **kwargs):
            for chunk in stream_chunks:
                yield chunk
                
        mock_chain.stream.side_effect = fake_stream
        mock_runnable_sequence.return_value = mock_chain
        
        # Mock StrOutputParser
        mock_str_parser.return_value = MagicMock()
        
        # Mock ChatOpenAI
        mock_model = MagicMock()
        mock_chat_openai.return_value = mock_model
        
        # 테스트 대상 객체 생성
        reader = TarotReader()
        
        # 기본 대화 상태 확인
        assert reader.conversation_state["is_card_drawn"] is False
        assert reader.conversation_state["cards"] is None
        
        # 테스트 실행
        with patch('time.sleep') as mock_sleep: 
            responses = list(reader.process_query("내 미래에 대해 알려주세요", "testuser", "미래운"))
        
        # 테스트 검증
        assert responses == stream_chunks
        assert reader.conversation_state["is_card_drawn"] is True
        
        # RunnableSequence 생성 검증
        mock_runnable_sequence.assert_called_once()
        
        # 호출 파라미터 검증
        mock_chain.stream.assert_called_once()
        call_kwargs = mock_chain.stream.call_args[1]
        assert "input" in call_kwargs
        input_dict = call_kwargs["input"]
        assert input_dict["text"] == "내 미래에 대해 알려주세요"
        assert input_dict["topic"] == "미래운"