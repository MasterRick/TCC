<script setup lang="ts">
import { createQuestions, createQuestionsGetStatus, createQuestion } from '@/api/routers'
import Toolbar from '../components/Toolbar.vue'
import { ref } from 'vue'

const status = ref<{
  running: boolean
  current_file: string
  current_difficulty: number
  current_descriptor: string | null
  current_content: string | null
}>({
  running: false,
  current_file: '',
  current_difficulty: 0,
  current_descriptor: null,
  current_content: null,
})

const fetchCreateQuestions = async () => {
  await createQuestions()
}

const fetchGetStatus = async () => {
  console.log('Fetching status...')
  status.value = await createQuestionsGetStatus()
}

const fetchCreateQuestion = async () => {
  await createQuestion({
    content: 'Star Wars',
    difficulty: 0,
    descriptor_id: 200,
  })
}

fetchGetStatus()
</script>

<template>
  <Toolbar>
    <v-container>
      <v-row>
        <v-col>
          <h1 class="text-center">Criar Multiplas Questões Aleatórias</h1>
          <p class="text-center">Use o formulário abaixo para criar novas questões.</p>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <p class="text-center">
            Status:
            {{
              status.running == true
                ? 'A criação de questões não está disponível no momento, tente novamente mais tarde.'
                : 'Criação de questões disponível'
            }}
          </p>
        </v-col>
      </v-row>
      <v-row>
        <v-col class="d-flex justify-center">
          <v-btn :disabled="status.running" color="success" @click="fetchCreateQuestion">
            Criar Questão Exemplo
          </v-btn>
          <v-btn :disabled="status.running" color="primary" @click="fetchCreateQuestions">
            Criar Questões Aleatórias
          </v-btn>
          <v-btn color="secondary" @click="fetchGetStatus"> Verificar Status </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </Toolbar>
</template>
<style scoped></style>
