import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Proxy for development - in production, VITE_API_URL will be used
    proxy: {
      '/user': 'http://localhost:8000',
      '/game': 'http://localhost:8000',
      '/stats': 'http://localhost:8000',
    }
  }
})
