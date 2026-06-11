FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl gnupg ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-cache the MCP server so first request isn't slow
RUN npx --yes --prefer-offline mongodb-mcp-server@latest --help || true

COPY . .

RUN mkdir -p /etc/secrets/firebase

ENV PORT=8080
EXPOSE 8080

CMD streamlit run frontend/app.py \
    --server.port=$PORT \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --browser.gatherUsageStats=false
