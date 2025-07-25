<script setup lang="ts">
import { RouterView } from 'vue-router'
import '@mdi/font/css/materialdesignicons.css'
</script>

<template>
  <v-container class="full-screen">
    <RouterView />
  </v-container>
</template>

<style>
html,
body,
#app {
  margin: 0;
  padding: 0;
}
.full-screen {
  min-width: 100vw;
  padding: 0;
}
</style>
