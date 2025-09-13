<template>
  <div id="app" :data-theme="theme" class="app-layout">
    <!-- Skip to main content link for keyboard users -->
    <a href="#main-content" class="sr-only skip-link">Skip to main content</a>
    
    <!-- Header with dark/light mode toggle -->
    <header class="header" role="banner">
      <div class="container">
        <div class="flex justify-between items-center">
          <div>
            <h1>
              <router-link to="/" class="header-link" aria-label="Go to homepage">{{ siteName }}</router-link>
            </h1>
            <p class="subtitle">{{ siteTagline }}</p>
          </div>
          <button 
            @click="toggleTheme" 
            class="btn btn-secondary theme-toggle"
            :aria-label="`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`"
            :title="`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`"
          >
            <span aria-hidden="true">{{ theme === 'light' ? '🌙' : '☀️' }}</span>
            <span class="desktop-only">{{ theme === 'light' ? 'Dark' : 'Light' }}</span>
          </button>
        </div>
      </div>
    </header>

    <!-- MOSAIC Info Banner -->
    <div class="info-banner" role="banner" aria-label="MOSAIC regulation information">
      <div class="container">
        <div class="banner-content">
          <div class="banner-text">
            <strong>MOSAIC Final Rule Effective:</strong> October 22, 2025 | 
            <strong>LSA Criteria:</strong> ≤61 knots stall speed | 
            <strong>Sport Pilot:</strong> ≤59 knots, 1 passenger max
          </div>
          <router-link to="/mosaic" class="info-link" aria-label="Learn more about MOSAIC regulations">
            More Info
          </router-link>
        </div>
      </div>
    </div>

    <!-- Main content -->
    <main id="main-content" class="main" role="main">
      <div class="container">
        <router-view />
      </div>
    </main>

    <!-- Footer -->
    <footer class="footer" role="contentinfo">
      <div class="container">
        <div class="flex justify-center items-center flex-col gap-2">
          <p class="text-secondary">
            Data based on FAA MOSAIC Final Rule (July 2025)
          </p>
          <p class="text-secondary">
            <small>
              API: <a href="/api/docs/" target="_blank" class="text-accent" aria-label="API Documentation (opens in new tab)">Documentation</a> |
              <router-link to="/about#legal-disclaimer" class="text-accent">Legal Disclaimer</router-link>
            </small>
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { onMounted, provide } from 'vue'
import { useTheme } from './composables/useTheme'
import { useBranding } from './composables/useBranding'

const { theme, toggleTheme } = useTheme()
const { siteName, siteTagline, showAllAircraft, isMosaicPlane } = useBranding()

// Provide theme and branding to child components
provide('theme', theme)
provide('branding', { siteName, siteTagline, showAllAircraft, isMosaicPlane })

onMounted(() => {
  // Set initial theme on document
  document.documentElement.setAttribute('data-theme', theme.value)
})
</script>

<style scoped>
.header {
  background-color: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
  padding: 1.5rem 0;
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
}

.header-link {
  color: var(--text-primary);
  text-decoration: none;
  transition: color 0.2s ease;
}

.header-link:hover {
  color: var(--text-accent);
}

.subtitle {
  color: var(--text-secondary);
  font-size: 1rem;
  margin: 0;
}

.theme-toggle {
  min-width: 3rem;
  height: 3rem;
}

.info-banner {
  background-color: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
  padding: 0.75rem 0;
}

.banner-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.banner-text {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.info-link {
  color: var(--text-accent);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.875rem;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  transition: background-color 0.2s ease;
}

.info-link:hover {
  background-color: var(--bg-tertiary);
  text-decoration: underline;
}

.main {
  padding: 2rem 0;
  min-height: calc(100vh - 200px);
  flex: 1;
}

.footer {
  background-color: var(--bg-secondary);
  border-top: 1px solid var(--border-color);
  padding: 2rem 0;
  margin-top: auto;
}

.text-accent {
  color: var(--text-accent);
  text-decoration: none;
}

.text-accent:hover {
  text-decoration: underline;
}

.text-secondary {
  color: var(--text-secondary);
}

.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Accessibility Styles */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.skip-link {
  position: absolute;
  top: -40px;
  left: 6px;
  background-color: var(--text-accent);
  color: white;
  padding: 8px;
  text-decoration: none;
  border-radius: 0 0 8px 8px;
  z-index: 1000;
  transition: top 0.2s ease;
}

.skip-link:focus {
  top: 0;
}

/* Enhanced focus indicators */
.theme-toggle:focus-visible {
  outline: 2px solid var(--text-accent);
  outline-offset: 2px;
}

.header-link:focus-visible,
.info-link:focus-visible,
.text-accent:focus-visible {
  outline: 2px solid var(--text-accent);
  outline-offset: 2px;
  border-radius: 2px;
}

@media (max-width: 768px) {
  .header {
    padding: 1rem 0;
  }

  .banner-content {
    flex-direction: column;
    text-align: center;
    gap: 0.5rem;
  }

  .banner-text {
    font-size: 0.75rem;
  }

  .main {
    padding: 1rem 0;
  }
}
</style>