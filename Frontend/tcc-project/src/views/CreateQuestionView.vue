<script setup lang="ts">
import { createQuestions, createQuestionsGetStatus, createQuestion } from '@/api/routers'
import Toolbar from '../components/Toolbar.vue'
import { ref, type Ref } from 'vue'
import QuestionFilters from '@/components/QuestionFilters.vue'
import type { Descriptors } from '@/types'

const status = ref<{
  running: boolean
  current_file: string
  current_difficulty: number
  current_descriptor: string | null
  current_content: string | null
}>({
  running: true,
  current_file: '',
  current_difficulty: 0,
  current_descriptor: null,
  current_content: null,
})

const filters = ref({
  descriptor: null as Descriptors | null,
  difficulty: 'Fácil' as string | null,
  discipline: 'Matemática' as string | null,
  classroom: 'Ensino Fundamental' as string | null,
  year: '5º Ano' as string | null,
})

const content = ref('')

const fetchCreateQuestions = async () => {
  await createQuestions()
}

const fetchGetStatus = async () => {
  console.log('Fetching status...')
  status.value = await createQuestionsGetStatus()
}

const fetchCreateQuestion = async () => {
  await createQuestion({
    content: content.value,
    difficulty:
      filters.value.difficulty == 'Fácil' ? 0 : filters.value.difficulty == 'Médio' ? 1 : 2,
    descriptor_id: filters.value.descriptor?.id,
  })
  fetchGetStatus()
}

fetchGetStatus()
</script>

<template>
  <Toolbar>
    <v-container>
      <v-row>
        <v-col>
          <h1 class="text-center">Criar Questões</h1>
          <p class="text-center">Use o formulário abaixo para criar novas questões.</p>
        </v-col>
      </v-row>
      <v-row>
        <v-col class="d-flex justify-center mb-4">
          <v-btn color="secondary" @click="fetchGetStatus">
            Atualizar status:
            {{
              status.running == true
                ? 'A criação de questões não está disponível no momento, tente novamente mais tarde.'
                : 'Criação de questões disponível'
            }}
          </v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <p class="text-center">
            Use os filtros abaixo para especificar o tipo de questão que deseja criar.
          </p>
        </v-col>
      </v-row>
      <v-row>
        <QuestionFilters v-model="filters" />
      </v-row>
      <v-row class="mt-4">
        <v-textarea
          label="Coloque aqui a tematica que você quer na questão"
          v-model="content"
          rows="4"
          outlined
        ></v-textarea>
      </v-row>
      <v-row>
        <v-col class="d-flex justify-center" style="gap: 15px">
          <v-btn :disabled="status.running" color="success" @click="fetchCreateQuestion">
            Criar Questão
          </v-btn>
          <v-btn :disabled="true" color="primary" @click="fetchCreateQuestions">
            Criar Questões Aleatórias
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </Toolbar>
</template>
<style scoped></style>
