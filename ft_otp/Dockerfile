FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    binutils \
    oathtool \
    && rm -rf /var/lib/apt/lists/*

RUN pip install pyinstaller

RUN pyinstaller --onefile ft_otp.py

RUN mv ./dist/ft_otp /app

CMD ["/ft_otp"]
