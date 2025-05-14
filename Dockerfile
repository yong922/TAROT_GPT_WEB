FROM python:3.12-slim

WORKDIR /app

COPY requirement.txt ./

RUN pip install --no-cache-dir -r requirement.txt \
    && rm -rf /root/.cache/pip

COPY . .

CMD ["python", "run.py"]
