<template>
  <div class="airspeed-gauge-container">
    <div class="gauge-wrapper">
      <div class="gauge-canvas">
        <svg width="280" height="280" viewBox="0 0 280 280">
          <!-- Outer bezel -->
          <circle cx="140" cy="140" r="138" fill="#2a2a2a" stroke="#666" stroke-width="4"/>
          
          <!-- Inner face -->
          <circle cx="140" cy="140" r="120" fill="#000" stroke="#333" stroke-width="2"/>
          
          <!-- Major tick marks and numbers -->
          <g v-for="mark in majorMarks" :key="mark.speed">
            <line
              :x1="140 + Math.cos(mark.angle - Math.PI/2) * 100"
              :y1="140 + Math.sin(mark.angle - Math.PI/2) * 100"
              :x2="140 + Math.cos(mark.angle - Math.PI/2) * 85"
              :y2="140 + Math.sin(mark.angle - Math.PI/2) * 85"
              stroke="white"
              stroke-width="2"
            />
            <text
              :x="140 + Math.cos(mark.angle - Math.PI/2) * 75"
              :y="140 + Math.sin(mark.angle - Math.PI/2) * 75"
              text-anchor="middle"
              dominant-baseline="middle"
              fill="white"
              font-family="Arial, sans-serif"
              font-size="16"
              font-weight="bold"
            >
              {{ mark.speed }}
            </text>
          </g>
          
          <!-- Minor tick marks -->
          <g v-for="mark in minorMarks" :key="`minor-${mark.speed}`">
            <line
              :x1="140 + Math.cos(mark.angle - Math.PI/2) * 100"
              :y1="140 + Math.sin(mark.angle - Math.PI/2) * 100"
              :x2="140 + Math.cos(mark.angle - Math.PI/2) * 92"
              :y2="140 + Math.sin(mark.angle - Math.PI/2) * 92"
              stroke="white"
              stroke-width="1"
            />
          </g>
          
          <!-- Airspeed label -->
          <text
            x="140"
            y="180"
            text-anchor="middle"
            fill="white"
            font-family="Arial, sans-serif"
            font-size="12"
            font-weight="bold"
          >
            AIRSPEED
          </text>
          
          <!-- Knots label -->
          <text
            x="140"
            y="195"
            text-anchor="middle"
            fill="white"
            font-family="Arial, sans-serif"
            font-size="10"
          >
            KNOTS
          </text>
          
          <!-- Center hub -->
          <circle cx="140" cy="140" r="12" fill="#444" stroke="#666" stroke-width="1"/>
          
          <!-- Needle -->
          <g :transform="`rotate(${needleAngle * 180 / Math.PI} 140 140)`">
            <!-- Needle body -->
            <polygon
              points="140,50 142,140 140,145 138,140"
              fill="white"
              stroke="#ccc"
              stroke-width="0.5"
            />
            <!-- Needle tip -->
            <polygon
              points="138,50 142,50 140,45"
              fill="white"
            />
          </g>
          
          <!-- Center dot -->
          <circle cx="140" cy="140" r="4" fill="white"/>
        </svg>
      </div>
      
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'

const props = defineProps({
  stallSpeed: {
    type: [Number, String],
    required: true
  },
  cruiseSpeed: {
    type: [Number, String],
    default: null
  },
  maneuveringSpeed: {
    type: [Number, String],
    default: null
  },
  maxSpeed: {
    type: [Number, String], 
    default: null
  }
})

// Convert string props to numbers
const stallSpeed = computed(() => parseFloat(props.stallSpeed))
const cruiseSpeed = computed(() => props.cruiseSpeed ? parseFloat(props.cruiseSpeed) : null)
const maneuveringSpeed = computed(() => props.maneuveringSpeed ? parseFloat(props.maneuveringSpeed) : null)
const maxSpeed = computed(() => props.maxSpeed ? parseFloat(props.maxSpeed) : null)

const currentSpeed = ref(0)
let animationId = null

// Calculate maximum scale for the gauge (at least 40 knots above top speed, minimum 200)
const maxScale = computed(() => {
  const topSpeed = maxSpeed.value || 160
  const minScaleFromTopSpeed = topSpeed + 40
  const minScale = Math.max(minScaleFromTopSpeed, 200)
  return Math.ceil(minScale / 20) * 20
})

// Generate major tick marks (every 20 knots)
const majorMarks = computed(() => {
  const marks = []
  for (let speed = 40; speed <= maxScale.value; speed += 20) {
    // Start at 0° (12 o'clock, pointing up) and sweep 340° clockwise to 340°
    const angle = (0 + (speed / maxScale.value) * 340) * Math.PI / 180
    marks.push({ speed, angle })
  }
  return marks
})

// Generate minor tick marks (every 10 knots)
const minorMarks = computed(() => {
  const marks = []
  for (let speed = 30; speed <= maxScale.value; speed += 10) {
    if (speed % 20 !== 0 && speed >= 30) { // Skip major marks and very low speeds
      // Start at 0° (12 o'clock, pointing up) and sweep 340° clockwise to 340°
      const angle = (0 + (speed / maxScale.value) * 340) * Math.PI / 180
      marks.push({ speed, angle })
    }
  }
  return marks
})

// Calculate needle angle
const needleAngle = computed(() => {
  const normalizedSpeed = Math.max(0, Math.min(currentSpeed.value, maxScale.value))
  // Start at 0° (12 o'clock, pointing up) and sweep 340° clockwise to 340°
  return (0 + (normalizedSpeed / maxScale.value) * 340) * Math.PI / 180
})


// Animation function
const animateToSpeed = (targetSpeed, duration = 2000) => {
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
  
  const startSpeed = currentSpeed.value
  const speedDiff = targetSpeed - startSpeed
  const startTime = Date.now()
  
  const animate = () => {
    const elapsed = Date.now() - startTime
    const progress = Math.min(elapsed / duration, 1)
    
    // Smooth easing
    const easeProgress = 1 - Math.pow(1 - progress, 3) // ease-out cubic
    
    currentSpeed.value = startSpeed + (speedDiff * easeProgress)
    
    if (progress < 1) {
      animationId = requestAnimationFrame(animate)
    }
  }
  
  animate()
}

onMounted(() => {
  // Debug props and calculations
  console.log('AirspeedGauge computed values:', {
    stallSpeed: stallSpeed.value,
    cruiseSpeed: cruiseSpeed?.value, 
    maneuveringSpeed: maneuveringSpeed?.value,
    maxSpeed: maxSpeed?.value,
    maxScaleValue: maxScale.value
  })
  
  console.log('Computed properties exist check:', {
    stallSpeedExists: !!stallSpeed,
    cruiseSpeedExists: !!cruiseSpeed,
    maneuveringSpeedExists: !!maneuveringSpeed,
    maxSpeedExists: !!maxSpeed
  })
  
  console.log('v-if conditions would pass:', {
    maneuveringCondition: maneuveringSpeed && maneuveringSpeed.value,
    yellowArcCondition: maxSpeed && maxSpeed.value && maneuveringSpeed && maneuveringSpeed.value,
    redLineCondition: maxSpeed && maxSpeed.value,
    cruiseLineCondition: cruiseSpeed && cruiseSpeed.value
  })
  
  
  // Animate to cruise speed after loading
  setTimeout(() => {
    if (cruiseSpeed?.value) {
      animateToSpeed(cruiseSpeed.value, 2000)
    } else if (maneuveringSpeed?.value) {
      animateToSpeed(maneuveringSpeed.value, 2000)
    }
  }, 500)
})

onUnmounted(() => {
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
})
</script>

<style scoped>
.airspeed-gauge-container {
  padding: 1.5rem;
  margin: 1rem 0;
}


.gauge-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
}

.gauge-canvas {
  display: flex;
  justify-content: center;
  align-items: center;
}



/* Mobile responsive */
@media (max-width: 768px) {
  .gauge-canvas svg {
    max-width: 100%;
    height: auto;
  }
}

/* SVG styling that works in both themes */
svg {
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
}

[data-theme="dark"] svg text {
  fill: white;
}

[data-theme="light"] svg text {
  fill: white; /* Keep white text on black gauge face */
}
</style>