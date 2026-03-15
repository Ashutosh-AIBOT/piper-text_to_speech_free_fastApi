---
title: Piper Text-to-Speech API
emoji: 🗣️
colorFrom: blue
colorTo: green
sdk: docker
sdk_version: latest
app_file: Dockerfile
pinned: false
---

# Piper TTS API

A FastAPI-based Text-to-Speech API using Piper TTS

## Features

- High-quality English TTS
- Simple password authentication
- Docker support
- Ready for Hugging Face Spaces

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/tts` | POST | Convert text to speech |
| `/health` | GET | Health check |
| `/docs` | GET | Swagger documentation |

## Usage

```bash
curl -X POST https://your-space.hf.space/v1/tts \
  -H "Authorization: your-password" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world"}' \
  --output speech.wav