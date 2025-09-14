<template>
  <div class="manufacturers">
    <div class="container mx-auto px-4 py-8">
      <!-- Page Header -->
      <div class="page-header mb-8">
        <h1 class="text-3xl font-bold mb-4">Aircraft Manufacturers</h1>
        <p class="text-secondary text-lg">
          Browse all aircraft manufacturers in our MOSAIC aircraft database. Click on any manufacturer to view their aircraft models.
        </p>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
        <p class="mt-4 text-secondary">Loading manufacturers...</p>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="text-center py-12">
        <div class="text-error mb-4">
          <svg class="w-16 h-16 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.99-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
          </svg>
        </div>
        <h2 class="text-xl font-semibold mb-2">Failed to Load Manufacturers</h2>
        <p class="text-secondary mb-4">{{ error }}</p>
        <button @click="fetchManufacturers" class="btn btn-primary">
          Try Again
        </button>
      </div>

      <!-- Manufacturers grid -->
      <div v-else class="manufacturers-grid">
        <!-- Search and filters -->
        <div class="filters mb-6">
          <div class="flex flex-col sm:flex-row gap-4">
            <div class="flex-1">
              <label for="manufacturer-search" class="sr-only">Search manufacturers</label>
              <input
                id="manufacturer-search"
                v-model="searchTerm"
                type="text"
                placeholder="Search manufacturers..."
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
              />
            </div>
            <div class="flex gap-2">
              <button
                @click="filterByStatus('all')"
                :class="['btn', statusFilter === 'all' ? 'btn-primary' : 'btn-secondary']"
              >
                All ({{ manufacturers.length }})
              </button>
              <button
                @click="filterByStatus('active')"
                :class="['btn', statusFilter === 'active' ? 'btn-primary' : 'btn-secondary']"
              >
                Active ({{ activeCount }})
              </button>
              <button
                @click="filterByStatus('inactive')"
                :class="['btn', statusFilter === 'inactive' ? 'btn-primary' : 'btn-secondary']"
              >
                Historic ({{ inactiveCount }})
              </button>
            </div>
          </div>
        </div>

        <!-- Manufacturers list -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <router-link
            v-for="manufacturer in filteredManufacturers"
            :key="manufacturer.id"
            :to="`/manufacturers/${manufacturer.id}`"
            class="manufacturer-card group"
          >
            <div class="card hover:shadow-lg transition-all duration-300 group-hover:transform group-hover:-translate-y-1">
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <h3 class="text-xl font-semibold mb-2 group-hover:text-primary transition-colors">
                    {{ manufacturer.name }}
                  </h3>
                  <div class="flex items-center gap-2 mb-3">
                    <span
                      :class="[
                        'px-2 py-1 rounded-full text-xs font-medium',
                        manufacturer.is_currently_manufacturing
                          ? 'bg-success/10 text-success'
                          : 'bg-gray-500/10 text-gray-600'
                      ]"
                    >
                      {{ manufacturer.is_currently_manufacturing ? 'Currently Manufacturing' : 'Historic' }}
                    </span>
                  </div>
                  <p class="text-sm text-secondary">
                    Click to view aircraft models from {{ manufacturer.name }}
                  </p>
                </div>
                <div class="ml-4">
                  <svg 
                    class="w-6 h-6 text-secondary group-hover:text-primary transition-colors" 
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                  </svg>
                </div>
              </div>
            </div>
          </router-link>
        </div>

        <!-- Empty state -->
        <div v-if="filteredManufacturers.length === 0" class="text-center py-12">
          <div class="text-secondary mb-4">
            <svg class="w-16 h-16 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
          </div>
          <h2 class="text-xl font-semibold mb-2">No manufacturers found</h2>
          <p class="text-secondary">
            {{ searchTerm ? `No manufacturers match "${searchTerm}"` : 'No manufacturers match your current filters' }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { apiRequest } from '../utils/api.js'

const manufacturers = ref([])
const loading = ref(true)
const error = ref(null)
const searchTerm = ref('')
const statusFilter = ref('all')

const fetchManufacturers = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await apiRequest('/v1/manufacturers/')
    const data = await response.json()
    manufacturers.value = data.results || data
  } catch (err) {
    error.value = 'Unable to load manufacturers. Please check your connection and try again.'
    console.error('Error fetching manufacturers:', err)
  } finally {
    loading.value = false
  }
}

const filteredManufacturers = computed(() => {
  let filtered = manufacturers.value

  // Filter by search term
  if (searchTerm.value) {
    const search = searchTerm.value.toLowerCase()
    filtered = filtered.filter(m => 
      m.name.toLowerCase().includes(search)
    )
  }

  // Filter by status
  if (statusFilter.value === 'active') {
    filtered = filtered.filter(m => m.is_currently_manufacturing)
  } else if (statusFilter.value === 'inactive') {
    filtered = filtered.filter(m => !m.is_currently_manufacturing)
  }

  return filtered
})

const activeCount = computed(() => 
  manufacturers.value.filter(m => m.is_currently_manufacturing).length
)

const inactiveCount = computed(() => 
  manufacturers.value.filter(m => !m.is_currently_manufacturing).length
)

const filterByStatus = (status) => {
  statusFilter.value = status
}

onMounted(() => {
  fetchManufacturers()
})
</script>

<style scoped>
.page-header {
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 2rem;
}

.manufacturer-card {
  text-decoration: none;
  color: inherit;
}

.card {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 0.75rem;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.card:hover {
  border-color: var(--primary);
  box-shadow: 0 10px 25px -5px var(--shadow), 0 4px 6px -2px var(--shadow);
}

.btn {
  px: 1rem;
  py: 0.5rem;
  rounded: 0.375rem;
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

.btn-secondary {
  background-color: var(--bg-secondary);
  color: var(--text-primary);
  border-color: var(--border-color);
}

.btn-secondary:hover {
  background-color: var(--bg-tertiary);
  border-color: var(--primary);
}

.filters {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  padding: 1rem;
}

.filters input {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
}

.filters input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 2px var(--primary-alpha);
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .filters .flex {
    flex-direction: column;
    gap: 1rem;
  }
  
  .filters .flex.gap-2 {
    flex-direction: row;
    gap: 0.5rem;
  }
  
  .btn {
    font-size: 0.875rem;
    padding: 0.375rem 0.75rem;
  }
}
</style>