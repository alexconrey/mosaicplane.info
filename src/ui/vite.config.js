import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { cloudflare } from '@cloudflare/vite-plugin'

export default defineConfig({
  plugins: [
    vue({
      template: {
        compilerOptions: {
          // Enable production optimizations for better SEO performance
          hoistStatic: true,
          cacheHandlers: true
        }
      }
    }),
    cloudflare()
  ],
  server: {
    port: 3000,
    host: '0.0.0.0',
    historyApiFallback: true
  },
  build: {
    // Optimize for Cloudflare Workers static asset hosting with aggressive caching
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    minify: 'terser',
    rollupOptions: {
      output: {
        // Enable content-based file naming for optimal caching
        entryFileNames: 'assets/[name]-[hash].js',
        chunkFileNames: 'assets/[name]-[hash].js',
        assetFileNames: (assetInfo) => {
          const fileName = assetInfo.names?.[0] || 'unknown';
          const extType = fileName.split('.').at(1);
          if (/png|jpe?g|svg|gif|tiff|bmp|ico/i.test(extType)) {
            return `assets/images/[name]-[hash][extname]`;
          }
          if (/woff2?|ttf|eot/i.test(extType)) {
            return `assets/fonts/[name]-[hash][extname]`;
          }
          return `assets/[name]-[hash][extname]`;
        },
        manualChunks: {
          vendor: ['vue', 'vue-router', 'axios']
        }
      }
    },
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
        // Additional SEO performance optimizations
        dead_code: true
        // Note: drop_unused was removed in terser 5.x
      },
      mangle: {
        safari10: true // Fix Safari 10 compatibility
      }
    },
    // SEO performance optimizations
    chunkSizeWarningLimit: 1000, // Warn for chunks larger than 1MB
    target: 'es2018' // Modern browser support for better performance
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