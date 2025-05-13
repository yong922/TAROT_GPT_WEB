from unittest.mock import MagicMock

# 가짜 generator 함수
def fake_stream(*args, **kwargs):
    yield "이것은 "
    yield "테스트 "
    yield "응답입니다."

# mock 객체 만들기
mock_model = MagicMock()
mock_model.stream = fake_stream
mock_model.return_value = mock_model

# "서비스" 흉내
model_instance = mock_model()
stream_response = model_instance.stream(input="dummy")

# 결과 직접 출력
for chunk in stream_response:
    print("[chunk 출력]", chunk)