import { describe, it, expect, beforeEach, vi } from 'vitest'

describe('useTheme (functional tests)', () => {
  beforeEach(() => {
    // Clear localStorage before each test
    localStorage.clear()
    vi.clearAllMocks()
  })

  it('should have a theme toggle function', async () => {
    const { useTheme } = await import('@/composables/useTheme')
    const { toggleTheme, theme } = useTheme()
    
    expect(typeof toggleTheme).toBe('function')
    expect(theme.value).toBeDefined()
    expect(['light', 'dark']).toContain(theme.value)
  })

  it('should toggle between light and dark themes', async () => {
    const { useTheme } = await import('@/composables/useTheme')
    const { toggleTheme, theme } = useTheme()
    
    const initialTheme = theme.value
    toggleTheme()
    const newTheme = theme.value
    
    expect(newTheme).not.toBe(initialTheme)
    expect(['light', 'dark']).toContain(newTheme)
    
    // Toggle back
    toggleTheme()
    expect(theme.value).toBe(initialTheme)
  })

  it('should persist theme to localStorage', async () => {
    const { useTheme } = await import('@/composables/useTheme')
    const { toggleTheme, theme } = useTheme()
    
    // Clear any existing theme
    localStorage.removeItem('theme')
    
    toggleTheme()
    
    // Wait for Vue's reactivity to update localStorage
    await new Promise(resolve => setTimeout(resolve, 10))
    
    // Should have stored the current theme value
    const storedTheme = localStorage.getItem('theme')
    expect(storedTheme).toBe(theme.value)
    expect(['light', 'dark']).toContain(storedTheme)
  })
})