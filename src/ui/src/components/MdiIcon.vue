<template>
  <svg 
    :width="size" 
    :height="size" 
    viewBox="0 0 24 24"
    :class="['mdi-icon', className]"
  >
    <path :d="path" fill="currentColor" />
  </svg>
</template>

<script setup>
defineProps({
  path: {
    type: String,
    required: true
  },
  size: {
    type: [String, Number],
    default: 16
  },
  className: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.mdi-icon {
  display: inline-block;
  vertical-align: middle;
}
</style>