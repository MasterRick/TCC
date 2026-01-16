<script setup lang="ts">
import { useMessageStore } from '@/stores/messageStore'
import { computed } from 'vue'

const messageStore = useMessageStore()

const getColor = (type: string) => {
  switch (type) {
    case 'success':
      return 'success'
    case 'error':
      return 'error'
    case 'warning':
      return 'warning'
    case 'info':
      return 'info'
    default:
      return 'info'
  }
}

const getIcon = (type: string) => {
  switch (type) {
    case 'success':
      return 'mdi-check-circle'
    case 'error':
      return 'mdi-alert-circle'
    case 'warning':
      return 'mdi-alert'
    case 'info':
      return 'mdi-information'
    default:
      return 'mdi-information'
  }
}

const currentMessage = computed(() => messageStore.messages[0] || null)

const closeMessage = () => {
  if (currentMessage.value) {
    messageStore.removeMessage(currentMessage.value.id)
  }
}
</script>

<template>
  <v-snackbar
    v-if="currentMessage"
    :model-value="true"
    :color="getColor(currentMessage.type)"
    :timeout="currentMessage.timeout"
    location="top right"
    @update:model-value="closeMessage"
  >
    <div class="d-flex align-center">
      <v-icon :icon="getIcon(currentMessage.type)" class="mr-2"></v-icon>
      <span>{{ currentMessage.text }}</span>
    </div>
    <template v-slot:actions>
      <v-btn variant="text" @click="closeMessage" icon="mdi-close" size="small"></v-btn>
    </template>
  </v-snackbar>
</template>
