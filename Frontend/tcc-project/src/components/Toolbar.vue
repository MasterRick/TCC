<template>
  <v-app>
    <v-navigation-drawer v-model="drawer" app>
      <v-list>
        <v-list-item>
          <v-list-item-title class="text-h6">Meu App</v-list-item-title>
        </v-list-item>
        <v-divider></v-divider>

        <v-list-item
          v-for="item in menuItems"
          :key="item.title"
          link
          :to="item.route"
          @click="drawer = false"
        >
          <v-icon>{{ item.icon }}</v-icon>
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <v-toolbar-title>{{ $route.name }}</v-toolbar-title>
    </v-app-bar>

    <v-main>
      <v-container max-width="85vw">
        <slot></slot>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
import { menuItems } from '../utils/RouterOptions'

const drawer = ref(true)
</script>

<style scoped>
.v-navigation-drawer {
  width: 220px;
}
</style>
