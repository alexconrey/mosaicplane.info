import { ref, watch } from 'vue'

// Global theme state
const theme = ref(localStorage.getItem('theme') || 'light')

export function useTheme() {
  const toggleTheme = () => {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
  }

  // Watch for theme changes and update localStorage and document
  watch(theme, (newTheme) => {
    localStorage.setItem('theme', newTheme)
    document.documentElement.setAttribute('data-theme', newTheme)
  }, { immediate: true })

  return {
    theme,
    toggleTheme
  }
}