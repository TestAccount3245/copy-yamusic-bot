#!/bin/bash
# Запускает cloudflared tunnel для локального бэкенда
# Telegram Mini App на GitHub Pages будет обращаться к этому URL
#
# Установка cloudflared:
#   Windows: winget install Cloudflare.cloudflared
#   Mac:     brew install cloudflared
#   Linux:   https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
#
# Использование:
#   1. Запусти бэкенд: docker compose up backend
#   2. Запусти этот скрипт: bash scripts/tunnel.sh
#   3. Скопируй URL из вывода (https://xxx.trycloudflare.com)
#   4. Установи его в GitHub repo → Settings → Variables → API_BASE_URL
#   5. Перезапусти GitHub Actions deploy

echo "Starting cloudflared tunnel to localhost:8000..."
echo "The tunnel URL will appear below. Use it as API_BASE_URL."
echo ""

cloudflared tunnel --url http://localhost:8000
