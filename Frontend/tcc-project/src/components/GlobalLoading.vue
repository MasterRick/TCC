<script setup lang="ts">
import { useLoadingStore } from '@/stores/loadingStore'

const loadingStore = useLoadingStore()
</script>

<template>
  <v-overlay
    :model-value="loadingStore.isLoading"
    class="align-center justify-center"
    persistent
    contained
  >
    <div class="text-center">
      <v-progress-circular indeterminate color="primary" size="64" width="6"></v-progress-circular>
      <div v-if="loadingStore.loadingMessage" class="mt-4 text-h6 text-style">
        {{ loadingStore.loadingMessage }}
      </div>
    </div>
  </v-overlay>
</template>

<style scoped>
.v-overlay {
  z-index: 9999;
}

.text-style {
  font-weight: 500;
  color: black;
}
</style>
