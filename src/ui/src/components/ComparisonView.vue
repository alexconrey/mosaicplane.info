<template>
  <div class="comparison-view" role="dialog" aria-modal="true" aria-labelledby="comparison-title">
    <div class="modal-backdrop" @click="$emit('close')" aria-hidden="true"></div>
    <div class="card" role="document">
      <div class="comparison-header">
        <h3 id="comparison-title">Aircraft Comparison</h3>
        <button 
          @click="$emit('close')" 
          class="btn btn-secondary close-button"
          aria-label="Close comparison dialog"
        >
          <span aria-hidden="true">✕</span>
          <span class="close-text">Close</span>
        </button>
      </div>

      <div class="comparison-grid">
        <article 
          v-for="aircraft in props.aircraft" 
          :key="aircraft.id"
          class="aircraft-card"
          :aria-labelledby="`aircraft-${aircraft.id}-name`"
        >
          <!-- Aircraft Header -->
          <header class="aircraft-header">
            <!-- Aircraft Image -->
            <div class="aircraft-image-preview">
              <img 
                v-if="aircraft.image" 
                :src="aircraft.image" 
                :alt="`Photo of ${aircraft.manufacturer.name} ${aircraft.model} aircraft`"
                class="aircraft-thumbnail"
              />
              <div 
                v-else 
                class="no-image-placeholder"
                role="img"
                :aria-label="`No photo available for ${aircraft.manufacturer.name} ${aircraft.model}`"
              >
                <span class="no-image-text" aria-hidden="true">No Image</span>
              </div>
            </div>
            
            <h4 :id="`aircraft-${aircraft.id}-name`">
              <router-link 
                :to="`/aircraft/${aircraft.id}`" 
                class="aircraft-name-link"
                :aria-label="`View detailed information for ${aircraft.manufacturer.name} ${aircraft.model}`"
              >
                {{ aircraft.manufacturer.name }} {{ aircraft.model }}
              </router-link>
            </h4>
            <div class="certification-year">
              Certified {{ aircraft.certification_date ? new Date(aircraft.certification_date).getFullYear() : 'N/A' }}
            </div>
          </header>

          <!-- Eligibility Status -->
          <div class="eligibility-section">
            <h5>Pilot Eligibility</h5>
            <div class="eligibility-badges">
              <span 
                v-if="aircraft.sport_pilot_eligible" 
                class="badge badge-success large"
              >
                ✓ Sport Pilot Eligible
              </span>
              <span 
                v-else-if="aircraft.is_mosaic_compliant" 
                class="badge badge-warning large"
              >
                ⚠ Private Pilot Required
              </span>
              <div class="endorsements">
                <span 
                  v-if="aircraft.retractable_gear" 
                  class="badge badge-info"
                  title="Retractable Landing Gear - Endorsement Required"
                >
                  Retractable Gear
                </span>
                <span 
                  v-if="aircraft.variable_pitch_prop" 
                  class="badge badge-info"
                  title="Variable Pitch Propeller - Endorsement Required"
                >
                  Variable Pitch Prop
                </span>
              </div>
            </div>
          </div>

          <!-- Performance Specs -->
          <div class="specs-section">
            <h5>Performance</h5>
            <div class="specs-grid">
              <div class="spec-item">
                <div class="spec-label">Stall Speed (Vs1)</div>
                <div class="spec-value" :class="getStallSpeedClass(aircraft.clean_stall_speed)">
                  {{ aircraft.clean_stall_speed }} knots
                  <div class="spec-note">
                    {{ aircraft.clean_stall_speed <= 59 ? 'Sport Pilot OK' : 'Private Pilot Only' }}
                  </div>
                </div>
              </div>

              <div class="spec-item">
                <div class="spec-label">Top Speed</div>
                <div class="spec-value highlight">
                  {{ aircraft.top_speed }} knots
                </div>
              </div>

              <div class="spec-item">
                <div class="spec-label">Maneuvering Speed (Va)</div>
                <div class="spec-value">
                  {{ aircraft.maneuvering_speed }} knots
                </div>
              </div>
              <div class="spec-item" v-if="aircraft.cruise_speed">
                <div class="spec-label">Cruise Speed</div>
                <div class="spec-value">
                  {{ aircraft.cruise_speed }} knots
                  <div class="spec-note">75% power</div>
                </div>
              </div>
              <div class="spec-item" v-if="aircraft.vx_speed">
                <div class="spec-label">Best Angle Climb (Vx)</div>
                <div class="spec-value">
                  {{ aircraft.vx_speed }} knots
                </div>
              </div>
              <div class="spec-item" v-if="aircraft.vy_speed">
                <div class="spec-label">Best Rate Climb (Vy)</div>
                <div class="spec-value">
                  {{ aircraft.vy_speed }} knots
                </div>
              </div>
              <div class="spec-item" v-if="aircraft.vs0_speed">
                <div class="spec-label">Stall Speed (Vs0)</div>
                <div class="spec-value">
                  {{ aircraft.vs0_speed }} knots
                  <div class="spec-note">Landing config</div>
                </div>
              </div>
              <div class="spec-item" v-if="aircraft.vg_speed">
                <div class="spec-label">Best Glide (Vg)</div>
                <div class="spec-value">
                  {{ aircraft.vg_speed }} knots
                </div>
              </div>
              <div class="spec-item" v-if="aircraft.vfe_speed">
                <div class="spec-label">Max Flap Extended (Vfe)</div>
                <div class="spec-value">
                  {{ aircraft.vfe_speed }} knots
                </div>
              </div>
              <div class="spec-item" v-if="aircraft.vno_speed">
                <div class="spec-label">Max Structural Cruise (Vno)</div>
                <div class="spec-value">
                  {{ aircraft.vno_speed }} knots
                </div>
              </div>
              <div class="spec-item" v-if="aircraft.vne_speed">
                <div class="spec-label">Never Exceed (Vne)</div>
                <div class="spec-value text-danger">
                  {{ aircraft.vne_speed }} knots
                </div>
              </div>

              <div class="spec-item">
                <div class="spec-label">Max Takeoff Weight</div>
                <div class="spec-value">
                  {{ aircraft.max_takeoff_weight?.toLocaleString() || 'N/A' }} lbs
                </div>
              </div>
            </div>
          </div>

          <!-- Configuration -->
          <div class="config-section">
            <h5>Configuration</h5>
            <div class="config-grid">
              <div class="config-item">
                <span class="config-label">Seating:</span>
                <span class="config-value">{{ aircraft.seating_capacity }} seats</span>
              </div>
              <div class="config-item">
                <span class="config-label">Landing Gear:</span>
                <span class="config-value">{{ aircraft.retractable_gear ? 'Retractable' : 'Fixed' }}</span>
              </div>
              <div class="config-item">
                <span class="config-label">Propeller:</span>
                <span class="config-value">{{ aircraft.variable_pitch_prop ? 'Variable Pitch' : 'Fixed Pitch' }}</span>
              </div>
              <div class="config-item">
                <span class="config-label">Manufacturing:</span>
                <span class="config-value">{{ aircraft.manufacturer.is_currently_manufacturing ? 'Active' : 'Legacy' }}</span>
              </div>
            </div>
          </div>

          <!-- MOSAIC Notes for Sport Pilots -->
          <div v-if="aircraft.sport_pilot_eligible" class="mosaic-notes">
            <h5>Sport Pilot Notes</h5>
            <ul class="notes-list">
              <li>Maximum 1 passenger allowed</li>
              <li>
                {{ aircraft.seating_capacity > 2 ? 
                  `${aircraft.seating_capacity - 1} seats remain empty when sport pilot flying` : 
                  'Can use both seats' 
                }}
              </li>
              <li v-if="aircraft.retractable_gear">
                Retractable gear endorsement required
              </li>
              <li v-if="aircraft.variable_pitch_prop">
                Variable pitch propeller endorsement required
              </li>
              <li v-if="!aircraft.retractable_gear && !aircraft.variable_pitch_prop">
                No additional endorsements required
              </li>
            </ul>
          </div>
        </article>
      </div>

      <!-- Comparison Summary -->
      <div class="comparison-summary">
        <h4>Comparison Summary</h4>
        <div class="summary-grid">
          <div class="summary-item">
            <div class="summary-label">Sport Pilot Eligible</div>
            <div class="summary-value">
              {{ sportPilotCount }} of {{ props.aircraft.length }} aircraft
            </div>
          </div>
          <div class="summary-item">
            <div class="summary-label">Fastest Aircraft</div>
            <div class="summary-value">
              {{ fastestAircraft?.manufacturer.name }} {{ fastestAircraft?.model }}
              ({{ fastestAircraft?.top_speed }}kt)
            </div>
          </div>
          <div class="summary-item">
            <div class="summary-label">Lowest Stall Speed</div>
            <div class="summary-value">
              {{ lowestStallAircraft?.manufacturer.name }} {{ lowestStallAircraft?.model }}
              ({{ lowestStallAircraft?.clean_stall_speed }}kt)
            </div>
          </div>
          <div class="summary-item">
            <div class="summary-label">Most Seats</div>
            <div class="summary-value">
              {{ mostSeatsAircraft?.manufacturer.name }} {{ mostSeatsAircraft?.model }}
              ({{ mostSeatsAircraft?.seating_capacity }} seats)
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  aircraft: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['close'])

const handleKeyDown = (event) => {
  if (event.key === 'Escape') {
    emit('close')
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleKeyDown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyDown)
})

const sportPilotCount = computed(() => 
  props.aircraft.filter(a => a.sport_pilot_eligible).length
)

const fastestAircraft = computed(() => 
  props.aircraft.reduce((fastest, current) => 
    current.top_speed > fastest.top_speed ? current : fastest
  )
)

const lowestStallAircraft = computed(() => 
  props.aircraft.reduce((lowest, current) => 
    current.clean_stall_speed < lowest.clean_stall_speed ? current : lowest
  )
)

const mostSeatsAircraft = computed(() => 
  props.aircraft.reduce((most, current) => 
    current.seating_capacity > most.seating_capacity ? current : most
  )
)

const getStallSpeedClass = (stallSpeed) => {
  if (stallSpeed <= 59) return 'stall-sport-pilot'
  if (stallSpeed <= 61) return 'stall-private-pilot'
  return 'stall-not-mosaic'
}
</script>

<style scoped>
.comparison-view {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  overflow-y: auto;
}

.comparison-view .card {
  width: 100%;
  max-width: 1400px;
  max-height: 90vh;
  overflow-y: auto;
  margin: 0;
}

.comparison-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.comparison-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.aircraft-card {
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  padding: 1.5rem;
  background-color: var(--bg-secondary);
}

.aircraft-header {
  text-align: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.aircraft-image-preview {
  margin-bottom: 1rem;
  display: flex;
  justify-content: center;
}

.aircraft-thumbnail {
  width: 120px;
  height: 80px;
  object-fit: cover;
  border-radius: 0.375rem;
  border: 1px solid var(--border-color);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.no-image-placeholder {
  width: 120px;
  height: 80px;
  border: 2px dashed var(--border-color);
  border-radius: 0.375rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--bg-tertiary);
}

.no-image-text {
  color: var(--text-secondary);
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.aircraft-header h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
}

.aircraft-name-link {
  color: var(--text-accent);
  text-decoration: none;
  transition: color 0.2s ease;
}

.aircraft-name-link:hover {
  color: var(--text-primary);
  text-decoration: underline;
}

.certification-year {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.eligibility-section,
.specs-section,
.config-section,
.mosaic-notes {
  margin-bottom: 1.5rem;
}

.eligibility-section h5,
.specs-section h5,
.config-section h5,
.mosaic-notes h5 {
  margin: 0 0 1rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.eligibility-badges {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.badge.large {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  font-weight: 600;
  text-align: center;
}

.endorsements {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
  margin-top: 0.5rem;
}

.specs-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.spec-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 0.75rem;
  background-color: var(--bg-primary);
  border-radius: 0.375rem;
  border: 1px solid var(--border-color);
}

.spec-label {
  font-weight: 500;
  color: var(--text-primary);
  font-size: 0.875rem;
}

.spec-value {
  text-align: right;
  font-weight: 600;
  color: var(--text-primary);
}

.spec-value.highlight {
  color: var(--text-accent);
}

.spec-value.stall-sport-pilot {
  color: var(--success-color);
}

.spec-value.stall-private-pilot {
  color: var(--warning-color);
}

.spec-value.stall-not-mosaic {
  color: var(--danger-color);
}

.spec-note {
  font-size: 0.75rem;
  font-weight: 400;
  color: var(--text-secondary);
  margin-top: 0.25rem;
}

.config-grid {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.config-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--border-color);
}

.config-item:last-child {
  border-bottom: none;
}

.config-label {
  font-weight: 500;
  color: var(--text-secondary);
}

.config-value {
  font-weight: 600;
  color: var(--text-primary);
}

.notes-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.notes-list li {
  padding: 0.375rem 0;
  font-size: 0.875rem;
  color: var(--text-secondary);
  border-left: 3px solid var(--success-color);
  padding-left: 0.75rem;
  margin-bottom: 0.5rem;
}

.comparison-summary {
  border-top: 1px solid var(--border-color);
  padding-top: 2rem;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.summary-item {
  text-align: center;
  padding: 1rem;
  background-color: var(--bg-secondary);
  border-radius: 0.375rem;
  border: 1px solid var(--border-color);
}

.summary-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
}

.summary-value {
  font-weight: 600;
  color: var(--text-accent);
  font-size: 0.875rem;
}

/* Mobile responsive */
@media (max-width: 768px) {
  .comparison-view {
    padding: 0.5rem;
  }

  .comparison-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .aircraft-card {
    padding: 1rem;
  }

  .comparison-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .summary-grid {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }

  .spec-item {
    flex-direction: column;
    gap: 0.5rem;
    text-align: left;
  }

  .spec-value {
    text-align: left;
  }
}

@media (max-width: 480px) {
  .comparison-view .card {
    margin: 0;
    border-radius: 0;
    max-height: 100vh;
  }

  .aircraft-header h4 {
    font-size: 1.1rem;
  }

  .badge.large {
    padding: 0.375rem 0.75rem;
    font-size: 0.75rem;
  }
}
</style>