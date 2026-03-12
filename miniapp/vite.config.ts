import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  // GitHub Pages: set to '/repo-name/'. Custom domain or local: '/'
  base: process.env.GITHUB_ACTIONS ? '/copy-yamusic-bot/' : '/',
  server: {
    host: '0.0.0.0',
    port: 3000,
  },
  define: {
    __API_BASE_URL__: JSON.stringify(process.env.VITE_API_BASE_URL || ''),
  },
})
