FROM python:3.8.16-slim-buster
COPY requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /usr/local/src
COPY ./ ./
ENTRYPOINT ["python", "./predictor/src/aiokafka_agent_main.py", "-u"]