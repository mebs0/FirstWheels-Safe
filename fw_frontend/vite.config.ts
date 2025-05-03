import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import vueDevTools from 'vite-plugin-vue-devtools'

export default defineConfig({
  server: {
    https: {
      key: './key.pem',
      cert: './cert.pem',
    },
    host: '0.0.0.0',
    port: 5173,
    allowedHosts: ['10.0.0.26'],
  },
  plugins: [
    vue(),
    vueJsx(),
    //vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})
