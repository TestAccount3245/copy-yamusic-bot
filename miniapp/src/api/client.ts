import axios from 'axios'

declare const __API_BASE_URL__: string

// Dev: пустая строка → относительный '/api' (проксируется через nginx)
// GitHub Pages: VITE_API_BASE_URL = URL cloudflared tunnel (https://xxx.trycloudflare.com)
const apiBase = __API_BASE_URL__ || ''

const api = axios.create({
  baseURL: `${apiBase}/api`,
  timeout: 30000,
})

api.interceptors.request.use((config) => {
  const initData = window.Telegram?.WebApp?.initData
  if (initData) {
    config.headers['X-Telegram-Init-Data'] = initData
  }
  return config
})

export default api
