// API utility for making requests with the correct base URL
// Runtime environment detection - handles various deployment scenarios
function getApiBase() {
  const hostname = window.location.hostname
  const port = window.location.port
  
  // Local development
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return '/api'
  }
  
  // Cloudflare Workers deployment
  if (hostname.includes('workers.dev')) {
    return 'https://api.mosaicplane.info'
  }
  
  // Production deployment (custom domain)
  if (hostname === 'mosaicplane.info' || hostname === 'www.mosaicplane.info') {
    return 'https://api.mosaicplane.info'
  }
  
  // Docker production container (nginx proxy)
  if (port === '8000' || port === '') {
    return '/api'
  }
  
  // Fallback to relative API path for any other scenario
  return '/api'
}

const API_BASE = getApiBase()

/**
 * Make an API request with the correct base URL
 * @param {string} endpoint - The API endpoint (e.g., '/v1/aircraft/')
 * @param {object} options - Fetch options
 * @returns {Promise<Response>}
 */
export const apiRequest = (endpoint, options = {}) => {
  const url = `${API_BASE}${endpoint}`
  console.log(`API Request: ${url}`) // Debug log to see where requests are going
  return fetch(url, options)
}

/**
 * Get the full API URL for a given endpoint
 * @param {string} endpoint - The API endpoint (e.g., '/v1/aircraft/')
 * @returns {string}
 */
export const getApiUrl = (endpoint) => {
  return `${API_BASE}${endpoint}`
}

export default {
  apiRequest,
  getApiUrl
}