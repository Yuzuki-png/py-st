FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3.11 python3.11-venv python3.11-dev \
    python3-pip \
    tesseract-ocr \
    tesseract-ocr-jpn \
    libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && apt-get clean

WORKDIR /var/task

COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

CMD ["app.handler"]
