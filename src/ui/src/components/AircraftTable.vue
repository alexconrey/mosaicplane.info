<template>
  <div class="aircraft-table-container">
    <!-- MOSAIC Effective Date Notice -->
    <div class="mosaic-notice" role="alert" aria-live="polite">
      <div class="notice-content">
        <div class="notice-icon">📅</div>
        <div class="notice-text">
          <strong>Important:</strong> This reflects aircraft legality after <strong>October 22, 2025</strong> when MOSAIC becomes effective. 
          These privileges are not currently available.
        </div>
      </div>
    </div>

    <!-- Search and Filter Controls -->
    <div class="controls">
      <div class="card">
        <div class="controls-header">
          <h3>Aircraft Database</h3>
          <div class="controls-stats">
            <span class="badge" :class="aircraft.length === 0 ? 'badge-error badge-pulse' : 'badge-info'">{{ aircraft.length }} Total Aircraft</span>
            <div class="eligibility-legend">
              <button 
                @click="showLegend = !showLegend" 
                class="legend-button"
                :class="{ active: showLegend }"
                :aria-expanded="showLegend"
                aria-controls="legend-dropdown"
              >
                🧭 Legend
                <span class="arrow">{{ showLegend ? '▼' : '▶' }}</span>
              </button>
              <div 
                v-if="showLegend" 
                class="legend-dropdown"
                id="legend-dropdown"
              >
                <div class="legend-header">
                  <small class="legend-instruction">Click any badge to filter aircraft</small>
                </div>
                <div class="legend-item">
                  <button 
                    @click="toggleBadgeFilter('Sport Pilot')"
                    class="badge badge-success badge-clickable legend-badge"
                    :class="{ 'badge-active': selectedBadges.includes('Sport Pilot') }"
                  >
                    Sport Pilot
                  </button>
                  <div class="legend-text">
                    <strong>Stall speed ≤59 knots</strong><br>
                    Can be flown with sport pilot certificate. Sport pilots limited to 1 passenger.
                  </div>
                </div>
                <div class="legend-item">
                  <button 
                    @click="toggleBadgeFilter('Private Pilot')"
                    class="badge badge-warning badge-clickable legend-badge"
                    :class="{ 'badge-active': selectedBadges.includes('Private Pilot') }"
                  >
                    Private Pilot
                  </button>
                  <div class="legend-text">
                    <strong>Stall speed 59-61 knots</strong><br>
                    MOSAIC LSA compliant but requires private pilot certificate.
                  </div>
                </div>
                <div class="legend-item">
                  <button 
                    @click="toggleBadgeFilter('Not MOSAIC Eligible')"
                    class="badge badge-danger badge-clickable legend-badge"
                    :class="{ 'badge-active': selectedBadges.includes('Not MOSAIC Eligible') }"
                  >
                    Not MOSAIC Eligible
                  </button>
                  <div class="legend-text">
                    <strong>Stall speed >61 knots</strong><br>
                    Exceeds MOSAIC limits. Requires private pilot certificate.
                  </div>
                </div>
                <div class="legend-item">
                  <button 
                    @click="toggleBadgeFilter('MOSAIC Eligible')"
                    class="badge badge-purple badge-clickable legend-badge"
                    :class="{ 'badge-active': selectedBadges.includes('MOSAIC Eligible') }"
                  >
                    MOSAIC Eligible
                  </button>
                  <div class="legend-text">
                    <strong>Stall speed ≤61 knots</strong><br>
                    Meets MOSAIC Light Sport Aircraft criteria. Includes both Sport Pilot and Private Pilot eligible aircraft.
                  </div>
                </div>
                <div class="legend-item">
                  <button 
                    @click="toggleBadgeFilter('RG')"
                    class="badge badge-info badge-clickable legend-badge"
                    :class="{ 'badge-active': selectedBadges.includes('RG') }"
                  >
                    RG
                  </button>
                  <div class="legend-text">
                    <strong>Retractable Gear</strong><br>
                    Endorsement required for sport pilots.
                  </div>
                </div>
                <div class="legend-item">
                  <button 
                    @click="toggleBadgeFilter('VP')"
                    class="badge badge-info badge-clickable legend-badge"
                    :class="{ 'badge-active': selectedBadges.includes('VP') }"
                  >
                    VP
                  </button>
                  <div class="legend-text">
                    <strong>Variable Pitch Propeller</strong><br>
                    Endorsement required for sport pilots.
                  </div>
                </div>
                <div class="legend-footer">
                  <small><em>MOSAIC regulations effective October 22, 2025</em></small>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="controls-grid">
          <!-- Search -->
          <div class="control-group">
            <label for="search-aircraft">Search Aircraft</label>
            <Tooltip 
              text="Search by model or manufacturer. Supports multiple terms (e.g., 'cessna 172')."
              position="bottom"
              :delay="100"
            >
              <input
                id="search-aircraft"
                v-model="searchQuery"
                type="text"
                class="form-control"
                placeholder="Search aircraft (e.g., 'cessna 172', '172', 'piper')"
                aria-describedby="search-hint"
              />
            </Tooltip>
            <div id="search-hint" class="sr-only">Search by aircraft model or manufacturer name. Supports multiple terms.</div>
          </div>


          <!-- Manufacturer Filter -->
          <div class="control-group">
            <label for="manufacturer-filter">Manufacturer</label>
            <select id="manufacturer-filter" v-model="manufacturerFilter" class="form-control">
              <option value="all">All Manufacturers</option>
              <option v-for="manufacturer in manufacturers" 
                      :key="manufacturer.id" 
                      :value="manufacturer.id">
                {{ manufacturer.name }}
              </option>
            </select>
          </div>

          <!-- Seating Filter -->
          <div class="control-group">
            <label for="seating-filter">Seating Capacity</label>
            <select id="seating-filter" v-model="seatingFilter" class="form-control">
              <option value="all">Any Seating</option>
              <option value="2">2 Seats</option>
              <option value="4">4 Seats</option>
            </select>
          </div>

          <!-- Year Range Filter -->
          <div v-if="minYear && maxYear" class="control-group">
            <label>Certification Year Range</label>
            <div class="year-range-container">
              <VueSlider
                v-model="yearRange"
                :min="minYear"
                :max="maxYear"
                :tooltip="'always'"
                :tooltip-placement="'bottom'"
                :height="6"
                class="year-range-slider"
              />
            </div>
          </div>

        </div>
        
        <!-- Badge Filters Row -->
        <div class="badge-filters-section">
          <div class="badge-filters-header">
            <label class="badge-filters-label">Filter by Labels:</label>
          </div>
          
          <div class="badge-filters-row">
            <div class="badge-filters-left">
              <button
                v-for="badge in availableBadges"
                :key="badge.name"
                @click="toggleBadgeFilter(badge.name)"
                class="badge badge-clickable badge-filter-button"
                :class="[
                  getBadgeClass(badge.name),
                  { 'badge-active': selectedBadges.includes(badge.name) }
                ]"
              >
                {{ badge.name }} ({{ badge.count }})
              </button>
            </div>
            
            <div class="badge-filters-right">
              <div class="control-group per-page-inline">
                <label for="items-per-page-inline" class="per-page-label">Per Page:</label>
                <select id="items-per-page-inline" v-model="selectedItemsPerPage" class="form-control form-control-sm">
                  <option value="10">10</option>
                  <option value="20">20</option>
                  <option value="50">50</option>
                  <option value="100">100</option>
                  <option value="all">All</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>


    <!-- Loading State -->
    <div v-if="loading" class="loading-container" role="status" aria-live="polite">
      <div class="spinner" aria-hidden="true"></div>
      <p>Loading aircraft data...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-container" role="alert">
      <div class="card">
        <h3><strong>{{ errorTitle }}</strong></h3>
        <p>{{ errorMessage }}</p>
        <div class="error-buttons">
          <button @click="fetchData" class="btn btn-primary">Retry</button>
          <button @click="takeABreak" class="btn btn-secondary">Take a break</button>
        </div>
      </div>
    </div>

    <!-- Aircraft Table -->
    <div v-else class="table-container">
      <table class="table" role="table" aria-label="Aircraft database with sorting and filtering">
        <caption class="sr-only">
          Aircraft database showing {{ filteredAircraft.length }} aircraft with eligibility information. Use table headers to sort data.
        </caption>
        <thead>
          <tr>
            <th scope="col" class="checkbox-col">
              <input
                type="checkbox"
                class="checkbox desktop-only"
                :checked="allVisibleSelected"
                @change="toggleSelectAll"
                :indeterminate="someSelected"
                aria-label="Select all visible aircraft"
              />
              <span class="mobile-only selection-header">Select</span>
            </th>
            <th scope="col" class="sortable" @click="sortBy('manufacturer_name')"
                :aria-sort="getSortAriaAttribute('manufacturer_name')"
                tabindex="0"
                @keydown.enter="sortBy('manufacturer_name')"
                @keydown.space.prevent="sortBy('manufacturer_name')">
              Aircraft {{ getSortIcon('manufacturer_name') }}
            </th>
            <th scope="col" class="desktop-only sortable" @click="sortBy('clean_stall_speed')"
                :aria-sort="getSortAriaAttribute('clean_stall_speed')"
                tabindex="0"
                @keydown.enter="sortBy('clean_stall_speed')"
                @keydown.space.prevent="sortBy('clean_stall_speed')">
              Stall Speed {{ getSortIcon('clean_stall_speed') }}
            </th>
            <th scope="col" class="desktop-only sortable" @click="sortBy('top_speed')"
                :aria-sort="getSortAriaAttribute('top_speed')"
                tabindex="0"
                @keydown.enter="sortBy('top_speed')"
                @keydown.space.prevent="sortBy('top_speed')">
              Top Speed {{ getSortIcon('top_speed') }}
            </th>
            <th scope="col" class="desktop-only sortable" @click="sortBy('seating_capacity')"
                :aria-sort="getSortAriaAttribute('seating_capacity')"
                tabindex="0"
                @keydown.enter="sortBy('seating_capacity')"
                @keydown.space.prevent="sortBy('seating_capacity')">
              Seats {{ getSortIcon('seating_capacity') }}
            </th>
            <th scope="col" class="desktop-only sortable" @click="sortBy('certification_date')"
                :aria-sort="getSortAriaAttribute('certification_date')"
                tabindex="0"
                @keydown.enter="sortBy('certification_date')"
                @keydown.space.prevent="sortBy('certification_date')">
              Year {{ getSortIcon('certification_date') }}
            </th>
            <th scope="col">Eligibility</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="aircraft in paginatedAircraft"
            :key="aircraft.id"
            :class="{ selected: isSelected(aircraft) }"
            @click="toggleSelection(aircraft, $event)"
            @keydown.enter="toggleSelection(aircraft, $event)"
            @keydown.space.prevent="toggleSelection(aircraft, $event)"
            tabindex="0"
            :aria-selected="isSelected(aircraft)"
            role="row"
            :aria-label="`${aircraft.manufacturer_name} ${aircraft.model} aircraft row`"
          >
            <td class="checkbox-col">
              <input
                type="checkbox"
                class="checkbox desktop-only"
                :checked="isSelected(aircraft)"
                @change="toggleSelection(aircraft, $event)"
                @click.stop
                :aria-label="`Select ${aircraft.manufacturer_name} ${aircraft.model}`"
              />
              <button 
                @click.stop="toggleSelection(aircraft)"
                class="btn btn-secondary btn-sm mobile-only"
              >
                {{ isSelected(aircraft) ? 'Selected' : 'Select' }}
              </button>
            </td>
            <td class="aircraft-info">
              <div class="aircraft-name">
                <router-link 
                  :to="`/aircraft/${aircraft.id}`" 
                  class="aircraft-link"
                >
                  <strong>{{ aircraft.manufacturer_name }} {{ aircraft.model }}</strong>
                </router-link>
              </div>
              <div class="mobile-only aircraft-details">
                <div class="detail-row">
                  <span class="detail-label">Stall:</span>
                  <span>{{ aircraft.clean_stall_speed }}kt</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">Top:</span>
                  <span>{{ aircraft.top_speed }}kt</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">Seats:</span>
                  <span>{{ aircraft.seating_capacity }}</span>
                </div>
              </div>
            </td>
            <td class="desktop-only">
              <span class="speed-value">{{ aircraft.clean_stall_speed }}kt</span>
            </td>
            <td class="desktop-only">
              <span class="speed-value">{{ aircraft.top_speed }}kt</span>
            </td>
            <td class="desktop-only">
              {{ aircraft.seating_capacity }}
            </td>
            <td class="desktop-only">
              {{ aircraft.certification_date ? new Date(aircraft.certification_date).getFullYear() : 'N/A' }}
            </td>
            <td>
              <div class="eligibility-badges">
                <Tooltip 
                  v-if="aircraft.sport_pilot_eligible" 
                  :text="`Sport Pilot Eligible - Stall speed ${aircraft.clean_stall_speed} knots is ≤59 knots CAS. Sport pilots can fly this aircraft with up to 1 passenger. Click to filter.`"
                  position="top"
                >
                  <button 
                    @click.stop="toggleBadgeFilter('Sport Pilot')"
                    class="badge badge-success badge-clickable"
                    :class="{ 'badge-active': selectedBadges.includes('Sport Pilot') }"
                  >
                    Sport Pilot
                  </button>
                </Tooltip>
                <Tooltip 
                  v-else-if="aircraft.is_mosaic_compliant" 
                  :text="`Private Pilot Required - Stall speed ${aircraft.clean_stall_speed} knots is between 59-61 knots CAS. MOSAIC LSA compliant but requires private pilot certificate or higher. Click to filter.`"
                  position="top"
                >
                  <button 
                    @click.stop="toggleBadgeFilter('Private Pilot')"
                    class="badge badge-warning badge-clickable"
                    :class="{ 'badge-active': selectedBadges.includes('Private Pilot') }"
                  >
                    Private Pilot
                  </button>
                </Tooltip>
                <Tooltip 
                  v-else 
                  :text="`Not MOSAIC Eligible - Stall speed ${aircraft.clean_stall_speed} knots exceeds 61 knots CAS maximum. Does not qualify under MOSAIC regulations. Click to filter.`"
                  position="top"
                >
                  <button 
                    @click.stop="toggleBadgeFilter('Not MOSAIC Eligible')"
                    class="badge badge-danger badge-clickable"
                    :class="{ 'badge-active': selectedBadges.includes('Not MOSAIC Eligible') }"
                  >
                    Not MOSAIC Eligible
                  </button>
                </Tooltip>
                <Tooltip 
                  v-if="aircraft.retractable_gear" 
                  :text="`Retractable Landing Gear - This aircraft has retractable landing gear. Sport pilots require a logbook endorsement to operate aircraft with retractable gear. Click to filter.`"
                  position="top"
                >
                  <button 
                    @click.stop="toggleBadgeFilter('RG')"
                    class="badge badge-info badge-clickable"
                    :class="{ 'badge-active': selectedBadges.includes('RG') }"
                  >
                    RG
                  </button>
                </Tooltip>
                <Tooltip 
                  v-if="aircraft.variable_pitch_prop" 
                  :text="`Variable Pitch Propeller - This aircraft has a variable pitch (constant speed) propeller. Sport pilots require a logbook endorsement to operate aircraft with variable pitch props. Click to filter.`"
                  position="top"
                >
                  <button 
                    @click.stop="toggleBadgeFilter('VP')"
                    class="badge badge-info badge-clickable"
                    :class="{ 'badge-active': selectedBadges.includes('VP') }"
                  >
                    VP
                  </button>
                </Tooltip>
                <Tooltip 
                  v-if="aircraft.is_mosaic_compliant" 
                  :text="`MOSAIC Eligible - This aircraft meets MOSAIC Light Sport Aircraft criteria with stall speed ≤61 knots CAS. Click to filter.`"
                  position="top"
                >
                  <button 
                    @click.stop="toggleBadgeFilter('MOSAIC Eligible')"
                    class="badge badge-clickable"
                    :class="[getBadgeClass('MOSAIC Eligible'), { 'badge-active': selectedBadges.includes('MOSAIC Eligible') }]"
                  >
                    MOSAIC Eligible
                  </button>
                </Tooltip>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Empty State -->
      <div v-if="filteredAircraft.length === 0" class="empty-state" role="status" aria-live="polite">
        <div class="card">
          <h3>No Aircraft Found</h3>
          <p>Try adjusting your search or filter criteria.</p>
          <button @click="clearFilters" class="btn btn-secondary">Clear Filters</button>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="selectedItemsPerPage !== 'all' && totalPages > 1" class="pagination">
      <button
        @click="goToPage(Math.max(1, currentPage - 1))"
        :disabled="currentPage === 1"
        class="btn btn-secondary pagination-btn"
      >
        ← Previous
      </button>
      
      <div class="page-selector">
        <button
          v-if="currentPage > 3"
          @click="goToPage(1)"
          class="btn btn-secondary page-btn"
        >
          1
        </button>
        <span v-if="currentPage > 4" class="page-dots">...</span>
        
        <button
          v-for="page in visiblePages"
          :key="page"
          @click="goToPage(page)"
          class="btn page-btn"
          :class="{ 
            'btn-primary': page === currentPage, 
            'btn-secondary': page !== currentPage 
          }"
        >
          {{ page }}
        </button>
        
        <span v-if="currentPage < totalPages - 3" class="page-dots">...</span>
        <button
          v-if="currentPage < totalPages - 2"
          @click="goToPage(totalPages)"
          class="btn btn-secondary page-btn"
        >
          {{ totalPages }}
        </button>
      </div>
      
      <button
        @click="goToPage(Math.min(totalPages, currentPage + 1))"
        :disabled="currentPage === totalPages"
        class="btn btn-secondary pagination-btn"
      >
        Next →
      </button>
    </div>
    
    <div v-if="selectedItemsPerPage !== 'all' && totalPages > 1" class="pagination-info">
      Showing {{ (currentPage - 1) * itemsPerPage + 1 }}-{{ Math.min(currentPage * itemsPerPage, filteredAircraft.length) }} 
      of {{ filteredAircraft.length }} aircraft
    </div>
    <div v-else-if="selectedItemsPerPage === 'all'" class="pagination-info">
      Showing all {{ filteredAircraft.length }} aircraft
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, inject } from 'vue'
import Tooltip from './Tooltip.vue'
import { apiRequest } from '../utils/api.js'
import VueSlider from 'vue-slider-component'
import 'vue-slider-component/theme/default.css'

const emit = defineEmits(['aircraft-selected'])
const props = defineProps({
  selectedAircraft: {
    type: Array,
    default: () => []
  }
})

// Inject branding context
const branding = inject('branding', { showAllAircraft: ref(false), isMosaicPlane: ref(false) })

// Data state
const aircraft = ref([])
const manufacturers = ref([])
const loading = ref(true)
const error = ref(null)

// Humorous error state
const errorTitle = ref('')
const errorMessage = ref('')

// Technical nonsense problems for error titles
const technicalProblems = [
  'Flux capacitor on verge of failure',
  'Quantum entanglement matrix destabilized', 
  'Dilithium crystal alignment error',
  'Hyperspace engine requires recalibration',
  'Temporal displacement buffer overflow',
  'Tachyon emission levels critically low',
  'Warp core containment field fluctuating',
  'Subspace communication array malfunctioning',
  'Ion drive manifold pressure anomaly detected',
  'Gravitational wave interference detected',
  'Dark matter injection system offline',
  'Antimatter containment field weakening',
  'Plasma conduit experiencing cascade failure',
  'Neutron flow regulator stuck in reverse',
  'Chronometer synchronization protocol failed',
  'Dimensional stabilizer needs urgent repair',
  'Particle accelerator running backwards',
  'Space-time continuum experiencing hiccups',
  'Electromagnetic field generator overheating',
  'Cosmic ray deflector shield malfunctioning'
]

// Get or initialize engineer count from localStorage with decrement
const getEngineerCount = () => {
  const stored = localStorage.getItem('engineerCount')
  let count = stored ? parseInt(stored) : 72
  
  if (count > 0) {
    count -= 1
    localStorage.setItem('engineerCount', count.toString())
  }
  
  return count
}

// Reset engineer count when API is working again
const resetEngineerCount = () => {
  localStorage.setItem('engineerCount', '72')
}

// Filter state
const searchQuery = ref('')
const manufacturerFilter = ref('all')
const seatingFilter = ref('all')
const showOnlyMosaic = ref(!branding.showAllAircraft.value)
// Initialize selectedBadges with Sport Pilot filter for MosaicPlane.info
const selectedBadges = ref(branding.isMosaicPlane.value ? ['Sport Pilot'] : [])

// Year range filter state
const yearRange = ref([1940, 2025])

// Pagination state
const selectedItemsPerPage = ref(typeof window !== 'undefined' && window.innerWidth >= 768 ? '25' : '10')

// Selection state
const selectedIds = ref(new Set())

// UI state
const showLegend = ref(false)

// Sorting state
const sortField = ref('manufacturer_name')
const sortDirection = ref('asc') // 'asc' or 'desc'

// Pagination
const currentPage = ref(1)
const itemsPerPage = computed(() => {
  if (selectedItemsPerPage.value === 'all') {
    return filteredAircraft.value.length
  }
  return parseInt(selectedItemsPerPage.value)
})

// Computed properties - filtering only (no sorting)
const filteredAircraft = computed(() => {
  let filtered = aircraft.value

  // Search filter (case insensitive, space-tolerant)
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase().trim()
    
    // Support multiple search terms separated by spaces
    const searchTerms = query.split(/\s+/).filter(term => term.length > 0)
    
    filtered = filtered.filter(a => {
      const searchableText = `${a.model} ${a.manufacturer_name}`.toLowerCase()
      
      // If no search terms, don't filter
      if (searchTerms.length === 0) return true
      
      // All search terms must be found in the searchable text
      return searchTerms.every(term => searchableText.includes(term))
    })
  }

  // Manufacturer filter
  if (manufacturerFilter.value !== 'all') {
    filtered = filtered.filter(a => a.manufacturer === parseInt(manufacturerFilter.value))
  }

  // Seating filter
  if (seatingFilter.value !== 'all') {
    filtered = filtered.filter(a => a.seating_capacity === parseInt(seatingFilter.value))
  }

  // Year range filter
  filtered = filtered.filter(a => {
    if (!a.certification_date) return true // Include aircraft without certification date
    const year = new Date(a.certification_date).getFullYear()
    return year >= parseInt(yearRange.value[0]) && year <= parseInt(yearRange.value[1])
  })

  // Badge-based filtering
  if (selectedBadges.value.length > 0) {
    filtered = filtered.filter(a => {
      const aircraftBadges = getAircraftBadges(a)
      return selectedBadges.value.every(badge => aircraftBadges.includes(badge))
    })
  }

  // Return filtered data WITHOUT sorting - sorting happens on paginated slice
  return filtered
})

const paginatedAircraft = computed(() => {
  // First get the page slice
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  const pageSlice = filteredAircraft.value.slice(start, end)
  
  // Then sort ONLY the current page data
  return pageSlice.sort((a, b) => {
    let aValue = a[sortField.value]
    let bValue = b[sortField.value]
    
    // Handle special cases for different data types
    if (sortField.value === 'certification_date') {
      aValue = aValue ? new Date(aValue).getFullYear() : 0
      bValue = bValue ? new Date(bValue).getFullYear() : 0
    } else if (typeof aValue === 'string') {
      aValue = aValue.toLowerCase()
      bValue = bValue.toLowerCase()
    }
    
    // Compare values
    let comparison = 0
    if (aValue > bValue) comparison = 1
    if (aValue < bValue) comparison = -1
    
    // Apply sort direction
    return sortDirection.value === 'asc' ? comparison : -comparison
  })
})

const totalPages = computed(() => 
  Math.ceil(filteredAircraft.value.length / itemsPerPage.value)
)

const visiblePages = computed(() => {
  const delta = 2
  const range = []
  const rangeStart = Math.max(1, currentPage.value - delta)
  const rangeEnd = Math.min(totalPages.value, currentPage.value + delta)
  
  for (let i = rangeStart; i <= rangeEnd; i++) {
    range.push(i)
  }
  
  return range
})

const sportPilotCount = computed(() => 
  filteredAircraft.value.filter(a => a.sport_pilot_eligible).length
)

const totalSportPilotCount = computed(() => 
  aircraft.value.filter(a => a.sport_pilot_eligible).length
)

const availableBadges = computed(() => {
  const badgeCounts = {
    'Sport Pilot': aircraft.value.filter(a => a.sport_pilot_eligible).length,
    'Private Pilot': aircraft.value.filter(a => !a.sport_pilot_eligible && a.is_mosaic_compliant).length,
    'Not MOSAIC Eligible': aircraft.value.filter(a => !a.is_mosaic_compliant).length,
    'MOSAIC Eligible': aircraft.value.filter(a => a.is_mosaic_compliant).length,
    'RG': aircraft.value.filter(a => a.retractable_gear).length,
    'VP': aircraft.value.filter(a => a.variable_pitch_prop).length
  }
  
  return Object.entries(badgeCounts)
    .filter(([_, count]) => count > 0)
    .map(([name, count]) => ({ name, count }))
})

const allVisibleSelected = computed(() =>
  paginatedAircraft.value.length > 0 && 
  paginatedAircraft.value.every(a => selectedIds.value.has(a.id))
)

const someSelected = computed(() =>
  paginatedAircraft.value.some(a => selectedIds.value.has(a.id)) && 
  !allVisibleSelected.value
)

// Year range computed properties
const minYear = computed(() => {
  if (aircraft.value.length === 0) return null
  const years = aircraft.value
    .map(a => a.certification_date ? new Date(a.certification_date).getFullYear() : null)
    .filter(year => year !== null)
  return years.length > 0 ? Math.min(...years) : null
})

const maxYear = computed(() => {
  if (aircraft.value.length === 0) return null
  const years = aircraft.value
    .map(a => a.certification_date ? new Date(a.certification_date).getFullYear() : null)
    .filter(year => year !== null)
  return years.length > 0 ? Math.max(...years) : null
})

// Methods
const fetchData = async () => {
  loading.value = true
  error.value = null
  
  try {
    // Fetch aircraft and manufacturers in parallel
    const [aircraftResponse, manufacturersResponse] = await Promise.all([
      apiRequest('/v1/aircraft/'),
      apiRequest('/v1/manufacturers/')
    ])

    if (!aircraftResponse.ok || !manufacturersResponse.ok) {
      throw new Error('Failed to fetch data')
    }

    const aircraftData = await aircraftResponse.json()
    const manufacturersData = await manufacturersResponse.json()

    aircraft.value = aircraftData.results || aircraftData
    manufacturers.value = manufacturersData.results || manufacturersData
    
    // Reset engineer count since API is working
    resetEngineerCount()
    
  } catch (err) {
    console.error('Error fetching data:', err)
    
    // Generate humorous error
    const randomProblem = technicalProblems[Math.floor(Math.random() * technicalProblems.length)]
    const engineerCount = getEngineerCount()
    
    error.value = true
    errorTitle.value = randomProblem
    errorMessage.value = engineerCount > 1 
      ? `Our dedicated team of ${engineerCount} carrier pigeons are working diligently to resolve this issue.`
      : engineerCount === 1
      ? `Our dedicated team of 1 carrier pigeon is working diligently to resolve this issue.`
      : 'Maybe if you stop refreshing, the carrier pigeons will have time to fix this.'
      
  } finally {
    loading.value = false
  }
}

// Open relaxing YouTube video in new tab
const takeABreak = () => {
  window.open('https://www.youtube.com/watch?v=ia8Q51ouA_s', '_blank')
}

const isSelected = (aircraftItem) => selectedIds.value.has(aircraftItem.id)

const toggleSelection = (aircraftItem, event) => {
  // Prevent row click when clicking checkbox
  if (event && event.target.type === 'checkbox') {
    event.stopPropagation()
  }

  if (selectedIds.value.has(aircraftItem.id)) {
    selectedIds.value.delete(aircraftItem.id)
  } else {
    selectedIds.value.add(aircraftItem.id)
  }

  // Emit selected aircraft
  const selected = aircraft.value.filter(a => selectedIds.value.has(a.id))
  emit('aircraft-selected', selected)
}

const toggleSelectAll = () => {
  if (allVisibleSelected.value) {
    // Deselect all visible
    paginatedAircraft.value.forEach(a => selectedIds.value.delete(a.id))
  } else {
    // Select all visible
    paginatedAircraft.value.forEach(a => selectedIds.value.add(a.id))
  }

  const selected = aircraft.value.filter(a => selectedIds.value.has(a.id))
  emit('aircraft-selected', selected)
}

const clearFilters = () => {
  searchQuery.value = ''
  manufacturerFilter.value = 'all'
  seatingFilter.value = 'all'
  showOnlyMosaic.value = !branding.showAllAircraft.value
  // Reset to default badge filters (Sport Pilot for MosaicPlane.info)
  selectedBadges.value = branding.isMosaicPlane.value ? ['Sport Pilot'] : []
  // Reset year range to full range (only if we have year data)
  if (minYear.value && maxYear.value) {
    yearRange.value = [minYear.value, maxYear.value]
  }
  currentPage.value = 1
}


const sortBy = (field) => {
  if (sortField.value === field) {
    // Toggle direction if same field
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    // Set new field and default to ascending
    sortField.value = field
    sortDirection.value = 'asc'
  }
  // Don't reset page - sorting only affects current page now
}

const getSortIcon = (field) => {
  if (sortField.value !== field) return '⇅'
  return sortDirection.value === 'asc' ? '▲' : '▼'
}

const getSortAriaAttribute = (field) => {
  if (sortField.value !== field) return 'none'
  return sortDirection.value === 'asc' ? 'ascending' : 'descending'
}

const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

const getAircraftBadges = (aircraft) => {
  const badges = []
  
  if (aircraft.sport_pilot_eligible) {
    badges.push('Sport Pilot')
  } else if (aircraft.is_mosaic_compliant) {
    badges.push('Private Pilot')
  } else {
    badges.push('Not MOSAIC Eligible')
  }
  
  if (aircraft.is_mosaic_compliant) {
    badges.push('MOSAIC Eligible')
  }
  
  if (aircraft.retractable_gear) {
    badges.push('RG')
  }
  
  if (aircraft.variable_pitch_prop) {
    badges.push('VP')
  }
  
  return badges
}

const toggleBadgeFilter = (badgeName) => {
  const index = selectedBadges.value.indexOf(badgeName)
  if (index > -1) {
    selectedBadges.value.splice(index, 1)
  } else {
    selectedBadges.value.push(badgeName)
  }
  currentPage.value = 1
}

const clearBadgeFilters = () => {
  selectedBadges.value = []
  currentPage.value = 1
}

const getBadgeClass = (badgeName) => {
  switch (badgeName) {
    case 'Sport Pilot':
      return 'badge-success'
    case 'Private Pilot':
      return 'badge-warning'
    case 'Not MOSAIC Eligible':
      return 'badge-danger'
    case 'MOSAIC Eligible':
      return 'badge-purple'
    case 'RG':
    case 'VP':
      return 'badge-info'
    default:
      return 'badge-secondary'
  }
}

// Watch for filter changes and reset pagination
watch([searchQuery, manufacturerFilter, seatingFilter, showOnlyMosaic, selectedBadges, selectedItemsPerPage, yearRange], () => {
  currentPage.value = 1
})

// Initialize year range when aircraft data is loaded
watch(aircraft, () => {
  if (aircraft.value.length > 0 && minYear.value && maxYear.value) {
    // Only set initial values if they haven't been set yet or are still default values
    if (!yearRange.value || yearRange.value.length !== 2 || 
        (yearRange.value[0] === 1940 && yearRange.value[1] === 2025)) {
      yearRange.value = [minYear.value, maxYear.value]
    }
  }
}, { immediate: true })

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.aircraft-table-container {
  margin-bottom: 2rem;
}

/* MOSAIC Effective Date Notice */
.mosaic-notice {
  background: linear-gradient(135deg, #fef3cd, #fcf4a3);
  border: 2px solid #facc15;
  border-radius: 0.75rem;
  padding: 1rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

[data-theme="dark"] .mosaic-notice {
  background: linear-gradient(135deg, #451a03, #713f12);
  border-color: #a16207;
  color: #fbbf24;
}

.notice-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.notice-icon {
  font-size: 1.25rem;
  flex-shrink: 0;
}

.notice-text {
  color: #92400e;
  font-size: 0.9rem;
  line-height: 1.4;
}

[data-theme="dark"] .notice-text {
  color: #fbbf24;
}

.controls {
  margin-bottom: 2rem;
}

.controls-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.controls-stats {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.controls-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.control-group label {
  display: block;
  font-weight: 500;
  margin-bottom: 0.25rem;
  color: var(--text-primary);
  font-size: 0.875rem;
}

.checkbox-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.checkbox-label {
  font-size: 0.875rem;
  color: var(--text-primary);
  cursor: pointer;
  margin-bottom: 0;
}

.checkbox-col {
  width: 50px;
  text-align: center;
}

.selection-header {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-primary);
}

/* Mobile select button styling */
.mobile-only.btn {
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  white-space: nowrap;
}

.aircraft-info {
  min-width: 200px;
}

.aircraft-name {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.aircraft-link {
  text-decoration: none;
  color: var(--text-primary);
  transition: color 0.2s ease;
}

.aircraft-link:hover {
  color: var(--text-accent);
  text-decoration: underline;
}

.aircraft-details {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.detail-row {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.detail-label {
  font-weight: 500;
  min-width: 35px;
}

.eligibility-badges {
  display: flex;
  flex-wrap: nowrap;
  gap: 15px;
  overflow: hidden;
  padding: 0;
  margin: 0;
}

.eligibility-badges .tooltip-container {
  display: inline-flex;
  margin: 0;
  padding: 0;
  width: auto;
}

.eligibility-badges .tooltip-container:last-child {
  margin-right: 0;
}

.eligibility-badges .badge-clickable {
  margin-right: 0;
  padding-right: 0.4rem;
}

.badge-clickable {
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  padding: 0.2rem 0.4rem;
  border-radius: 0.25rem;
  font-size: 0.6875rem;
  font-weight: 500;
  color: white;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  text-transform: uppercase;
  letter-spacing: 0.025em;
  white-space: nowrap;
  flex-shrink: 0;
}

/* Use the exact same colors as the standard badge classes */
.badge-clickable.badge-success {
  background-color: var(--success-color);
  color: white;
}

.badge-clickable.badge-warning {
  background-color: var(--warning-color);
  color: white;
}

.badge-clickable.badge-danger {
  background-color: var(--danger-color);
  color: white;
}

.badge-clickable.badge-info {
  background-color: var(--info-color);
  color: white;
}

.badge-clickable.badge-primary {
  background-color: var(--text-accent, #3b82f6);
  color: white;
}

.badge-clickable.badge-purple {
  background-color: #8b5cf6;
  color: white;
}

.badge-clickable:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.badge-active:not(.badge-filter-button) {
  /* Remove active styling from table badges - only show on filter buttons */
}

.active-filters {
  margin-bottom: 1.5rem;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.filter-header h4 {
  margin: 0;
  color: var(--text-primary);
  font-size: 1rem;
}

.filter-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.badge-filter {
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
  color: white;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.badge-filter:hover {
  opacity: 0.8;
  transform: translateY(-1px);
}

.badge-filters-section {
  margin-top: 1rem;
}

.badge-filters-header {
  margin-bottom: 0.5rem;
}

.badge-filters-label {
  font-weight: 500;
  color: var(--text-primary);
  font-size: 0.875rem;
}

.badge-filters-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.badge-filters-left {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  align-items: center;
  flex: 1;
}

.badge-filters-right {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.per-page-inline {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0;
}

.per-page-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-primary);
  margin: 0;
}

.form-control-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
  min-width: 80px;
}

.badge-filter-button {
  transition: all 0.2s ease;
  font-size: 0.75rem !important;
  padding: 0.25rem 0.5rem !important;
  line-height: 1.25 !important;
  font-weight: 500 !important;
  border: 1px solid transparent;
}

.badge-filter-button:hover {
  opacity: 0.8;
  transform: translateY(-1px);
}

.badge-filter-button.badge-active {
  border: 5px solid var(--text-accent, #3b82f6);
  box-shadow: none !important;
  transform: none !important;
}


.speed-value {
  font-weight: 500;
  color: var(--text-primary);
}

.loading-container,
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 3rem 0;

.error-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
}
}

.empty-state {
  text-align: center;
  padding: 2rem 0;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 2rem;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.page-selector {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.page-btn {
  min-width: 2.5rem;
  height: 2.5rem;
  padding: 0;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.pagination-btn {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
}

.page-dots {
  color: var(--text-secondary);
  font-weight: bold;
  padding: 0 0.25rem;
  user-select: none;
}

.pagination-info {
  text-align: center;
  color: var(--text-secondary);
  font-size: 0.875rem;
  margin-top: 1rem;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
  min-width: auto;
}

/* Row hover and selection */
tbody tr {
  cursor: pointer;
  transition: background-color 0.2s ease;
}

tbody tr:hover {
  background-color: var(--bg-secondary);
}

tbody tr.selected {
  background-color: rgba(0, 102, 204, 0.1);
  border-left: 3px solid var(--text-accent);
}

/* Eligibility Legend */
.eligibility-legend {
  position: relative;
  display: inline-block;
}

.legend-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background-color: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 0.375rem;
  color: var(--text-primary);
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s ease;
}

.legend-button:hover {
  background-color: var(--bg-tertiary);
  border-color: var(--border-hover);
}

.legend-button.active {
  background-color: var(--text-accent);
  color: white;
  border-color: var(--text-accent);
}

.arrow {
  font-size: 0.75rem;
  transition: transform 0.2s ease;
}

.legend-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 0.5rem;
  background-color: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
  padding: 1rem;
  width: 400px;
  z-index: 100;
}

.legend-header {
  margin-bottom: 1rem;
  text-align: center;
}

.legend-instruction {
  color: var(--text-secondary);
  font-style: italic;
}

.legend-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.legend-item:last-of-type {
  margin-bottom: 0;
}

.legend-item .badge {
  flex-shrink: 0;
  margin-top: 0.125rem;
}

.legend-text {
  flex: 1;
  font-size: 0.875rem;
  line-height: 1.4;
}

.legend-text strong {
  color: var(--text-primary);
}

.legend-footer {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-color);
  text-align: center;
}

.legend-footer small {
  color: var(--text-secondary);
}

.legend-badge {
  margin-top: 0.125rem;
  white-space: nowrap;
  text-align: center;
  display: inline-block;
}

.filter-hint {
  display: block;
  color: var(--text-secondary);
  font-style: italic;
  margin-top: 0.25rem;
  font-size: 0.6875rem;
}

/* Desktop explicit styling */
/* Mobile styles */
@media (max-width: 640px) {
  .desktop-only {
    display: none !important;
  }
  
  .mobile-only {
    display: block !important;
  }
  
  .checkbox-col {
    width: 70px;
  }
}

@media (min-width: 641px) {
  .desktop-only {
    display: table-cell !important;
  }
  
  .mobile-only {
    display: none !important;
  }
}

/* Tablet responsive adjustments */
@media (max-width: 768px) {
  .table {
    font-size: 0.875rem;
  }
  
  .aircraft-info {
    min-width: 150px;
  }
}

/* Sortable table headers */
.sortable {
  cursor: pointer;
  user-select: none;
  transition: background-color 0.2s ease;
  position: relative;
}

.sortable:hover {
  background-color: var(--bg-secondary);
}

.sortable:active {
  background-color: var(--bg-tertiary);
}

/* Mobile responsive adjustments */
@media (max-width: 640px) {
  .controls-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }

  .controls-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .aircraft-details {
    gap: 0.5rem;
  }

  .badge-filters-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .badge-filters-left {
    width: 100%;
  }

  .badge-filters-right {
    width: 100%;
    justify-content: flex-start;
  }

  .pagination {
    justify-content: center;
    text-align: center;
    gap: 0.25rem;
  }

  .pagination-btn {
    padding: 0.375rem 0.75rem;
    font-size: 0.8rem;
  }

  .page-btn {
    min-width: 2rem;
    height: 2rem;
    font-size: 0.8rem;
  }

  .pagination-info {
    font-size: 0.8rem;
  }

  .legend-dropdown {
    right: auto;
    left: 0;
    width: 280px;
  }
}

@media (max-width: 480px) {
  .controls-stats {
    flex-direction: column;
    align-items: flex-start;
  }

  .eligibility-badges {
    flex-direction: column;
    gap: 0.125rem;
  }

  .badge {
    font-size: 0.625rem;
    padding: 0.125rem 0.375rem;
  }
}

/* Year Range Slider */
.year-range-container {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.year-range-slider {
  margin: 1rem 0;
}

.year-range-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-primary);
}

.year-label {
  padding: 0.25rem 0.5rem;
  background-color: var(--bg-secondary);
  border-radius: 0.25rem;
  border: 1px solid var(--border-color);
}

.year-slider-container {
  position: relative;
  height: 20px;
}

.year-slider {
  position: absolute;
  width: 100%;
  height: 6px;
  background: #e5e7eb;
  outline: none;
  appearance: none;
  -webkit-appearance: none;
  cursor: pointer;
}

[data-theme="dark"] .year-slider {
  background: #374151;
}

.year-slider::-webkit-slider-track {
  height: 6px;
  background: #d1d5db;
  border-radius: 3px;
  border: 1px solid #9ca3af;
}

[data-theme="dark"] .year-slider::-webkit-slider-track {
  background: #4b5563;
  border-color: #6b7280;
}

.year-slider::-webkit-slider-thumb {
  appearance: none;
  -webkit-appearance: none;
  height: 18px;
  width: 18px;
  background: var(--text-accent);
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid var(--bg-primary);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.year-slider::-moz-range-track {
  height: 6px;
  background: #d1d5db;
  border-radius: 3px;
  border: 1px solid #9ca3af;
}

[data-theme="dark"] .year-slider::-moz-range-track {
  background: #4b5563;
  border-color: #6b7280;
}

.year-slider::-moz-range-thumb {
  height: 18px;
  width: 18px;
  background: var(--text-accent);
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid var(--bg-primary);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.year-slider-min {
  z-index: 1;
}

.year-slider-max {
  z-index: 2;
}

/* Accessibility Styles */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Enhanced focus indicators */
.sortable:focus {
  outline: 2px solid var(--text-accent);
  outline-offset: 2px;
}

tbody tr:focus {
  outline: 2px solid var(--text-accent);
  outline-offset: -2px;
}

.year-slider:focus {
  outline: 2px solid var(--text-accent);
  outline-offset: 2px;
}

/* Improve keyboard navigation */
.sortable {
  position: relative;
}

.sortable:focus-visible {
  background-color: var(--bg-secondary);
}

/* Error badge styling with red glow */
.badge-error {
  background-color: #dc2626 !important;
  color: white !important;
  border: 2px solid #ef4444;
  box-shadow: 0 0 8px rgba(239, 68, 68, 0.6);
}

/* Pulsing animation for error state */
.badge-pulse {
  animation: pulse-error 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse-error {
  0%, 100% {
    opacity: 1;
    box-shadow: 0 0 8px rgba(239, 68, 68, 0.6);
  }
  50% {
    opacity: 0.8;
    box-shadow: 0 0 16px rgba(239, 68, 68, 0.9), 0 0 24px rgba(239, 68, 68, 0.4);
  }
}

/* Dark theme adjustments */
[data-theme="dark"] .badge-error {
  background-color: #dc2626 !important;
  border-color: #f87171;
  box-shadow: 0 0 8px rgba(248, 113, 113, 0.6);
}

[data-theme="dark"] .badge-pulse {
  animation: pulse-error-dark 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse-error-dark {
  0%, 100% {
    opacity: 1;
    box-shadow: 0 0 8px rgba(248, 113, 113, 0.6);
  }
  50% {
    opacity: 0.8;
    box-shadow: 0 0 16px rgba(248, 113, 113, 0.9), 0 0 24px rgba(248, 113, 113, 0.4);
  }
}
</style>