<template>
  <div class="manufacturer-detail">
    <div class="container mx-auto px-4 py-8">
      <!-- Loading state -->
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
        <p class="mt-4 text-secondary">Loading manufacturer details...</p>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="text-center py-12">
        <div class="text-error mb-4">
          <svg class="w-16 h-16 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.99-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
          </svg>
        </div>
        <h2 class="text-xl font-semibold mb-2">Manufacturer Not Found</h2>
        <p class="text-secondary mb-4">{{ error }}</p>
        <router-link to="/manufacturers" class="btn btn-primary">
          Back to Manufacturers
        </router-link>
      </div>

      <!-- Manufacturer content -->
      <div v-else-if="manufacturer">
        <!-- Breadcrumb -->
        <nav class="breadcrumb mb-6" aria-label="Breadcrumb">
          <div class="breadcrumb-container">
            <router-link to="/manufacturers" class="breadcrumb-item breadcrumb-link">
              <svg class="breadcrumb-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-4m-5 0H3m0 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1"></path>
              </svg>
              <span>Manufacturers</span>
            </router-link>
            <div class="breadcrumb-separator">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
              </svg>
            </div>
            <div class="breadcrumb-item breadcrumb-current" aria-current="page">
              <svg class="breadcrumb-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
              </svg>
              <span>{{ manufacturer.name }}</span>
            </div>
          </div>
        </nav>

        <!-- Manufacturer header -->
        <div class="manufacturer-header mb-8">
          <div class="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-6">
            <div class="flex-1">
              <h1 class="text-3xl font-bold mb-2">{{ manufacturer.name }}</h1>
              <div class="flex items-center gap-2 mb-4">
                <span
                  :class="[
                    'px-3 py-1 rounded-full text-sm font-medium',
                    manufacturer.is_currently_manufacturing
                      ? 'bg-success/10 text-success'
                      : 'bg-gray-500/10 text-gray-600'
                  ]"
                >
                  {{ manufacturer.is_currently_manufacturing ? 'Currently Manufacturing' : 'Historic Manufacturer' }}
                </span>
              </div>
              <p class="text-secondary text-lg">
                {{ manufacturer.is_currently_manufacturing 
                   ? `Browse current aircraft models from ${manufacturer.name}` 
                   : `Historic aircraft models from ${manufacturer.name}` }}
              </p>
            </div>
            
            <!-- Logo area -->
            <div class="logo-area">
              <!-- Display actual logo if available -->
              <div v-if="manufacturer.logo" class="logo-container">
                <img 
                  :src="manufacturer.logo" 
                  :alt="`${manufacturer.name} logo`"
                  class="manufacturer-logo"
                  @error="onLogoError"
                />
              </div>
              
              <!-- Fallback placeholder if no logo -->
              <div v-else class="logo-placeholder">
                <div class="logo-content">
                  <svg class="logo-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                  </svg>
                  <div class="logo-text">
                    <p class="logo-title">{{ manufacturer.name }}</p>
                    <p class="logo-subtitle">Logo</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Aircraft Table -->
        <div v-if="!aircraftLoading && aircraft.length > 0" class="aircraft-section">
          <ManufacturerAircraftTable 
            :aircraft="aircraft"
            :manufacturer-name="manufacturer.name"
          />
        </div>

        <!-- Aircraft loading state -->
        <div v-else-if="aircraftLoading" class="text-center py-8">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div>
          <p class="mt-2 text-secondary">Loading aircraft...</p>
        </div>

        <!-- No aircraft state -->
        <div v-else class="no-aircraft text-center py-12">
          <div class="text-secondary mb-4">
            <svg class="w-16 h-16 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.29.82-5.877 2.172M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.875a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0z"></path>
            </svg>
          </div>
          <h2 class="text-xl font-semibold mb-2">No Aircraft Found</h2>
          <p class="text-secondary mb-4">
            No aircraft models are currently listed for {{ manufacturer.name }}.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { apiRequest } from '../utils/api.js'
import ManufacturerAircraftTable from '../components/ManufacturerAircraftTable.vue'

const route = useRoute()
const manufacturer = ref(null)
const aircraft = ref([])
const loading = ref(true)
const aircraftLoading = ref(false)
const error = ref(null)

const fetchManufacturer = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await apiRequest(`/v1/manufacturers/${route.params.id}/`)
    const data = await response.json()
    manufacturer.value = data
    
    // Fetch aircraft for this manufacturer
    await fetchAircraft()
  } catch (err) {
    error.value = 'Manufacturer not found or unavailable.'
    console.error('Error fetching manufacturer:', err)
  } finally {
    loading.value = false
  }
}

const fetchAircraft = async () => {
  aircraftLoading.value = true
  
  try {
    const response = await apiRequest(`/v1/manufacturers/${route.params.id}/aircraft/`)
    const data = await response.json()
    aircraft.value = data
  } catch (err) {
    console.error('Error fetching aircraft:', err)
    aircraft.value = []
  } finally {
    aircraftLoading.value = false
  }
}

const onLogoError = (event) => {
  console.warn('Failed to load manufacturer logo:', event.target.src)
  // Hide the logo on error by setting manufacturer.logo to null
  if (manufacturer.value) {
    manufacturer.value.logo = null
  }
}

onMounted(() => {
  fetchManufacturer()
})
</script>

<style scoped>
.manufacturer-header {
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 2rem;
}

.logo-area {
  flex-shrink: 0;
}

.logo-container {
  width: 200px;
  height: 120px;
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  background: var(--bg-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.manufacturer-logo {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 0.25rem;
}

.logo-placeholder {
  width: 200px;
  height: 120px;
  border: 2px dashed var(--border-color);
  border-radius: 0.5rem;
  background: var(--bg-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.logo-placeholder:hover {
  border-color: var(--primary);
  background: var(--bg-tertiary);
}

.logo-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  text-align: center;
}

.logo-icon {
  width: 2rem;
  height: 2rem;
  color: var(--text-secondary);
}

.logo-text {
  color: var(--text-secondary);
}

.logo-title {
  font-size: 0.875rem;
  font-weight: 500;
  margin: 0;
}

.logo-subtitle {
  font-size: 0.875rem;
  margin: 0;
}

.aircraft-card {
  text-decoration: none;
  color: inherit;
}

.card {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 0.75rem;
  padding: 1.5rem;
  transition: all 0.3s ease;
  height: 100%;
}

.card:hover {
  border-color: var(--primary);
  box-shadow: 0 10px 25px -5px var(--shadow), 0 4px 6px -2px var(--shadow);
}

.specs-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}

.spec {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.spec-label {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.spec-value {
  color: var(--text-primary);
  font-weight: 500;
  font-size: 0.875rem;
}

.badges {
  margin-top: auto;
}

.badge {
  padding: 0.25rem 0.5rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.badge-success {
  background-color: var(--success-alpha);
  color: var(--success);
}

.badge-primary {
  background-color: var(--primary-alpha);
  color: var(--primary);
}

.badge-warning {
  background-color: var(--warning-alpha);
  color: var(--warning);
}

.badge-info {
  background-color: var(--info-alpha);
  color: var(--info);
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 0.375rem;
  font-weight: 500;
  transition: all 0.2s ease;
  border: 1px solid transparent;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.btn-primary {
  background-color: var(--primary);
  color: white;
}

.btn-primary:hover {
  background-color: var(--primary-dark);
}

.breadcrumb {
  margin-bottom: 1.5rem;
}

.breadcrumb-container {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.breadcrumb-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.breadcrumb-link {
  color: var(--text-secondary);
  text-decoration: none;
  padding: 0.375rem 0.75rem;
  border-radius: 0.5rem;
  transition: all 0.2s ease;
  background: transparent;
  border: 1px solid transparent;
}

.breadcrumb-link:hover {
  color: var(--primary);
  background: var(--bg-primary);
  border-color: var(--border-color);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.breadcrumb-current {
  color: var(--primary);
  background: var(--primary-alpha);
  padding: 0.375rem 0.75rem;
  border-radius: 0.5rem;
  border: 1px solid var(--primary);
}

.breadcrumb-icon {
  width: 1rem;
  height: 1rem;
  flex-shrink: 0;
}

.breadcrumb-separator {
  color: var(--text-secondary);
  display: flex;
  align-items: center;
}

.breadcrumb-separator svg {
  width: 0.875rem;
  height: 0.875rem;
}

/* Responsive adjustments */
@media (max-width: 1024px) {
  .manufacturer-header .flex {
    flex-direction: column;
    align-items: stretch;
  }
  
  .logo-area {
    align-self: center;
  }
  
  .logo-container {
    width: 150px;
    height: 90px;
  }
  
  .logo-placeholder {
    width: 150px;
    height: 90px;
  }
}

@media (max-width: 768px) {
  .breadcrumb-container {
    padding: 0.5rem 0.75rem;
    gap: 0.5rem;
  }
  
  .breadcrumb-item {
    font-size: 0.8rem;
    gap: 0.375rem;
  }
  
  .breadcrumb-link,
  .breadcrumb-current {
    padding: 0.25rem 0.5rem;
  }
  
  .breadcrumb-icon {
    width: 0.875rem;
    height: 0.875rem;
  }
  
  .logo-container {
    width: 120px;
    height: 75px;
  }
  
  .logo-placeholder {
    width: 120px;
    height: 75px;
  }
  
  .logo-icon {
    width: 1.5rem;
    height: 1.5rem;
  }
  
  .logo-title {
    font-size: 0.8rem;
  }
  
  .logo-subtitle {
    font-size: 0.875rem;
  }
}
</style>