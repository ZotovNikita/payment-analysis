FROM python:3.12.5-slim-bookworm

RUN apt-get update && \
    apt-get install -y python3 python3-pip

WORKDIR /opt/app

RUN pip install torch --no-cache-dir --index-url https://download.pytorch.org/whl/cpu

COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt

COPY ./src ./src

CMD ["python3", "-m", "src"]
