FROM python:3.11-slim-bullseye

WORKDIR /app

ARG GO_VERSION=1.22.1

ARG TARGETARCH

RUN apt-get update && \
    apt-get install -y --no-install-recommends wget ca-certificates && \
    wget "https://golang.org/dl/go${GO_VERSION}.linux-${TARGETARCH}.tar.gz" -O go.tar.gz && \
    tar -C /usr/local -xzf go.tar.gz && \
    rm go.tar.gz && \
    export PATH="/usr/local/go/bin:${PATH}" && \
    go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest && \
    apt-get purge -y --auto-remove wget && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PATH="/usr/local/go/bin:/root/go/bin:${PATH}"

CMD ["python", "main.py"]