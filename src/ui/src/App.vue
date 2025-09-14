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
          <div class="header-controls">
            <button 
              @click="toggleTheme" 
              class="btn btn-secondary theme-toggle"
              :aria-label="`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`"
              :title="`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`"
            >
              <span aria-hidden="true">{{ theme === 'light' ? '🌙' : '☀️' }}</span>
              <span class="desktop-only">{{ theme === 'light' ? 'Dark' : 'Light' }}</span>
            </button>
            <nav class="nav-dropdown" @click="toggleNavDropdown" @blur="closeNavDropdown" tabindex="0" role="navigation" aria-label="Main navigation">
              <button
                class="btn btn-secondary nav-toggle"
                :aria-label="showNavDropdown ? 'Close navigation menu' : 'Open navigation menu'"
                :aria-expanded="showNavDropdown"
                aria-haspopup="true"
              >
                <span aria-hidden="true">☰</span>
                <span class="desktop-only">Menu</span>
              </button>
              <div
                v-if="showNavDropdown"
                class="nav-dropdown-content"
                role="menu"
                aria-label="Navigation menu"
              >
                <router-link
                  to="/manufacturers"
                  class="nav-dropdown-item"
                  role="menuitem"
                  @click="closeNavDropdown"
                >
                  🏭 Manufacturers
                </router-link>
                <router-link
                  to="/mosaic"
                  class="nav-dropdown-item"
                  role="menuitem"
                  @click="closeNavDropdown"
                >
                  📋 MOSAIC Info
                </router-link>
                <router-link
                  to="/about"
                  class="nav-dropdown-item"
                  role="menuitem"
                  @click="closeNavDropdown"
                >
                  ℹ️ About
                </router-link>
              </div>
            </nav>
          </div>
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
        <div class="footer-content">
          <div class="footer-left"></div>
          <div class="footer-center">
            <p class="text-secondary">
              Data based on FAA MOSAIC Final Rule (July 2025)
            </p>
            <p class="text-secondary">
              <small>
                API: <a href="/api/docs/" target="_blank" rel="noopener" class="text-accent" aria-label="API Documentation (opens in new tab)">Documentation</a> |
                <router-link to="/about#legal-disclaimer" class="text-accent">Legal Disclaimer</router-link>
              </small>
            </p>
          </div>
          <div class="footer-right"></div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { onMounted, provide, ref } from 'vue'
import { useTheme } from './composables/useTheme'
import { useBranding } from './composables/useBranding'

const { theme, toggleTheme } = useTheme()
const { siteName, siteTagline, showAllAircraft, isMosaicPlane } = useBranding()

// Navigation dropdown state
const showNavDropdown = ref(false)


const toggleNavDropdown = () => {
  showNavDropdown.value = !showNavDropdown.value
}

const closeNavDropdown = () => {
  showNavDropdown.value = false
}

// Provide theme and branding to child components
provide('theme', theme)
provide('branding', { siteName, siteTagline, showAllAircraft, isMosaicPlane })

onMounted(() => {
  // Set initial theme on document
  document.documentElement.setAttribute('data-theme', theme.value)
  
  // Close dropdown when clicking outside
  document.addEventListener('click', (event) => {
    if (!event.target.closest('nav.nav-dropdown')) {
      closeNavDropdown()
    }
  })
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

.header-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.nav-dropdown {
  position: relative;
  display: inline-block;
}

.nav-toggle {
  min-width: 3rem;
  height: 3rem;
}

.nav-dropdown-content {
  position: absolute;
  right: 0;
  top: calc(100% + 0.5rem);
  background-color: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  min-width: 180px;
  z-index: 200;
  animation: slideDown 0.2s ease-out;
}

.nav-dropdown-item {
  display: block;
  padding: 0.75rem 1rem;
  color: var(--text-primary);
  text-decoration: none;
  border-radius: 0.25rem;
  transition: background-color 0.2s ease;
}

.nav-dropdown-item:hover {
  background-color: var(--bg-tertiary);
}

.nav-dropdown-item:first-child {
  border-radius: 0.5rem 0.5rem 0.25rem 0.25rem;
}

.nav-dropdown-item:last-child {
  border-radius: 0.25rem 0.25rem 0.5rem 0.5rem;
}

.theme-toggle {
  min-width: 3rem;
  height: 3rem;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.footer-left,
.footer-right {
  flex: 0 0 auto;
  min-width: 120px;
}

.footer-center {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  text-align: center;
}

.commit-info {
  font-family: 'Courier New', Consolas, monospace;
  opacity: 0.7;
  font-size: 0.875rem;
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
.theme-toggle:focus-visible,
.nav-toggle:focus-visible {
  outline: 2px solid var(--text-accent);
  outline-offset: 2px;
}

.nav-dropdown:focus-visible {
  outline: 2px solid var(--text-accent);
  outline-offset: 2px;
  border-radius: 0.5rem;
}

.nav-dropdown-item:focus-visible {
  outline: 2px solid var(--text-accent);
  outline-offset: 2px;
  background-color: var(--bg-tertiary);
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

  .header-controls {
    gap: 0.25rem;
  }

  .nav-dropdown-content {
    right: -0.5rem;
    min-width: 160px;
  }

  .nav-dropdown-item {
    padding: 0.5rem 0.75rem;
    font-size: 0.875rem;
  }

  .banner-content {
    flex-direction: column;
    text-align: center;
    gap: 0.5rem;
  }

  .banner-text {
    font-size: 0.875rem;
  }

  .main {
    padding: 1rem 0;
  }

  .footer-content {
    flex-direction: column;
    text-align: center;
  }

  .footer-left,
  .footer-right {
    min-width: auto;
  }

  .commit-info {
    font-size: 0.875rem;
  }
}
</style>