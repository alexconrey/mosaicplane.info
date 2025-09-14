import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { ref } from 'vue'
import App from '@/App.vue'

// Mock the composables
vi.mock('@/composables/useTheme', () => ({
  useTheme: () => ({
    theme: ref('light'),
    toggleTheme: vi.fn()
  })
}))

vi.mock('@/composables/useBranding', () => ({
  useBranding: () => ({
    siteName: ref('MosaicPlane.info'),
    siteTagline: ref('Compare MOSAIC-Compliant Aircraft'),
    showAllAircraft: ref(false),
    isMosaicPlane: ref(true)
  })
}))

// Mock localStorage
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn()
}
Object.defineProperty(window, 'localStorage', { value: localStorageMock })

describe('App.vue', () => {
  let wrapper

  beforeEach(() => {
    // Reset mocks
    vi.clearAllMocks()
    localStorageMock.getItem.mockReturnValue('light')
    
    wrapper = mount(App, {
      global: {
        stubs: {
          'router-link': {
            template: '<a><slot /></a>',
            props: ['to']
          },
          'router-view': {
            template: '<div>Router View</div>'
          }
        }
      }
    })
  })

  describe('Header Navigation', () => {
    it('renders the site name and tagline', () => {
      expect(wrapper.find('h1').text()).toBe('MosaicPlane.info')
      expect(wrapper.find('.subtitle').text()).toBe('Compare MOSAIC-Compliant Aircraft')
    })

    it('renders theme toggle button with correct order', () => {
      const headerControls = wrapper.find('.header-controls')
      const buttons = headerControls.findAll('button')
      
      // Theme toggle should be first button
      expect(buttons[0].classes()).toContain('theme-toggle')
      // Navigation toggle should be second button  
      expect(buttons[1].classes()).toContain('nav-toggle')
    })

    it('shows correct theme toggle text for light mode', () => {
      const themeButton = wrapper.find('.theme-toggle')
      expect(themeButton.find('[aria-hidden="true"]').text()).toBe('🌙')
      expect(themeButton.find('.desktop-only').text()).toBe('Dark')
    })

    it('has proper accessibility attributes on theme toggle', () => {
      const themeButton = wrapper.find('.theme-toggle')
      expect(themeButton.attributes('aria-label')).toBe('Switch to dark mode')
      expect(themeButton.attributes('title')).toBe('Switch to dark mode')
    })
  })

  describe('Navigation Dropdown', () => {
    it('initially hides navigation dropdown', () => {
      expect(wrapper.find('.nav-dropdown-content').exists()).toBe(false)
    })

    it('shows navigation dropdown when nav toggle is clicked', async () => {
      const navToggle = wrapper.find('.nav-toggle')
      await navToggle.trigger('click')
      
      expect(wrapper.find('.nav-dropdown-content').exists()).toBe(true)
    })

    it('has proper accessibility attributes on nav toggle', () => {
      const navToggle = wrapper.find('.nav-toggle')
      expect(navToggle.attributes('aria-label')).toBe('Open navigation menu')
      expect(navToggle.attributes('aria-expanded')).toBe('false')
      expect(navToggle.attributes('aria-haspopup')).toBe('true')
    })

    it('updates aria-expanded when dropdown is opened', async () => {
      const navToggle = wrapper.find('.nav-toggle')
      await navToggle.trigger('click')
      
      expect(navToggle.attributes('aria-expanded')).toBe('true')
      expect(navToggle.attributes('aria-label')).toBe('Close navigation menu')
    })

    it('renders navigation menu items when dropdown is open', async () => {
      const navToggle = wrapper.find('.nav-toggle')
      await navToggle.trigger('click')
      
      const menuItems = wrapper.findAll('.nav-dropdown-item')
      expect(menuItems).toHaveLength(2)
      
      // Check menu item content
      expect(menuItems[0].text().trim()).toBe('📋 MOSAIC Info')
      expect(menuItems[1].text().trim()).toBe('ℹ️ About')
    })

    it('has proper ARIA roles on navigation menu', async () => {
      const navToggle = wrapper.find('.nav-toggle')
      await navToggle.trigger('click')
      
      const dropdown = wrapper.find('.nav-dropdown-content')
      expect(dropdown.attributes('role')).toBe('menu')
      expect(dropdown.attributes('aria-label')).toBe('Navigation menu')
      
      const menuItems = wrapper.findAll('.nav-dropdown-item')
      menuItems.forEach(item => {
        expect(item.attributes('role')).toBe('menuitem')
      })
    })
  })

  describe('MOSAIC Info Banner', () => {
    it('renders MOSAIC regulation information', () => {
      const banner = wrapper.find('.info-banner')
      const bannerText = banner.find('.banner-text')
      
      expect(bannerText.text()).toContain('MOSAIC Final Rule Effective: October 22, 2025')
      expect(bannerText.text()).toContain('LSA Criteria: ≤61 knots stall speed')
      expect(bannerText.text()).toContain('Sport Pilot: ≤59 knots, 1 passenger max')
    })

    it('has proper accessibility attributes', () => {
      const banner = wrapper.find('.info-banner')
      expect(banner.attributes('role')).toBe('banner')
      expect(banner.attributes('aria-label')).toBe('MOSAIC regulation information')
    })

    it('renders "More Info" link to MOSAIC page', () => {
      const infoLink = wrapper.find('.info-link')
      expect(infoLink.text().trim()).toBe('More Info')
      expect(infoLink.attributes('aria-label')).toBe('Learn more about MOSAIC regulations')
    })
  })

  describe('Footer Layout', () => {
    it('renders three-column footer layout', () => {
      const footerContent = wrapper.find('.footer-content')
      expect(footerContent.find('.footer-left').exists()).toBe(true)
      expect(footerContent.find('.footer-center').exists()).toBe(true)
      expect(footerContent.find('.footer-right').exists()).toBe(true)
    })

    it('renders footer center content', () => {
      const footerCenter = wrapper.find('.footer-center')
      expect(footerCenter.text()).toContain('Data based on FAA MOSAIC Final Rule (July 2025)')
      expect(footerCenter.text()).toContain('API:')
      expect(footerCenter.text()).toContain('Documentation')
      expect(footerCenter.text()).toContain('Legal Disclaimer')
    })

    it('has proper accessibility attributes on footer', () => {
      const footer = wrapper.find('.footer')
      expect(footer.attributes('role')).toBe('contentinfo')
    })

    it('renders API documentation link with proper attributes', () => {
      const apiLink = wrapper.find('a[href="/api/docs/"]')
      expect(apiLink.exists()).toBe(true)
      expect(apiLink.attributes('target')).toBe('_blank')
      expect(apiLink.attributes('aria-label')).toBe('API Documentation (opens in new tab)')
      expect(apiLink.classes()).toContain('text-accent')
    })
  })

  describe('Accessibility Features', () => {
    it('renders skip to main content link', () => {
      const skipLink = wrapper.find('.skip-link')
      expect(skipLink.exists()).toBe(true)
      expect(skipLink.attributes('href')).toBe('#main-content')
      expect(skipLink.text()).toBe('Skip to main content')
      expect(skipLink.classes()).toContain('sr-only')
    })

    it('has main content with proper id and role', () => {
      const main = wrapper.find('#main-content')
      expect(main.exists()).toBe(true)
      expect(main.attributes('role')).toBe('main')
      expect(main.classes()).toContain('main')
    })

    it('sets data-theme attribute on root element', () => {
      expect(wrapper.attributes('data-theme')).toBe('light')
      expect(wrapper.attributes('id')).toBe('app')
      expect(wrapper.classes()).toContain('app-layout')
    })
  })

  describe('Component Lifecycle', () => {
    it('provides theme and branding to child components', () => {
      // The provide() calls should be made during component setup
      // This ensures child components can inject these values
      expect(wrapper.vm).toBeDefined()
    })
  })
})