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

describe('Recent Component Updates', () => {
  let wrapper

  beforeEach(() => {
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

  describe('Navigation Button Order', () => {
    it('renders theme toggle button before menu button', () => {
      const headerControls = wrapper.find('.header-controls')
      const buttons = headerControls.findAll('button')
      
      expect(buttons).toHaveLength(2)
      expect(buttons[0].classes()).toContain('theme-toggle')
      expect(buttons[1].classes()).toContain('nav-toggle')
    })
  })

  describe('Navigation Dropdown', () => {
    it('initially hides the dropdown menu', () => {
      expect(wrapper.find('.nav-dropdown-content').exists()).toBe(false)
    })

    it('shows dropdown when nav button is clicked', async () => {
      const navToggle = wrapper.find('.nav-toggle')
      await navToggle.trigger('click')
      
      expect(wrapper.find('.nav-dropdown-content').exists()).toBe(true)
    })

    it('includes MOSAIC and About menu items', async () => {
      const navToggle = wrapper.find('.nav-toggle')
      await navToggle.trigger('click')
      
      const menuItems = wrapper.findAll('.nav-dropdown-item')
      expect(menuItems).toHaveLength(2)
      expect(menuItems[0].text()).toContain('MOSAIC Info')
      expect(menuItems[1].text()).toContain('About')
    })

    it('has proper accessibility attributes', () => {
      const navToggle = wrapper.find('.nav-toggle')
      expect(navToggle.attributes('aria-expanded')).toBe('false')
      expect(navToggle.attributes('aria-haspopup')).toBe('true')
      expect(navToggle.attributes('aria-label')).toBe('Open navigation menu')
    })
  })

  describe('Footer Layout', () => {
    it('has three-column footer layout', () => {
      const footerContent = wrapper.find('.footer-content')
      expect(footerContent.find('.footer-left').exists()).toBe(true)
      expect(footerContent.find('.footer-center').exists()).toBe(true)
      expect(footerContent.find('.footer-right').exists()).toBe(true)
    })

    it('maintains center content in footer', () => {
      const footerCenter = wrapper.find('.footer-center')
      expect(footerCenter.text()).toContain('Data based on FAA MOSAIC Final Rule (July 2025)')
      expect(footerCenter.text()).toContain('Legal Disclaimer')
    })

    it('footer left section is empty (no commit hash)', () => {
      const footerLeft = wrapper.find('.footer-left')
      expect(footerLeft.text().trim()).toBe('')
    })
  })

  describe('Theme Toggle Functionality', () => {
    it('displays correct theme toggle button text for light mode', () => {
      const themeToggle = wrapper.find('.theme-toggle')
      expect(themeToggle.find('[aria-hidden="true"]').text()).toBe('🌙')
      expect(themeToggle.find('.desktop-only').text()).toBe('Dark')
    })

    it('has correct accessibility labels', () => {
      const themeToggle = wrapper.find('.theme-toggle')
      expect(themeToggle.attributes('aria-label')).toBe('Switch to dark mode')
      expect(themeToggle.attributes('title')).toBe('Switch to dark mode')
    })
  })

  describe('MOSAIC Info Banner', () => {
    it('displays current MOSAIC regulation information', () => {
      const banner = wrapper.find('.info-banner')
      const bannerText = banner.find('.banner-text')
      
      expect(bannerText.text()).toContain('October 22, 2025')
      expect(bannerText.text()).toContain('≤61 knots stall speed')
      expect(bannerText.text()).toContain('≤59 knots, 1 passenger max')
    })

    it('has accessible More Info link', () => {
      const infoLink = wrapper.find('.info-link')
      expect(infoLink.exists()).toBe(true)
      expect(infoLink.attributes('aria-label')).toBe('Learn more about MOSAIC regulations')
    })
  })
})