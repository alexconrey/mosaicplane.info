<template>
  <div class="home">
    <AircraftTable 
      @aircraft-selected="handleAircraftSelection"
      :selected-aircraft="selectedAircraft"
    />
    
    <!-- Compare button -->
    <div class="compare-section" v-if="selectedAircraft.length > 0" role="region" aria-label="Aircraft comparison controls">
      <div class="flex justify-between items-center">
        <p class="text-secondary" aria-live="polite">
          {{ selectedAircraft.length }} aircraft selected
        </p>
        <button 
          @click="compareAircraft" 
          :disabled="selectedAircraft.length < 2"
          class="btn btn-success"
          :aria-label="selectedAircraft.length < 2 ? 'Select at least 2 aircraft to compare' : `Compare ${selectedAircraft.length} selected aircraft`"
        >
          Compare {{ selectedAircraft.length > 1 ? `${selectedAircraft.length} ` : '' }}Aircraft
        </button>
      </div>
    </div>

    <!-- Comparison results -->
    <Transition name="modal-fade">
      <ComparisonView 
        v-if="showComparison"
        :aircraft="comparisonData"
        @close="closeComparison"
        role="dialog"
        aria-modal="true"
        aria-label="Aircraft comparison results"
      />
    </Transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AircraftTable from '../components/AircraftTable.vue'
import ComparisonView from '../components/ComparisonView.vue'
import { apiRequest } from '../utils/api.js'

// Aircraft selection state
const selectedAircraft = ref([])
const showComparison = ref(false)
const comparisonData = ref([])

const handleAircraftSelection = (aircraft) => {
  selectedAircraft.value = aircraft
}

const compareAircraft = async () => {
  if (selectedAircraft.value.length < 2) return
  
  try {
    const ids = selectedAircraft.value.map(a => a.id).join(',')
    const response = await apiRequest(`/v1/aircraft/compare/?ids=${ids}`)
    const data = await response.json()
    
    comparisonData.value = data
    showComparison.value = true
  } catch (error) {
    console.error('Error comparing aircraft:', error)
    alert('Failed to compare aircraft. Please try again.')
  }
}

const closeComparison = () => {
  showComparison.value = false
  comparisonData.value = []
}
</script>

<style scoped>
.compare-section {
  position: sticky;
  bottom: 0;
  background-color: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  padding: 1rem;
  margin: 2rem 0;
  box-shadow: 0 4px 12px var(--shadow);
}

/* Modal fade transition */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: all 0.3s ease;
}

.modal-fade-enter-from {
  opacity: 0;
  transform: translateY(-20px) scale(0.95);
}

.modal-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.98);
}

.modal-fade-enter-to,
.modal-fade-leave-from {
  opacity: 1;
  transform: translateY(0) scale(1);
}
</style>