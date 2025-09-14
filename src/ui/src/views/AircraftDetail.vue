<template>
  <div class="aircraft-detail-container">
    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>Loading aircraft details...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-container">
      <div class="card">
        <h3>Aircraft Not Found</h3>
        <p>{{ error }}</p>
        <router-link to="/" class="btn btn-primary">← Back to Aircraft List</router-link>
      </div>
    </div>

    <!-- Aircraft Detail Content -->
    <div v-else-if="aircraft" class="aircraft-detail">
      <!-- Header -->
      <div class="aircraft-header">
        <div class="header-content">
          <div class="aircraft-image" v-if="aircraft.image">
            <img :src="aircraft.image" :alt="`${aircraft.manufacturer_name} ${aircraft.model}`" class="header-aircraft-img" />
          </div>
          <div class="aircraft-title">
            <h1>{{ aircraft.manufacturer_name }} {{ aircraft.model }}</h1>
            <div class="eligibility-badges">
              <span 
                v-if="aircraft.sport_pilot_eligible" 
                class="badge badge-success"
                title="Sport Pilot Eligible - Stall speed ≤59 knots"
              >
                Sport Pilot Eligible
              </span>
              <span 
                v-else-if="aircraft.is_mosaic_compliant" 
                class="badge badge-warning"
                title="Private Pilot Required - Stall speed 59-61 knots"
              >
                Private Pilot Required
              </span>
              <span 
                v-else 
                class="badge badge-danger"
                title="Not MOSAIC Compliant - Stall speed >61 knots"
              >
                Not MOSAIC Eligible
              </span>
              <span 
                v-if="aircraft.retractable_gear" 
                class="badge badge-info"
                title="Retractable Landing Gear - Endorsement Required for Sport Pilots"
              >
                Retractable Gear
              </span>
              <span 
                v-if="aircraft.variable_pitch_prop" 
                class="badge badge-info"
                title="Variable Pitch Propeller - Endorsement Required for Sport Pilots"
              >
                Variable Pitch Prop
              </span>
            </div>
          </div>
          <div class="header-actions">
            <router-link to="/" class="btn btn-secondary">← Back to List</router-link>
            <button 
              v-if="hasPendingCorrections" 
              @click="submitAllCorrections" 
              class="btn btn-success correction-button"
              :disabled="submittingCorrection"
            >
              <span class="correction-icon">💾</span>
              {{ submittingCorrection ? 'Submitting...' : `Submit ${Object.keys(pendingCorrections).length} Correction${Object.keys(pendingCorrections).length > 1 ? 's' : ''}` }}
            </button>
          </div>
        </div>
      </div>

      <!-- Aircraft Specifications -->
      <div class="specifications-grid">
        <!-- Aircraft Information -->
        <div class="card spec-card full-width">
          <h3>Aircraft Information</h3>
          
          <!-- MOSAIC Eligibility Summary -->
          <div class="mosaic-summary">
            <div class="eligibility-badge" :class="getMosaicEligibilityClass(aircraft)">
              {{ getMosaicEligibilityText(aircraft) }}
            </div>
            <div class="key-specs">
              <span v-if="aircraft.clean_stall_speed" class="key-spec">
                Stall: {{ aircraft.clean_stall_speed }}kt
              </span>
              <span v-if="aircraft.max_takeoff_weight" class="key-spec">
                MTOW: {{ aircraft.max_takeoff_weight.toLocaleString() }} lbs
              </span>
              <span class="key-spec">
                Seats: {{ aircraft.seating_capacity }}
              </span>
            </div>
          </div>

          <!-- 2x2 Grid Layout -->
          <div class="aircraft-info-grid">
            <!-- Top Left: Flight Envelope -->
            <div class="info-section">
              <h4>Flight Envelope</h4>
              <div class="spec-table">
                <div class="spec-row">
                  <div class="spec-label">Clean Stall (Vs1)</div>
                  <div class="spec-value">
                    <EditableField
                      field-name="clean_stall_speed"
                      :current-value="`${aircraft.clean_stall_speed} knots CAS`"
                      display-name="stall speed"
                      :is-editing="editingField === 'clean_stall_speed'"
                      :edit-form="editForm"
                      @start-edit="startEdit"
                      @save-edit="saveEdit"
                      @cancel-edit="cancelEdit"
                      class="inline-edit"
                    >
                      <strong>{{ aircraft.clean_stall_speed }}kt</strong>
                      <span class="spec-note">{{ getStallSpeedNote(aircraft.clean_stall_speed) }}</span>
                    </EditableField>
                  </div>
                </div>
                <div class="spec-row" v-if="aircraft.vs0_speed">
                  <div class="spec-label">Landing Stall (Vs0)</div>
                  <div class="spec-value">
                    <EditableField
                      field-name="vs0_speed"
                      :current-value="`${aircraft.vs0_speed} knots`"
                      display-name="Vs0 speed"
                      :is-editing="editingField === 'vs0_speed'"
                      :edit-form="editForm"
                      @start-edit="startEdit"
                      @save-edit="saveEdit"
                      @cancel-edit="cancelEdit"
                      class="inline-edit"
                    >
                      {{ aircraft.vs0_speed }}kt
                      <span class="spec-note">Full flaps, landing gear down</span>
                    </EditableField>
                  </div>
                </div>
                <div class="spec-row">
                  <div class="spec-label">Maneuvering (Va)</div>
                  <div class="spec-value">
                    <EditableField
                      field-name="maneuvering_speed"
                      :current-value="`${aircraft.maneuvering_speed} knots`"
                      display-name="maneuvering speed"
                      :is-editing="editingField === 'maneuvering_speed'"
                      :edit-form="editForm"
                      @start-edit="startEdit"
                      @save-edit="saveEdit"
                      @cancel-edit="cancelEdit"
                      class="inline-edit"
                    >
                      {{ aircraft.maneuvering_speed }}kt
                    </EditableField>
                  </div>
                </div>
                <div class="spec-row" v-if="aircraft.vno_speed">
                  <div class="spec-label">Normal Ops (Vno)</div>
                  <div class="spec-value">
                    <EditableField
                      field-name="vno_speed"
                      :current-value="`${aircraft.vno_speed} knots`"
                      display-name="Vno speed"
                      :is-editing="editingField === 'vno_speed'"
                      :edit-form="editForm"
                      @start-edit="startEdit"
                      @save-edit="saveEdit"
                      @cancel-edit="cancelEdit"
                      class="inline-edit"
                    >
                      {{ aircraft.vno_speed }}kt
                    </EditableField>
                  </div>
                </div>
                <div class="spec-row" v-if="aircraft.vne_speed">
                  <div class="spec-label">Never Exceed (Vne)</div>
                  <div class="spec-value">
                    <EditableField
                      field-name="vne_speed"
                      :current-value="`${aircraft.vne_speed} knots`"
                      display-name="Vne speed"
                      :is-editing="editingField === 'vne_speed'"
                      :edit-form="editForm"
                      @start-edit="startEdit"
                      @save-edit="saveEdit"
                      @cancel-edit="cancelEdit"
                      class="inline-edit"
                    >
                      <span class="text-danger">{{ aircraft.vne_speed }}kt</span>
                      <span class="spec-note text-danger">Never exceed this speed</span>
                    </EditableField>
                  </div>
                </div>
                <div class="spec-row">
                  <div class="spec-label">Top Speed</div>
                  <div class="spec-value">
                    <EditableField
                      field-name="top_speed"
                      :current-value="`${aircraft.top_speed} knots`"
                      display-name="top speed"
                      :is-editing="editingField === 'top_speed'"
                      :edit-form="editForm"
                      @start-edit="startEdit"
                      @save-edit="saveEdit"
                      @cancel-edit="cancelEdit"
                      class="inline-edit"
                    >
                      {{ aircraft.top_speed }}kt
                    </EditableField>
                  </div>
                </div>
              </div>
            </div>

            <!-- Top Right: Performance Speeds -->
            <div class="info-section">
              <h4>Performance Speeds</h4>
              <div class="spec-table">
                <div class="spec-row" v-if="aircraft.vx_speed">
                  <div class="spec-label">Best Angle Climb (Vx)</div>
                  <div class="spec-value">
                    <EditableField
                      field-name="vx_speed"
                      :current-value="`${aircraft.vx_speed} knots`"
                      display-name="Vx speed"
                      :is-editing="editingField === 'vx_speed'"
                      :edit-form="editForm"
                      @start-edit="startEdit"
                      @save-edit="saveEdit"
                      @cancel-edit="cancelEdit"
                      class="inline-edit"
                    >
                      {{ aircraft.vx_speed }}kt
                    </EditableField>
                  </div>
                </div>
                <div class="spec-row" v-if="aircraft.vy_speed">
                  <div class="spec-label">Best Rate Climb (Vy)</div>
                  <div class="spec-value">
                    <EditableField
                      field-name="vy_speed"
                      :current-value="`${aircraft.vy_speed} knots`"
                      display-name="Vy speed"
                      :is-editing="editingField === 'vy_speed'"
                      :edit-form="editForm"
                      @start-edit="startEdit"
                      @save-edit="saveEdit"
                      @cancel-edit="cancelEdit"
                      class="inline-edit"
                    >
                      {{ aircraft.vy_speed }}kt
                    </EditableField>
                  </div>
                </div>
                <div class="spec-row" v-if="aircraft.vg_speed">
                  <div class="spec-label">Best Glide (Vg)</div>
                  <div class="spec-value">
                    <EditableField
                      field-name="vg_speed"
                      :current-value="`${aircraft.vg_speed} knots`"
                      display-name="Vg speed"
                      :is-editing="editingField === 'vg_speed'"
                      :edit-form="editForm"
                      @start-edit="startEdit"
                      @save-edit="saveEdit"
                      @cancel-edit="cancelEdit"
                      class="inline-edit"
                    >
                      {{ aircraft.vg_speed }}kt
                    </EditableField>
                  </div>
                </div>
                <div class="spec-row" v-if="aircraft.vfe_speed">
                  <div class="spec-label">Max Flaps Extended (Vfe)</div>
                  <div class="spec-value">
                    <EditableField
                      field-name="vfe_speed"
                      :current-value="`${aircraft.vfe_speed} knots`"
                      display-name="Vfe speed"
                      :is-editing="editingField === 'vfe_speed'"
                      :edit-form="editForm"
                      @start-edit="startEdit"
                      @save-edit="saveEdit"
                      @cancel-edit="cancelEdit"
                      class="inline-edit"
                    >
                      {{ aircraft.vfe_speed }}kt
                    </EditableField>
                  </div>
                </div>
                <div class="spec-row" v-if="aircraft.cruise_speed">
                  <div class="spec-label">Cruise Speed</div>
                  <div class="spec-value">
                    <EditableField
                      field-name="cruise_speed"
                      :current-value="`${aircraft.cruise_speed} knots`"
                      display-name="cruise speed"
                      :is-editing="editingField === 'cruise_speed'"
                      :edit-form="editForm"
                      @start-edit="startEdit"
                      @save-edit="saveEdit"
                      @cancel-edit="cancelEdit"
                      class="inline-edit"
                    >
                      {{ aircraft.cruise_speed }}kt
                      <span class="spec-note">75% power at optimal altitude</span>
                    </EditableField>
                  </div>
                </div>
              </div>
            </div>

            <!-- Bottom Left: Aircraft Limits -->
            <div class="info-section">
              <h4>Aircraft Limits</h4>
              <div class="spec-table">
                <div class="spec-row">
                  <div class="spec-label">Maximum Takeoff Weight</div>
                  <div class="spec-value">
                    <EditableField
                      field-name="max_takeoff_weight"
                      :current-value="aircraft.max_takeoff_weight ? `${aircraft.max_takeoff_weight} lbs` : 'Not specified'"
                      display-name="takeoff weight"
                      :is-editing="editingField === 'max_takeoff_weight'"
                      :edit-form="editForm"
                      @start-edit="startEdit"
                      @save-edit="saveEdit"
                      @cancel-edit="cancelEdit"
                      class="inline-edit"
                    >
                      {{ aircraft.max_takeoff_weight ? `${aircraft.max_takeoff_weight.toLocaleString()} lbs` : 'Not specified' }}
                    </EditableField>
                  </div>
                </div>
                <div class="spec-row">
                  <div class="spec-label">Seating Capacity</div>
                  <div class="spec-value">
                    <EditableField
                      field-name="seating_capacity"
                      :current-value="`${aircraft.seating_capacity} seats`"
                      display-name="seating capacity"
                      :is-editing="editingField === 'seating_capacity'"
                      :edit-form="editForm"
                      @start-edit="startEdit"
                      @save-edit="saveEdit"
                      @cancel-edit="cancelEdit"
                      class="inline-edit"
                    >
                      {{ aircraft.seating_capacity }} seats
                      <span v-if="aircraft.sport_pilot_eligible && aircraft.seating_capacity > 2" class="spec-note">
                        (Sport pilots limited to 1 passenger)
                      </span>
                    </EditableField>
                  </div>
                </div>
              </div>
            </div>

            <!-- Bottom Right: Certification Information -->
            <div class="info-section">
              <h4>Certification</h4>
              <div class="spec-table">
                <div class="spec-row">
                  <div class="spec-label">Certification Date</div>
                  <div class="spec-value">
                    {{ aircraft.certification_date ? formatDate(aircraft.certification_date) : 'Not specified' }}
                    <span v-if="aircraft.certification_date" class="spec-note">
                      {{ getCertificationNote(aircraft.certification_date) }}
                    </span>
                  </div>
                </div>
                <div class="spec-row">
                  <div class="spec-label">MOSAIC Compliant</div>
                  <div class="spec-value">
                    {{ aircraft.is_mosaic_compliant ? 'Yes' : 'No' }}
                  </div>
                </div>
                <div class="spec-row">
                  <div class="spec-label">Sport Pilot Eligible</div>
                  <div class="spec-value">
                    {{ aircraft.sport_pilot_eligible ? 'Yes' : 'No' }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Airspeed Gauge -->
        <!-- TODO: Re-enable airspeed gauge later -->
        <!--
        <div class="card spec-card">
          <AirspeedGauge
            :stall-speed="aircraft.clean_stall_speed"
            :cruise-speed="aircraft.cruise_speed"
            :maneuvering-speed="aircraft.maneuvering_speed"
            :max-speed="aircraft.top_speed"
          />
        </div>
        -->

        <!-- AMP Ad -->
        <div class="card spec-card full-width ad-container">
          <amp-ad width="100vw" height="320"
               type="adsense"
               data-ad-client="ca-pub-6080657940765418"
               data-ad-slot="3049559222"
               data-auto-format="rspv"
               data-full-width="">
            <div overflow=""></div>
          </amp-ad>
        </div>

        <!-- Engine Configurations -->
        <div v-if="aircraft.engines && aircraft.engines.length > 0" class="card spec-card full-width">
          <h3>Available Engine Configurations</h3>
          <div class="engine-impact-note">
            <p><strong>Note:</strong> Different engine configurations may affect aircraft performance and MOSAIC eligibility. Each configuration is listed with its impact on sport pilot eligibility.</p>
          </div>
          <div class="engines-grid">
            <div v-for="engine in aircraft.engines" :key="engine.id" class="engine-card">
              <div class="engine-header">
                <h4>{{ engine.manufacturer }} {{ engine.model }}</h4>
                <div class="engine-eligibility">
                  <span 
                    v-if="getEngineEligibilityImpact(engine).eligible" 
                    class="badge badge-success engine-badge"
                    :title="getEngineEligibilityImpact(engine).reason"
                  >
                    Sport Pilot OK
                  </span>
                  <span 
                    v-else-if="getEngineEligibilityImpact(engine).mosaic" 
                    class="badge badge-warning engine-badge"
                    :title="getEngineEligibilityImpact(engine).reason"
                  >
                    Private Pilot
                  </span>
                  <span 
                    v-else 
                    class="badge badge-danger engine-badge"
                    :title="getEngineEligibilityImpact(engine).reason"
                  >
                    Not MOSAIC
                  </span>
                </div>
              </div>
              
              <div class="engine-specs">
                <div class="engine-spec-row">
                  <div class="engine-spec">
                    <label>Power Output</label>
                    <span class="spec-highlight">{{ engine.horsepower }} hp</span>
                  </div>
                  <div class="engine-spec">
                    <label>Displacement</label>
                    <span>{{ engine.displacement_liters }}L</span>
                  </div>
                </div>
                
                <div class="engine-spec-row">
                  <div class="engine-spec">
                    <label>Fuel Type</label>
                    <span>{{ formatFuelType(engine.fuel_type) }}</span>
                  </div>
                  <div class="engine-spec">
                    <label>Fuel System</label>
                    <span>{{ engine.is_fuel_injected ? 'Fuel Injected' : 'Carbureted' }}</span>
                  </div>
                </div>
                
                <div class="engine-spec-row">
                  <div class="engine-spec">
                    <label>Engine Type</label>
                    <span>{{ formatEngineType(engine.engine_type) }}</span>
                  </div>
                </div>
              </div>
              
              <!-- Engine-specific performance impact -->
              <div class="engine-impact">
                <div class="impact-section">
                  <h5>Performance Impact</h5>
                  <ul class="impact-list">
                    <li v-if="engine.horsepower > 180">Higher power may affect handling characteristics</li>
                    <li v-if="engine.fuel_type === 'MOGAS'">Can use automotive gasoline (typically lower cost)</li>
                    <li v-if="engine.is_fuel_injected">Fuel injection provides better fuel distribution</li>
                    <li v-if="!engine.is_fuel_injected">Carbureted engine - simpler maintenance</li>
                    <li v-if="engine.displacement_liters > 5">Larger displacement - more power, higher fuel consumption</li>
                  </ul>
                </div>
                
                <div class="impact-section">
                  <h5>MOSAIC Considerations</h5>
                  <p class="impact-explanation">{{ getEngineEligibilityImpact(engine).explanation }}</p>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Multi-engine comparison note -->
          <div v-if="aircraft.engines.length > 1" class="engine-comparison-note">
            <h4>Engine Configuration Impact</h4>
            <p>This aircraft model was offered with multiple engine options. The engine choice can affect:</p>
            <ul>
              <li><strong>Performance characteristics</strong> - Different power outputs and fuel consumption</li>
              <li><strong>Operating costs</strong> - Fuel type, maintenance complexity, and parts availability</li>
              <li><strong>MOSAIC eligibility</strong> - While the airframe determines basic eligibility, engine choice affects overall performance</li>
              <li><strong>Training requirements</strong> - Some configurations may require additional endorsements</li>
            </ul>
          </div>
        </div>

        <!-- Data Verification -->
        <div v-if="aircraft.verification_source" class="card spec-card full-width">
          <h3>Data Verification</h3>
          <div class="verification-content">
            <p>{{ aircraft.verification_source }}</p>
            <div class="verification-note">
              <small>
                <strong>Note:</strong> This data has been verified against official documentation. 
                If you notice any errors, please use the "Suggest Correction" button above.
              </small>
            </div>
          </div>
        </div>
      </div>

      <!-- MOSAIC Information -->
      <div class="mosaic-info card">
        <h3>MOSAIC Regulation Impact</h3>
        <div class="mosaic-content">
          <div v-if="aircraft.sport_pilot_eligible" class="mosaic-eligible">
            <h4>✅ Sport Pilot Eligible (Effective October 22, 2025)</h4>
            <ul>
              <li>Can be flown with a sport pilot certificate</li>
              <li>Sport pilots are limited to 1 passenger regardless of aircraft seating</li>
              <li v-if="aircraft.retractable_gear || aircraft.variable_pitch_prop">
                Endorsements required for: 
                <span v-if="aircraft.retractable_gear">retractable landing gear</span>
                <span v-if="aircraft.retractable_gear && aircraft.variable_pitch_prop">, </span>
                <span v-if="aircraft.variable_pitch_prop">variable pitch propeller</span>
              </li>
              <li>No medical certificate required (driver's license valid)</li>
            </ul>
          </div>
          <div v-else-if="aircraft.is_mosaic_compliant" class="mosaic-private">
            <h4>⚠️ Private Pilot Required</h4>
            <ul>
              <li>Qualifies as MOSAIC LSA but exceeds sport pilot limits</li>
              <li>Requires private pilot certificate or higher</li>
              <li>Medical certificate required</li>
            </ul>
          </div>
          <div v-else class="mosaic-non-eligible">
            <h4>❌ Not MOSAIC Compliant</h4>
            <ul>
              <li>Stall speed exceeds 61 knots (MOSAIC LSA limit)</li>
              <li>Requires private pilot certificate or higher</li>
              <li>Medical certificate required</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Pending Corrections Summary -->
    <div v-if="hasPendingCorrections" class="pending-corrections-summary">
      <div class="card">
        <h4>Pending Corrections</h4>
        <div class="corrections-list">
          <div v-for="(correction, fieldName) in pendingCorrections" :key="fieldName" class="correction-item">
            <div class="correction-details">
              <strong>{{ getFieldDisplayName(fieldName) }}</strong>
              <div class="correction-change">
                <span class="current-value">{{ correction.current_value }}</span>
                <span class="arrow">→</span>
                <span class="suggested-value">{{ correction.suggested_value }}</span>
              </div>
              <div class="correction-reason">{{ correction.reason }}</div>
            </div>
            <button @click="clearCorrection(fieldName)" class="btn-remove" title="Remove this correction">
              ✕
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { mdiPencil } from '@mdi/js'
import MdiIcon from '../components/MdiIcon.vue'
import EditableField from '../components/EditableField.vue'
import AirspeedGauge from '../components/AirspeedGauge.vue'
import { apiRequest } from '../utils/api.js'

const route = useRoute()
const router = useRouter()

// Data state
const aircraft = ref(null)
const loading = ref(true)
const error = ref(null)
const submittingCorrection = ref(false)

// Inline correction state
const pendingCorrections = ref({})
const showCorrectionModal = ref(false)
const currentEditField = ref(null)
const showEditIcon = ref(null)
const editingField = ref(null)
const editForm = ref({
  suggested_value: '',
  reason: '',
  source_documentation: ''
})

// Computed property to check if any corrections are pending
const hasPendingCorrections = computed(() => Object.keys(pendingCorrections.value).length > 0)

// Computed properties
const aircraftId = computed(() => route.params.id)

// Methods
const fetchAircraftDetail = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await apiRequest(`/v1/aircraft/${aircraftId.value}/`)
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Aircraft not found')
      }
      throw new Error('Failed to load aircraft details')
    }
    
    aircraft.value = await response.json()
  } catch (err) {
    console.error('Error fetching aircraft detail:', err)
    error.value = err.message
  } finally {
    loading.value = false
  }
}

// Inline editing functions
const startEdit = (fieldName, currentValue) => {
  editingField.value = fieldName
  editForm.value = {
    suggested_value: currentValue,
    reason: '',
    source_documentation: ''
  }
}

const cancelEdit = () => {
  editingField.value = null
  editForm.value = {
    suggested_value: '',
    reason: '',
    source_documentation: ''
  }
}

const saveEdit = (fieldName, currentValue, formData) => {
  // Add to pending corrections
  pendingCorrections.value[fieldName] = {
    field_name: fieldName,
    current_value: currentValue,
    suggested_value: formData.suggested_value,
    reason: formData.reason,
    source_documentation: formData.source_documentation || ''
  }
  
  // Reset editing state
  cancelEdit()
}

const getFieldDisplayName = (fieldName) => {
  const displayNames = {
    'clean_stall_speed': 'Clean Stall Speed',
    'top_speed': 'Top Speed',
    'maneuvering_speed': 'Maneuvering Speed',
    'cruise_speed': 'Cruise Speed',
    'vx_speed': 'Best Angle of Climb Speed (Vx)',
    'vy_speed': 'Best Rate of Climb Speed (Vy)',
    'vs0_speed': 'Stall Speed Landing Configuration (Vs0)',
    'vg_speed': 'Best Glide Speed (Vg)',
    'vfe_speed': 'Maximum Flap Extended Speed (Vfe)',
    'vno_speed': 'Maximum Structural Cruising Speed (Vno)',
    'vne_speed': 'Never Exceed Speed (Vne)',
    'max_takeoff_weight': 'Maximum Takeoff Weight',
    'seating_capacity': 'Seating Capacity',
    'certification_date': 'Certification Date',
    'retractable_gear': 'Retractable Gear',
    'variable_pitch_prop': 'Variable Pitch Propeller',
    'verification_source': 'Verification Source'
  }
  return displayNames[fieldName] || fieldName
}

const clearCorrection = (fieldName) => {
  delete pendingCorrections.value[fieldName]
}

const submitAllCorrections = async () => {
  if (!aircraft.value || Object.keys(pendingCorrections.value).length === 0) return
  
  submittingCorrection.value = true
  
  try {
    const submitterName = prompt('Your name (optional):') || ''
    const submitterEmail = prompt('Your email (optional):') || ''
    
    // Submit each correction
    const submissions = Object.values(pendingCorrections.value).map(correction => 
      apiRequest('/v1/corrections/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          aircraft: aircraft.value.id,
          submitter_name: submitterName,
          submitter_email: submitterEmail,
          ...correction
        })
      })
    )
    
    const results = await Promise.all(submissions)
    const failedSubmissions = results.filter(r => !r.ok)
    
    if (failedSubmissions.length > 0) {
      throw new Error(`${failedSubmissions.length} corrections failed to submit`)
    }
    
    // Reset state
    pendingCorrections.value = {}
    showCorrectionModal.value = false
    
    // Show success message
    alert(`Thank you! ${results.length} correction${results.length > 1 ? 's' : ''} submitted for review.`)
    
  } catch (err) {
    console.error('Error submitting corrections:', err)
    alert('Some corrections failed to submit. Please try again.')
  } finally {
    submittingCorrection.value = false
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
}

const formatFuelType = (fuelType) => {
  const types = {
    'AVGAS': 'Avgas (100LL/91UL)',
    'MOGAS': 'Automotive gasoline',
    'DIESEL': 'Jet A / Diesel',
    'ELECTRIC': 'Electric'
  }
  return types[fuelType] || fuelType
}

const formatEngineType = (engineType) => {
  const types = {
    'PISTON': 'Piston engine',
    'TURBOPROP': 'Turboprop',
    'ELECTRIC': 'Electric motor'
  }
  return types[engineType] || engineType
}

const getStallSpeedNote = (stallSpeed) => {
  const speed = parseFloat(stallSpeed)
  if (speed <= 59) {
    return 'Sport pilot eligible'
  } else if (speed <= 61) {
    return 'Private pilot required'
  } else {
    return 'Exceeds MOSAIC limits'
  }
}

const getMosaicEligibilityClass = (aircraft) => {
  const stallSpeed = parseFloat(aircraft.clean_stall_speed)
  if (stallSpeed <= 59) {
    return 'sport-pilot-eligible'
  } else if (stallSpeed <= 61) {
    return 'private-pilot-required'
  } else {
    return 'not-mosaic-eligible'
  }
}

const getMosaicEligibilityText = (aircraft) => {
  const stallSpeed = parseFloat(aircraft.clean_stall_speed)
  if (stallSpeed <= 59) {
    return 'Sport Pilot Eligible'
  } else if (stallSpeed <= 61) {
    return 'MOSAIC LSA (Private Pilot Required)'
  } else {
    return 'Not MOSAIC Eligible'
  }
}

const getCertificationNote = (certDate) => {
  const mosaicDate = new Date('2026-07-24')
  const certificationDate = new Date(certDate)
  
  if (certificationDate < mosaicDate) {
    return 'Legacy aircraft - eligible if meets performance requirements'
  } else {
    return 'Must meet MOSAIC LSA standards'
  }
}

const getEngineEligibilityImpact = (engine) => {
  // Engine eligibility is primarily based on the aircraft's stall speed, not the engine itself
  // However, we can provide context about how different engines might affect performance
  
  const baseAircraftEligible = aircraft.value?.sport_pilot_eligible
  const baseAircraftMosaic = aircraft.value?.is_mosaic_compliant
  
  // Determine if this engine configuration might affect eligibility
  const isHighPowerEngine = engine.horsepower > 200
  const isComplexEngine = engine.is_fuel_injected && engine.horsepower > 180
  
  if (baseAircraftEligible) {
    return {
      eligible: true,
      mosaic: true,
      reason: `Compatible with sport pilot eligible ${aircraft.value.manufacturer_name} ${aircraft.value.model}`,
      explanation: `This engine configuration maintains the aircraft's sport pilot eligibility. The ${engine.horsepower}hp ${engine.manufacturer} ${engine.model} provides good performance while staying within MOSAIC limits.`
    }
  } else if (baseAircraftMosaic) {
    return {
      eligible: false,
      mosaic: true,
      reason: `MOSAIC compliant but requires private pilot certificate`,
      explanation: `While this engine works with MOSAIC LSA certification, the aircraft's stall speed requires a private pilot certificate. The ${engine.horsepower}hp configuration provides excellent performance for private pilots.`
    }
  } else {
    return {
      eligible: false,
      mosaic: false,
      reason: `Aircraft exceeds MOSAIC limits regardless of engine`,
      explanation: `This ${engine.horsepower}hp engine configuration cannot make the aircraft MOSAIC compliant due to the airframe's inherent stall speed characteristics. Requires private pilot certificate.`
    }
  }
}

onMounted(() => {
  fetchAircraftDetail()
})
</script>

<style scoped>
.aircraft-detail-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.aircraft-header {
  margin-bottom: 2rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 2rem;
  flex-wrap: wrap;
}

.aircraft-image {
  flex-shrink: 0;
  max-width: 300px;
}

.header-aircraft-img {
  width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 12px var(--shadow);
  object-fit: cover;
  max-height: 200px;
}

.aircraft-title h1 {
  margin: 0 0 1rem 0;
  color: var(--text-primary);
}

.eligibility-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.header-actions {
  display: flex;
  gap: 1rem;
  flex-shrink: 0;
}

.specifications-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.spec-card {
  height: fit-content;
}

.spec-card.full-width {
  grid-column: 1 / -1;
}

.spec-card h3 {
  margin: 0 0 1.5rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--border-color);
}

.spec-grid {
  display: grid;
  gap: 1rem;
}

.spec-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.spec-item label {
  font-weight: 600;
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.spec-value {
  font-size: 1rem;
  color: var(--text-primary);
}

.spec-value strong {
  font-size: 1.125rem;
}

.spec-note {
  display: block;
  font-size: 0.75rem;
  color: var(--text-secondary);
  margin-top: 0.25rem;
}

/* Engine Information */
.engine-impact-note {
  background-color: var(--bg-secondary);
  padding: 1rem;
  border-radius: 0.375rem;
  margin-bottom: 1.5rem;
  border-left: 4px solid var(--text-accent);
}

.engine-impact-note p {
  margin: 0;
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.engines-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
}

.engine-card {
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  background-color: var(--bg-primary);
  box-shadow: 0 2px 4px var(--shadow);
  overflow: hidden;
}

.engine-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1.5rem 1.5rem 1rem 1.5rem;
  background-color: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
}

.engine-header h4 {
  margin: 0;
  color: var(--text-primary);
  font-size: 1.125rem;
}

.engine-eligibility {
  flex-shrink: 0;
  margin-left: 1rem;
}

.engine-badge {
  font-size: 0.75rem;
  padding: 0.375rem 0.75rem;
  white-space: nowrap;
}

.engine-specs {
  padding: 1.5rem;
}

.engine-spec-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
}

.engine-spec-row:last-child {
  margin-bottom: 0;
}

.engine-spec {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.engine-spec label {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.engine-spec span {
  font-size: 0.875rem;
  color: var(--text-primary);
}

.spec-highlight {
  font-weight: 600;
  color: var(--text-accent) !important;
  font-size: 1rem !important;
}

.engine-impact {
  padding: 1.5rem;
  background-color: var(--bg-secondary);
  border-top: 1px solid var(--border-color);
}

.impact-section {
  margin-bottom: 1.5rem;
}

.impact-section:last-child {
  margin-bottom: 0;
}

.impact-section h5 {
  margin: 0 0 0.75rem 0;
  font-size: 1rem;
  color: var(--text-primary);
  font-weight: 600;
}

.impact-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.impact-list li {
  position: relative;
  padding-left: 1.25rem;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.impact-list li::before {
  content: '•';
  position: absolute;
  left: 0;
  color: var(--text-accent);
  font-weight: bold;
}

.impact-explanation {
  margin: 0;
  font-size: 0.875rem;
  line-height: 1.5;
  color: var(--text-secondary);
}

.engine-comparison-note {
  margin-top: 2rem;
  padding: 1.5rem;
  background-color: var(--bg-secondary);
  border-radius: 0.5rem;
  border-left: 4px solid var(--warning-color);
}

.engine-comparison-note h4 {
  margin: 0 0 1rem 0;
  color: var(--text-primary);
}

.engine-comparison-note p {
  margin-bottom: 1rem;
  color: var(--text-secondary);
}

.engine-comparison-note ul {
  margin: 0;
  padding-left: 1.5rem;
}

.engine-comparison-note li {
  margin-bottom: 0.5rem;
  color: var(--text-secondary);
}

/* Data Verification */
.verification-content p {
  margin-bottom: 1rem;
  line-height: 1.6;
}

.verification-note {
  background-color: var(--bg-secondary);
  padding: 1rem;
  border-radius: 0.375rem;
  border-left: 4px solid var(--text-accent);
}

/* MOSAIC Information */
.mosaic-info {
  margin-top: 2rem;
}

.mosaic-content h4 {
  margin: 0 0 1rem 0;
}

.mosaic-eligible h4 {
  color: var(--success-color);
}

.mosaic-private h4 {
  color: var(--warning-color);
}

.mosaic-non-eligible h4 {
  color: var(--danger-color);
}

.mosaic-content ul {
  margin: 0;
  padding-left: 1.5rem;
}

.mosaic-content li {
  margin-bottom: 0.5rem;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background-color: var(--bg-primary);
  border-radius: 0.5rem;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-color);
}

.modal-header h3 {
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--text-secondary);
  padding: 0;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-close:hover {
  color: var(--text-primary);
}

.modal-body {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
}

.form-group textarea,
.form-group input,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 0.375rem;
  background-color: var(--bg-primary);
  color: var(--text-primary);
  font-family: inherit;
}

.form-group textarea:focus,
.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--text-accent);
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding-top: 1rem;
  border-top: 1px solid var(--border-color);
}

/* Loading and Error States */
.loading-container,
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 3rem 0;
  text-align: center;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .aircraft-detail-container {
    padding: 1rem 0.75rem;
  }
  
  .header-content {
    flex-direction: column;
    align-items: flex-start;
  }

  .aircraft-image {
    max-width: 100%;
    order: -1; /* Show image first on mobile */
  }

  .header-aircraft-img {
    max-height: 150px;
  }
  
  .header-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .specifications-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .engines-grid {
    grid-template-columns: 1fr;
  }
  
  .engine-spec-row {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }

  .engine-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
    padding: 1rem;
  }

  .engine-eligibility {
    margin-left: 0;
  }

  .engine-specs,
  .engine-impact {
    padding: 1rem;
  }

  .engine-comparison-note {
    padding: 1rem;
  }
  
  .modal-overlay {
    padding: 0.5rem;
  }
  
  .modal-actions {
    flex-direction: column-reverse;
  }
}

@media (max-width: 480px) {
  .eligibility-badges {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .badge {
    font-size: 0.625rem;
  }
  
  .editable-field {
    padding: 0.125rem 0.25rem;
    gap: 0.25rem;
  }
  
  .edit-icon {
    font-size: 0.75rem;
    padding: 0.125rem;
  }
  
  .correction-button {
    font-size: 0.75rem;
    padding: 0.5rem 0.75rem;
  }
}

/* Inline Editing Styles */
.editable-field {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  transition: background-color 0.2s ease;
  margin: -0.25rem -0.5rem;
}

.editable-field:hover {
  background-color: var(--bg-secondary);
}

.edit-icon {
  background: none;
  border: none;
  font-size: 0.875rem;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 0.25rem;
  opacity: 0.7;
  transition: all 0.2s ease;
  margin-left: 0.5rem;
  flex-shrink: 0;
}

.edit-icon:hover {
  opacity: 1;
  background-color: var(--bg-tertiary);
  transform: scale(1.1);
}

/* Dark mode specific styles for edit icon */
[data-theme="dark"] .edit-icon {
  color: var(--text-primary);
  opacity: 0.8;
}

[data-theme="dark"] .edit-icon:hover {
  color: var(--text-accent);
  opacity: 1;
}

.correction-button {
  animation: pulse 2s infinite;
  box-shadow: 0 0 0 0 rgba(40, 167, 69, 0.7);
}

@keyframes pulse {
  0% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(40, 167, 69, 0.7);
  }
  
  70% {
    transform: scale(1);
    box-shadow: 0 0 0 10px rgba(40, 167, 69, 0);
  }
  
  100% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(40, 167, 69, 0);
  }
}

.correction-icon {
  margin-right: 0.5rem;
}

.pending-corrections-summary {
  background: var(--bg-secondary);
  border: 2px solid var(--accent-color);
  border-radius: 8px;
  padding: 1rem;
  margin: 1rem 0;
  box-shadow: 0 2px 8px var(--shadow);
}

.corrections-list {
  max-height: 200px;
  overflow-y: auto;
  margin-bottom: 1rem;
}

.correction-item {
  padding: 0.5rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  margin-bottom: 0.5rem;
  background: var(--bg-primary);
  position: relative;
}

.correction-details {
  font-size: 0.9rem;
}

.correction-change {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0.25rem 0;
}

.current-value {
  color: var(--text-secondary);
  text-decoration: line-through;
}

.suggested-value {
  color: var(--success-color);
  font-weight: 500;
}

.arrow {
  color: var(--accent-color);
  font-weight: bold;
}

.correction-reason {
  font-style: italic;
  color: var(--text-secondary);
  margin-top: 0.25rem;
}

.btn-remove {
  background: var(--error-color);
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.25rem 0.5rem;
  font-size: 0.8rem;
  cursor: pointer;
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
}

.btn-remove:hover {
  background: #c53030;
}

/* Inline Edit Form Styles */
.edit-form {
  background: var(--bg-secondary);
  border: 2px solid var(--accent-color);
  border-radius: 6px;
  padding: 1rem;
  margin: 0.5rem 0;
}

.edit-inputs {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.edit-input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background-color: var(--bg-primary);
  color: var(--text-primary);
  font-family: inherit;
  font-size: 0.9rem;
}

.edit-input:focus {
  outline: none;
  border-color: var(--accent-color);
  box-shadow: 0 0 0 2px rgba(77, 166, 255, 0.2);
}

.edit-input::placeholder {
  color: var(--text-secondary);
}

.edit-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

.btn-save, .btn-cancel {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  font-size: 0.875rem;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-save {
  background: var(--success-color);
  color: white;
}

.btn-save:hover {
  background: #45a049;
}

.btn-cancel {
  background: var(--text-secondary);
  color: white;
}

.btn-cancel:hover {
  background: #666;
}

/* Mobile responsive for edit form */
@media (max-width: 768px) {
  .edit-inputs {
    gap: 0.5rem;
  }
  
  .edit-input {
    font-size: 16px; /* Prevent zoom on iOS */
  }
  
  .edit-actions {
    flex-direction: column;
  }
  
  .btn-save, .btn-cancel {
    width: 100%;
    padding: 0.75rem;
  }
}

/* Performance Specifications - New Layout */
.mosaic-summary {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
  padding: 1rem;
  background-color: var(--bg-tertiary);
  border-radius: 0.5rem;
  border: 1px solid var(--border-color);
  flex-wrap: wrap;
  gap: 1rem;
}

.eligibility-badge {
  padding: 0.5rem 1rem;
  border-radius: 1.5rem;
  font-weight: 600;
  font-size: 0.875rem;
  text-align: center;
  flex: 0 0 auto;
}

.eligibility-badge.sport-pilot-eligible {
  background-color: var(--success-color);
  color: white;
}

.eligibility-badge.private-pilot-required {
  background-color: var(--warning-color);
  color: white;
}

.eligibility-badge.not-mosaic-eligible {
  background-color: var(--danger-color);
  color: white;
}

.key-specs {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.key-spec {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 1rem;
}

.aircraft-info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto auto;
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.info-section {
  background-color: var(--bg-secondary);
  border-radius: 0.5rem;
  border: 1px solid var(--border-light);
  padding: 1rem;
}

.info-section h4 {
  margin: 0 0 0.75rem 0;
  color: var(--text-primary);
  font-weight: 600;
  font-size: 1.1rem;
  border-bottom: 2px solid var(--border-color);
  padding-bottom: 0.5rem;
}

.spec-table {
  display: grid;
  gap: 0.5rem;
}

.spec-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  padding: 0.5rem 0.75rem;
  background-color: var(--bg-tertiary);
  border-radius: 0.375rem;
  border: 1px solid var(--border-light);
}

.spec-label {
  font-weight: 500;
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.spec-value {
  text-align: right;
  font-weight: 600;
  color: var(--text-primary);
}

.spec-value .inline-edit {
  display: inline-block;
}

.spec-value .spec-note {
  display: block;
  font-weight: 400;
  font-size: 0.75rem;
  margin-top: 0.25rem;
  color: var(--text-secondary);
}

@media (max-width: 768px) {
  .mosaic-summary {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .key-specs {
    width: 100%;
    justify-content: space-between;
  }
  
  .aircraft-info-grid {
    grid-template-columns: 1fr;
    grid-template-rows: auto;
    gap: 1.5rem;
  }
  
  .spec-row {
    grid-template-columns: 1fr;
    gap: 0.5rem;
    text-align: left;
  }
  
  .spec-value {
    text-align: left;
  }
  
  .spec-value .spec-note {
    text-align: left;
  }
}

@media (max-width: 480px) {
  .key-specs {
    flex-direction: column;
    gap: 0.5rem;
  }
}

/* Ad Container Styles */
.ad-container {
  text-align: center;
  margin: 2rem 0;
  border: 1px solid var(--border-light);
  border-radius: 0.5rem;
  padding: 1rem;
  background-color: var(--bg-secondary);
}

.ad-container amp-ad {
  margin: 0 auto;
}

@media (max-width: 768px) {
  .ad-container {
    margin: 1.5rem 0;
    padding: 0.75rem;
  }
}
</style>