FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt && \
    rm -rf /root/.cache/pip

COPY . .

CMD ["python", "run.py"]