import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [
    vue()
    // Cloudflare plugin disabled for Docker development to avoid workerd binary issues
  ],
  server: {
    port: 3000,
    host: '0.0.0.0'
  },
  build: {
    // Optimize for static asset hosting
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    minify: 'terser',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue', 'vue-router', 'axios']
        }
      }
    },
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true
      }
    }
  },
  define: {
    // Replace API base URL based on environment
    __API_BASE_URL__: JSON.stringify(
      process.env.NODE_ENV === 'production' 
        ? 'https://api.mosaicplane.info'
        : '/api'
    )
  }
})