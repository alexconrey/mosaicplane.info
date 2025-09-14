// Simple API service for the application
const API_BASE_URL = typeof __API_BASE_URL__ !== 'undefined' ? __API_BASE_URL__ : '/api'

// Fetch aircraft data from API
export const fetchAircraft = async (filters = {}) => {
  const params = new URLSearchParams()
  
  Object.entries(filters).forEach(([key, value]) => {
    if (value !== null && value !== undefined && value !== '') {
      if (Array.isArray(value)) {
        value.forEach(v => params.append(key, v))
      } else {
        params.append(key, value)
      }
    }
  })
  
  const url = `${API_BASE_URL}/v1/aircraft/?${params}`
  const response = await fetch(url)
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }
  
  return await response.json()
}

// Fetch manufacturers data from API
export const fetchManufacturers = async () => {
  const url = `${API_BASE_URL}/v1/manufacturers/`
  const response = await fetch(url)
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }
  
  return await response.json()
}

// Fetch single aircraft by ID
export const fetchAircraftById = async (id) => {
  const url = `${API_BASE_URL}/v1/aircraft/${id}/`
  const response = await fetch(url)
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }
  
  return await response.json()
}

export default {
  fetchAircraft,
  fetchManufacturers,
  fetchAircraftById
}