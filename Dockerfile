FROM python:3.8-slim

WORKDIR /app

COPY requirement.txt ./

RUN pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip

COPY . .

CMD ["python", "run.py"]