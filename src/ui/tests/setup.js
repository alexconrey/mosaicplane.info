// Test setup file for Vue component tests
import { config } from '@vue/test-utils'

// Mock router for testing
const mockRouter = {
  push: vi.fn(),
  replace: vi.fn(),
  go: vi.fn(),
  back: vi.fn(),
  forward: vi.fn(),
  currentRoute: {
    value: {
      path: '/',
      name: 'home',
      params: {},
      query: {}
    }
  }
}

// Mock router-link component
const RouterLinkStub = {
  template: '<a><slot /></a>',
  props: ['to']
}

// Global test configuration
config.global.mocks = {
  $router: mockRouter,
  $route: mockRouter.currentRoute.value
}

config.global.stubs = {
  'router-link': RouterLinkStub,
  'router-view': true
}

// Mock window.location for branding tests
Object.defineProperty(window, 'location', {
  value: {
    hostname: 'localhost',
    href: 'http://localhost:3000',
    protocol: 'http:',
    port: '3000'
  },
  writable: true
})

// Mock fetch for API calls
global.fetch = vi.fn()

// Mock ResizeObserver for components that use it
global.ResizeObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}))

// Mock IntersectionObserver
global.IntersectionObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}))

// Setup for CSS custom properties
document.documentElement.style.setProperty = vi.fn()