<script setup lang="ts">
import Toolbar from '../components/Toolbar.vue'
import { menuItems } from '../utils/RouterOptions'
</script>

<template>
  <Toolbar>
    <v-row>
      <v-col>
        <h1 class="text-center">Bem-vindo ao Meu App</h1>
        <p class="text-center">Use o menu lateral para navegar entre as páginas.</p>
      </v-col>
    </v-row>
    <v-row>
      <template v-for="item in menuItems" :key="item.title">
        <v-col sm="6" md="6" v-if="item.route !== '/'">
          <v-card
            :key="item.title"
            link
            variant="tonal"
            :to="item.route"
            height="25vh"
            class="d-flex flex-column align-center justify-center"
          >
            <v-card-title class="text-h5">
              <v-icon>{{ item.icon }}</v-icon>
              {{ item.title }}
            </v-card-title>
            <v-card-subtitle class="text-center">
              Clique para navegar para {{ item.title }}.
            </v-card-subtitle>
          </v-card>
        </v-col>
      </template>
    </v-row>
  </Toolbar>
</template>
