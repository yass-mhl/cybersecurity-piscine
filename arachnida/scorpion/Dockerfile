FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    binutils \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install pyinstaller

RUN pyinstaller --onefile scorpion.py

RUN mv ./dist/scorpion /app

CMD ["/scorpion"]
