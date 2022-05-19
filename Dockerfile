FROM debian:bullseye AS builder

WORKDIR /tmp

ARG CHROME_VERSION="101.0.4951.54-1"
# Check available versions here: https://www.ubuntuupdates.org/package/google_chrome/stable/main/base/google-chrome-stable
RUN apt update && apt install unzip wget -y  \
  && wget --no-verbose -O /tmp/chrome.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}_amd64.deb
#  && apt install -y /tmp/chrome.deb \
#  && rm /tmp/chrome.deb \
#  && apt clean && rm -rf /var/lib/apt/lists/*

RUN wget  --no-verbose  https://chromedriver.storage.googleapis.com/101.0.4951.41/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip
#    && rm chromedriver_linux64.zip \



FROM python:bullseye

WORKDIR /app

ENV PATH="/app:${PATH}"

COPY --from=builder /tmp/chrome.deb .
COPY --from=builder /tmp/chromedriver .
RUN    apt install -y /tmp/chrome.deb \
       && rm /tmp/chrome.deb

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENTRYPOINT ["python3","main.py"]