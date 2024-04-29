FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    binutils \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install pyinstaller

RUN pyinstaller --onefile spider.py

RUN pip install flask

RUN mv ./dist/spider /app

CMD ["/spider"]
