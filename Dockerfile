# 1. 베이스 이미지 설정
FROM python:3.12-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 필요한 파일 복사
COPY requirements.txt ./
# 의존성 설치 후 패키지 캐시 삭제
RUN pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip

# 4. 애플리케이션 코드 복사
COPY . .

# 5. 컨테이너에서 실행할 명령어
# CMD ["python", "run.py"]
CMD ["sh", "-c", "flask db upgrade && python run.py"]