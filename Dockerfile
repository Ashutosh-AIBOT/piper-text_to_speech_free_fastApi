FROM python:3.10-slim

# Install system dependencies for Piper
RUN apt-get update && apt-get install -y \
    wget \
    git \
    g++ \
    make \
    cmake \
    espeak-ng \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Download Piper model using wget (WORKS 100%)
RUN mkdir -p /root/.piper && \
    cd /root/.piper && \
    echo "📥 Downloading Piper model en_US-amy-medium..." && \
    wget -q --show-progress https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx && \
    wget -q --show-progress https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx.json && \
    echo "✅ Model downloaded successfully!" && \
    ls -la /root/.piper/

# Copy application code
COPY app/ ./app/
COPY .env.example .env

# Expose port
EXPOSE 7860

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]