<template>
  <div v-if="isEditing" class="edit-form">
    <div class="edit-inputs">
      <input 
        v-model="localEditForm.suggested_value" 
        type="text" 
        class="edit-input"
        placeholder="Enter corrected value"
      />
      <input 
        v-model="localEditForm.reason" 
        type="text" 
        class="edit-input"
        placeholder="Reason for correction"
      />
      <input 
        v-model="localEditForm.source_documentation" 
        type="text" 
        class="edit-input"
        placeholder="Source (optional)"
      />
    </div>
    <div class="edit-actions">
      <button @click="handleSave" class="btn-save">
        Save
      </button>
      <button @click="handleCancel" class="btn-cancel">
        Cancel
      </button>
    </div>
  </div>
  <div v-else class="spec-value editable-field" @mouseenter="showIcon = true" @mouseleave="showIcon = false">
    <slot></slot>
    <button 
      v-if="showIcon" 
      @click="handleEdit"
      class="edit-icon"
      :title="`Suggest correction for ${displayName}`"
    >
      <MdiIcon :path="mdiPencil" :size="16" />
    </button>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { mdiPencil } from '@mdi/js'
import MdiIcon from './MdiIcon.vue'

const props = defineProps({
  fieldName: {
    type: String,
    required: true
  },
  currentValue: {
    type: String,
    required: true
  },
  displayName: {
    type: String,
    required: true
  },
  isEditing: {
    type: Boolean,
    default: false
  },
  editForm: {
    type: Object,
    default: () => ({
      suggested_value: '',
      reason: '',
      source_documentation: ''
    })
  }
})

const emit = defineEmits(['startEdit', 'saveEdit', 'cancelEdit'])

const showIcon = ref(false)
const localEditForm = reactive({ ...props.editForm })

watch(() => props.editForm, (newForm) => {
  Object.assign(localEditForm, newForm)
}, { deep: true })

const handleEdit = () => {
  emit('startEdit', props.fieldName, props.currentValue)
}

const handleSave = () => {
  if (!localEditForm.reason.trim()) {
    alert('Please provide a reason for the correction.')
    return
  }
  
  if (!localEditForm.suggested_value.trim()) {
    alert('Please provide a suggested value.')
    return
  }
  
  emit('saveEdit', props.fieldName, props.currentValue, localEditForm)
}

const handleCancel = () => {
  emit('cancelEdit')
}
</script>

<style scoped>
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

/* Editable field styles */
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
</style>