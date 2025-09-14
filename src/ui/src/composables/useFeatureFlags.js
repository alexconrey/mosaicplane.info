import { ref, computed } from 'vue'
import { apiRequest } from '../utils/api.js'

// Global feature flags state
const featureFlags = ref({})
const loading = ref(false)
const error = ref(null)

export function useFeatureFlags() {
  /**
   * Fetch feature flags from API - always fresh data
   */
  const fetchFeatureFlags = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await apiRequest('/v1/feature-flags/')

      if (!response.ok) {
        throw new Error(`Failed to fetch feature flags: ${response.status}`)
      }

      const data = await response.json()
      featureFlags.value = data

      console.log('Feature flags loaded:', data)
      return data

    } catch (err) {
      console.error('Error fetching feature flags:', err)
      error.value = err.message

      // Return empty object as fallback - all features will be disabled
      return {}

    } finally {
      loading.value = false
    }
  }

  /**
   * Check if a feature is enabled
   */
  const isFeatureEnabled = (featureKey) => {
    return computed(() => {
      return featureFlags.value[featureKey] === true
    })
  }

  /**
   * Get multiple feature flags as computed properties
   */
  const getFeatures = (...featureKeys) => {
    const features = {}
    featureKeys.forEach(key => {
      features[key] = isFeatureEnabled(key)
    })
    return features
  }

  /**
   * Initialize feature flags - call this in app setup
   */
  const initializeFeatureFlags = async () => {
    await fetchFeatureFlags()
  }

  /**
   * Refresh feature flags (always fetches fresh data)
   */
  const refreshFeatureFlags = async () => {
    await fetchFeatureFlags()
  }

  return {
    // State
    featureFlags: computed(() => featureFlags.value),
    loading: computed(() => loading.value),
    error: computed(() => error.value),

    // Methods
    fetchFeatureFlags,
    isFeatureEnabled,
    getFeatures,
    initializeFeatureFlags,
    refreshFeatureFlags
  }
}