<template>
  <div 
    ref="containerRef" 
    class="tooltip-container" 
    @mouseenter="showTooltip" 
    @mouseleave="hideTooltip"
  >
    <slot></slot>
    <Teleport to="body">
      <div 
        v-if="visible" 
        ref="tooltipRef"
        class="tooltip"
        :style="tooltipStyle"
        role="tooltip"
      >
        {{ text }}
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'

const props = defineProps({
  text: {
    type: String,
    required: true
  },
  position: {
    type: String,
    default: 'top',
    validator: (value) => ['top', 'bottom', 'left', 'right'].includes(value)
  },
  delay: {
    type: Number,
    default: 300
  }
})

const visible = ref(false)
const containerRef = ref(null)
const tooltipRef = ref(null)
const tooltipStyle = ref({})
let timeoutId = null

const showTooltip = async () => {
  if (timeoutId) clearTimeout(timeoutId)
  timeoutId = setTimeout(async () => {
    visible.value = true
    await nextTick()
    updateTooltipPosition()
  }, props.delay)
}

const hideTooltip = () => {
  if (timeoutId) clearTimeout(timeoutId)
  visible.value = false
}

const updateTooltipPosition = () => {
  if (!containerRef.value || !tooltipRef.value) return
  
  const containerRect = containerRef.value.getBoundingClientRect()
  const tooltipRect = tooltipRef.value.getBoundingClientRect()
  const viewportWidth = window.innerWidth
  const viewportHeight = window.innerHeight
  
  let top, left
  
  switch (props.position) {
    case 'top':
      top = containerRect.top - tooltipRect.height - 8
      left = containerRect.left + (containerRect.width / 2) - (tooltipRect.width / 2)
      break
    case 'bottom':
      top = containerRect.bottom + 8
      left = containerRect.left + (containerRect.width / 2) - (tooltipRect.width / 2)
      break
    case 'left':
      top = containerRect.top + (containerRect.height / 2) - (tooltipRect.height / 2)
      left = containerRect.left - tooltipRect.width - 8
      break
    case 'right':
      top = containerRect.top + (containerRect.height / 2) - (tooltipRect.height / 2)
      left = containerRect.right + 8
      break
    default:
      top = containerRect.top - tooltipRect.height - 8
      left = containerRect.left + (containerRect.width / 2) - (tooltipRect.width / 2)
  }
  
  // Keep tooltip within viewport bounds
  if (left < 8) left = 8
  if (left + tooltipRect.width > viewportWidth - 8) {
    left = viewportWidth - tooltipRect.width - 8
  }
  if (top < 8) top = containerRect.bottom + 8
  if (top + tooltipRect.height > viewportHeight - 8) {
    top = containerRect.top - tooltipRect.height - 8
  }
  
  tooltipStyle.value = {
    position: 'fixed',
    top: `${top}px`,
    left: `${left}px`,
    zIndex: 9999
  }
}
</script>

<style scoped>
.tooltip-container {
  position: relative;
  display: block;
  width: 100%;
}

.tooltip {
  padding: 0.5rem 0.75rem;
  background-color: var(--bg-tertiary);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
  border-radius: 0.375rem;
  font-size: 0.8125rem;
  line-height: 1.3;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
  max-width: 320px;
  white-space: normal;
  word-wrap: break-word;
  min-width: 200px;
  opacity: 0;
  animation: tooltip-appear 0.2s ease forwards;
}

@keyframes tooltip-appear {
  from {
    opacity: 0;
    transform: translateY(-5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive tooltip sizing */
@media (max-width: 768px) {
  .tooltip {
    max-width: 280px;
    min-width: 180px;
  }
}

@media (max-width: 480px) {
  .tooltip {
    max-width: 240px;
    min-width: 160px;
  }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .tooltip {
    background-color: var(--bg-primary);
    border-color: var(--border-hover);
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
  }
}
</style>