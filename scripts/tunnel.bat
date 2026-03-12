@echo off
REM Запускает cloudflared tunnel для локального бэкенда (Windows)
REM
REM Установка: winget install Cloudflare.cloudflared
REM
REM 1. Запусти бэкенд: docker compose up backend
REM 2. Запусти этот скрипт
REM 3. Скопируй URL (https://xxx.trycloudflare.com)
REM 4. Установи его в GitHub repo → Settings → Variables → API_BASE_URL

echo Starting cloudflared tunnel to localhost:8000...
echo The tunnel URL will appear below. Use it as API_BASE_URL.
echo.

cloudflared tunnel --url http://localhost:8000
