<template>
  <div class="manufacturer-aircraft-table">
    <!-- Header -->
    <div class="table-header mb-6">
      <h2 class="text-2xl font-bold mb-2">Aircraft Models</h2>
      <div class="flex items-center justify-between flex-wrap gap-4">
        <p class="text-secondary">
          {{ aircraft.length }} aircraft model{{ aircraft.length === 1 ? '' : 's' }} from {{ manufacturerName }}
        </p>
        <div class="table-controls">
          <!-- Search -->
          <div class="search-control">
            <input
              v-model="searchQuery"
              type="text"
              class="form-control"
              placeholder="Search models..."
              aria-label="Search aircraft models"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="table-container">
      <table class="table" role="table" aria-label="Aircraft models table">
        <thead>
          <tr>
            <th scope="col" class="sortable" @click="sortBy('model')"
                :aria-sort="getSortAriaAttribute('model')"
                tabindex="0"
                @keydown.enter="sortBy('model')"
            >
              Model {{ getSortIcon('model') }}
            </th>
            <th scope="col" class="desktop-only sortable" @click="sortBy('clean_stall_speed')"
                :aria-sort="getSortAriaAttribute('clean_stall_speed')"
                tabindex="0"
                @keydown.enter="sortBy('clean_stall_speed')"
            >
              Stall Speed {{ getSortIcon('clean_stall_speed') }}
            </th>
            <th scope="col" class="desktop-only sortable" @click="sortBy('cruise_speed')"
                :aria-sort="getSortAriaAttribute('cruise_speed')"
                tabindex="0"
                @keydown.enter="sortBy('cruise_speed')"
            >
              Cruise Speed {{ getSortIcon('cruise_speed') }}
            </th>
            <th scope="col" class="desktop-only sortable" @click="sortBy('top_speed')"
                :aria-sort="getSortAriaAttribute('top_speed')"
                tabindex="0"
                @keydown.enter="sortBy('top_speed')"
            >
              Max Speed {{ getSortIcon('top_speed') }}
            </th>
            <th scope="col" class="desktop-only sortable" @click="sortBy('seating_capacity')"
                :aria-sort="getSortAriaAttribute('seating_capacity')"
                tabindex="0"
                @keydown.enter="sortBy('seating_capacity')"
            >
              Seats {{ getSortIcon('seating_capacity') }}
            </th>
            <th scope="col" class="desktop-only sortable" @click="sortBy('certification_date')"
                :aria-sort="getSortAriaAttribute('certification_date')"
                tabindex="0"
                @keydown.enter="sortBy('certification_date')"
            >
              Year {{ getSortIcon('certification_date') }}
            </th>
            <th scope="col">Eligibility</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="plane in sortedAircraft"
            :key="plane.id"
            class="table-row"
            @click="$router.push(`/aircraft/${plane.id}`)"
          >
            <td class="aircraft-info">
              <div class="aircraft-name">
                <router-link 
                  :to="`/aircraft/${plane.id}`" 
                  class="aircraft-link"
                >
                  {{ plane.model }}
                </router-link>
              </div>
              <!-- Mobile-only specs -->
              <div class="mobile-only mobile-specs">
                <span class="mobile-spec">{{ plane.clean_stall_speed }}kt stall</span>
                <span v-if="plane.cruise_speed" class="mobile-spec">{{ plane.cruise_speed }}kt cruise</span>
                <span class="mobile-spec">{{ plane.top_speed }}kt max</span>
                <span class="mobile-spec">{{ plane.seating_capacity }} seats</span>
                <span v-if="plane.vx_speed" class="mobile-spec">{{ plane.vx_speed }}kt Vx</span>
                <span v-if="plane.vy_speed" class="mobile-spec">{{ plane.vy_speed }}kt Vy</span>
              </div>
            </td>
            <td class="desktop-only">
              <span class="speed-value">{{ plane.clean_stall_speed }}kt</span>
            </td>
            <td class="desktop-only">
              <span class="speed-value">{{ plane.cruise_speed ? `${plane.cruise_speed}kt` : 'N/A' }}</span>
            </td>
            <td class="desktop-only">
              <span class="speed-value">{{ plane.top_speed }}kt</span>
            </td>
            <td class="desktop-only">
              {{ plane.seating_capacity }}
            </td>
            <td class="desktop-only">
              {{ plane.certification_date ? new Date(plane.certification_date).getFullYear() : 'N/A' }}
            </td>
            <td>
              <div class="eligibility-badges">
                <span
                  v-if="plane.sport_pilot_eligible"
                  class="badge badge-success"
                  title="Eligible for sport pilot operation"
                >
                  Sport Pilot
                </span>
                <span
                  v-else-if="plane.is_mosaic_compliant"
                  class="badge badge-warning"
                  title="MOSAIC LSA compliant but requires private pilot certificate"
                >
                  Private Pilot
                </span>
                <span
                  v-else
                  class="badge badge-danger"
                  title="Not MOSAIC eligible - exceeds stall speed limits"
                >
                  Not MOSAIC
                </span>
                <span
                  v-if="plane.retractable_gear"
                  class="badge badge-info"
                  title="Retractable landing gear - endorsement required for sport pilots"
                >
                  RG
                </span>
                <span
                  v-if="plane.variable_pitch_prop"
                  class="badge badge-info"
                  title="Variable pitch propeller - endorsement required for sport pilots"
                >
                  VP
                </span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Empty State -->
      <div v-if="filteredAircraft.length === 0" class="empty-state" role="status" aria-live="polite">
        <div class="card">
          <h3>No Aircraft Found</h3>
          <p>No aircraft models match your search criteria.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  aircraft: {
    type: Array,
    required: true
  },
  manufacturerName: {
    type: String,
    required: true
  }
})

// Reactive state
const searchQuery = ref('')
const sortField = ref('model')
const sortDirection = ref('asc')

// Computed properties
const filteredAircraft = computed(() => {
  let filtered = [...props.aircraft]
  
  // Search filtering
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim()
    filtered = filtered.filter(a => 
      a.model.toLowerCase().includes(query)
    )
  }
  
  return filtered
})

const sortedAircraft = computed(() => {
  return [...filteredAircraft.value].sort((a, b) => {
    let aValue = a[sortField.value]
    let bValue = b[sortField.value]
    
    // Handle null values
    if (aValue === null || aValue === undefined) aValue = ''
    if (bValue === null || bValue === undefined) bValue = ''
    
    // Convert to strings for comparison if needed
    if (typeof aValue === 'string') aValue = aValue.toLowerCase()
    if (typeof bValue === 'string') bValue = bValue.toLowerCase()
    
    // Sort logic
    let result = 0
    if (aValue < bValue) result = -1
    else if (aValue > bValue) result = 1
    
    return sortDirection.value === 'asc' ? result : -result
  })
})

// Methods
const sortBy = (field) => {
  if (sortField.value === field) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortField.value = field
    sortDirection.value = 'asc'
  }
}

const getSortIcon = (field) => {
  if (sortField.value !== field) return '↕'
  return sortDirection.value === 'asc' ? '↑' : '↓'
}

const getSortAriaAttribute = (field) => {
  if (sortField.value !== field) return 'none'
  return sortDirection.value === 'asc' ? 'ascending' : 'descending'
}
</script>

<style scoped>
.manufacturer-aircraft-table {
  margin-top: 2rem;
}

.table-header {
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 1rem;
}

.table-controls {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.search-control {
  min-width: 250px;
}

.form-control {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid var(--border-color);
  border-radius: 0.375rem;
  background: var(--bg-primary);
  color: var(--text-primary);
  transition: all 0.2s ease;
}

.form-control:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 2px var(--primary-alpha);
}

.table-container {
  overflow-x: auto;
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  background: var(--bg-primary);
}

.table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}

.table th,
.table td {
  padding: 1rem 0.75rem;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

.table th {
  background: var(--bg-secondary);
  font-weight: 600;
  color: var(--text-primary);
  white-space: nowrap;
}

.sortable {
  cursor: pointer;
  user-select: none;
  transition: background-color 0.2s ease;
}

.sortable:hover {
  background: var(--bg-tertiary);
}

.table-row {
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.table-row:hover {
  background: var(--bg-secondary);
}

.aircraft-info {
  min-width: 200px;
}

.aircraft-link {
  color: var(--text-primary);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s ease;
}

.aircraft-link:hover {
  color: var(--primary);
}

.mobile-specs {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.25rem;
}

.mobile-spec {
  font-size: 0.75rem;
  color: var(--text-secondary);
  background: var(--bg-secondary);
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
}

.speed-value {
  font-family: 'Courier New', Consolas, monospace;
  font-weight: 500;
  min-width: 35px;
}

.eligibility-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
}

.badge {
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  white-space: nowrap;
}

.badge-success {
  background-color: var(--success-alpha);
  color: var(--success);
}

.badge-warning {
  background-color: var(--warning-alpha);
  color: var(--warning);
}

.badge-danger {
  background-color: var(--error-alpha);
  color: var(--error);
}

.badge-info {
  background-color: var(--info-alpha);
  color: var(--info);
}

.empty-state {
  padding: 3rem;
  text-align: center;
}

.card {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  padding: 2rem;
}

/* Mobile responsive */
@media (max-width: 768px) {
  .desktop-only {
    display: none !important;
  }
  
  .mobile-only {
    display: block !important;
  }
  
  .table-controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-control {
    min-width: auto;
  }
  
  .table th,
  .table td {
    padding: 0.75rem 0.5rem;
  }
}

@media (min-width: 769px) {
  .desktop-only {
    display: table-cell !important;
  }
  
  .mobile-only {
    display: none !important;
  }
}

/* Focus styles for accessibility */
.sortable:focus {
  outline: 2px solid var(--primary);
  outline-offset: -2px;
}

.table-row:focus {
  outline: 2px solid var(--primary);
  outline-offset: -2px;
}

.aircraft-link:focus {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
  border-radius: 2px;
}
</style>