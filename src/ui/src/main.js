import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'
import { useFeatureFlags } from './composables/useFeatureFlags.js'

// Initialize the app
const app = createApp(App)

// Initialize feature flags before mounting
const { initializeFeatureFlags } = useFeatureFlags()

initializeFeatureFlags().then(() => {
  console.log('Feature flags initialized')
}).catch(err => {
  console.warn('Failed to initialize feature flags:', err)
}).finally(() => {
  // Mount the app regardless of feature flag initialization success
  app.use(router).mount('#app')
})