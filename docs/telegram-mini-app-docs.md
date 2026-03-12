# Telegram Mini Apps Documentation (Reference)

This document describes the key concepts, architecture, and implementation details for Telegram Mini Apps.

Mini Apps allow developers to create web applications that run directly inside Telegram.

Official documentation:
https://core.telegram.org/bots/webapps

---

# 1. Overview

Telegram Mini Apps are web applications that open inside the Telegram client via bots.

They run inside a secure webview and interact with Telegram using the Telegram WebApp JavaScript API.

Mini Apps are typically used for:

- services
- stores
- dashboards
- games
- utilities
- music services

Mini Apps can communicate with a Telegram bot backend.

Architecture:

User → Telegram Client → Mini App (Frontend) → Backend API → Telegram Bot

---

# 2. Core Architecture

Typical system structure:

Frontend (Mini App)
- React / Vue / Next.js / Svelte
- communicates with backend API
- uses Telegram WebApp JS SDK

Backend
- Python (FastAPI recommended)
- business logic
- API endpoints
- database
- external integrations

Telegram Bot
- aiogram / python-telegram-bot
- launches the mini app
- sends files and notifications

Database
- PostgreSQL
- Redis (optional cache)

---

# 3. Launching Mini Apps

Mini Apps are launched via Telegram bots.

Example button:

InlineKeyboardButton(
    text="Open App",
    web_app=WebAppInfo(url="https://example.com")
)

When the user clicks the button, Telegram opens the Mini App.

---

# 4. Telegram WebApp JavaScript API

The Telegram client injects a global object:

window.Telegram.WebApp

Example initialization:

```javascript
const tg = window.Telegram.WebApp;
tg.ready();

Important functions:

Expand App
tg.expand();

Expands Mini App to full screen.

Main Button
tg.MainButton.setText("Download");
tg.MainButton.show();
tg.MainButton.onClick(() => {
    console.log("clicked");
});
Theme detection
tg.themeParams

Contains colors for dark/light themes.

Sending data to bot
tg.sendData(JSON.stringify({
  action: "download_track",
  track_id: 123
}));

Bot receives the data via web_app_data.

5. Authentication

Telegram provides signed user data.

Frontend receives:

initData
initDataUnsafe

Backend must verify the signature using the bot token.

Steps:

Receive initData

Parse query params

Generate HMAC-SHA256 hash

Compare with provided hash

If valid → user authenticated.

6. Recommended Frontend Stack

Best frameworks:

React
Next.js
Vue
Svelte

Useful UI libraries:

Tailwind

Radix UI

ShadCN

Framer Motion

7. Design Guidelines

Mini Apps should feel native inside Telegram.

Recommended UI:

Liquid Glass design

translucent panels

smooth transitions

minimal navigation

responsive layout

Navigation style:

Home
Search
Library
Profile

8. Communication with Backend

Use REST API or GraphQL.

Typical requests:

GET /search?q=track

GET /track/{id}

GET /album/{id}

POST /download

POST /upload-track

9. File downloads

Mini Apps cannot directly send large files to Telegram chat.

Instead:

Mini App → backend request → bot sends file to user.

Flow:

User clicks "Download"

Mini App calls API

Backend downloads file

Bot sends audio file

10. Security Best Practices

Always verify Telegram initData.

Implement:

rate limiting

request validation

authentication tokens

upload limits

11. Performance Recommendations

Use:

Redis caching
CDN for static assets
async backend

Avoid:

large frontend bundles
blocking API requests

12. Deployment

Typical setup:

Frontend → Vercel / Cloudflare / Nginx

Backend → Docker + FastAPI

Bot → Python service

Infrastructure example:

Nginx
↓
Mini App frontend
↓
FastAPI backend
↓
Redis / PostgreSQL
↓
Telegram Bot