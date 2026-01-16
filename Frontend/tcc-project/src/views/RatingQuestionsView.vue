<script setup lang="ts">
import Toolbar from '../components/Toolbar.vue'
import QuestionFilters from '../components/QuestionFilters.vue'
import { ref } from 'vue'
import { getQuestions, setRating } from '@/api/routers'
import type { Descriptors, Questions } from '@/types'

const questions = ref<Questions[]>([])
const comment = ref<string>('')
const isLoading = ref(false)

const filters = ref({
  descriptor: null as Descriptors | null,
  difficulty: 'Fácil' as string | null,
  discipline: 'Matemática' as string | null,
  classroom: 'Ensino Fundamental' as string | null,
  year: '5º Ano' as string | null,
})

const currentQuestionIndex = ref(0)
const page = ref(1)
const showRatingDialog = ref(false)
const rating = ref({
  coherence: 0,
  contextualization: 0,
  difficulty_level: 0,
  clarity: 0,
  descriptor_alignment: 0,
})

const fetchQuestions = async () => {
  isLoading.value = true
  try {
    const discipline =
      filters.value.discipline === 'Matemática'
        ? 'MAT'
        : filters.value.discipline === 'Português'
          ? 'POR'
          : undefined

    const classroom =
      filters.value.classroom === 'Ensino Fundamental'
        ? 'EF'
        : filters.value.classroom === 'Ensino Médio'
          ? 'EM'
          : undefined

    const year =
      filters.value.year === '5º Ano'
        ? '5ANO'
        : filters.value.year === '9º Ano'
          ? '9ANO'
          : filters.value.year === '3º Ano'
            ? '3ANO'
            : undefined

    const difficulty =
      filters.value.difficulty === 'Fácil'
        ? 0
        : filters.value.difficulty === 'Médio'
          ? 1
          : filters.value.difficulty === 'Difícil'
            ? 2
            : undefined

    const descriptor_id = filters.value.descriptor ? filters.value.descriptor.id : undefined

    questions.value = await getQuestions(
      page.value,
      discipline,
      classroom,
      year,
      difficulty,
      descriptor_id,
    )
  } catch (error) {
    console.error('Error fetching questions:', error)
  } finally {
    isLoading.value = false
  }
}

const onFilterChange = () => {
  page.value = 1
  currentQuestionIndex.value = 0
  fetchQuestions()
}

const setQuestionRating = async (questionId: number, comment: string) => {
  try {
    await setRating(questionId, rating.value, comment)
    console.log(`Rating for question ${questionId} set to`, rating.value)
  } catch (error) {
    console.error('Error setting question rating:', error)
  }
}

const openRatingDialog = () => {
  showRatingDialog.value = true
}

const saveRating = async () => {
  await setQuestionRating(questions.value[currentQuestionIndex.value].id, comment.value)
  showRatingDialog.value = false
  nextQuestion()
}

const nextQuestion = () => {
  if (currentQuestionIndex.value < questions.value.length - 1) {
    currentQuestionIndex.value++
  } else {
    page.value++
    currentQuestionIndex.value = 0
    fetchQuestions()
  }

  rating.value.coherence = 0
  rating.value.contextualization = 0
  rating.value.difficulty_level = 0
  rating.value.clarity = 0
  rating.value.descriptor_alignment = 0
  comment.value = ''
}

fetchQuestions()
</script>

<template>
  <Toolbar>
    <v-row>
      <v-col>
        <h1 class="text-center">Avaliação de Questões</h1>
        <p class="text-center">Use o formulário abaixo para avaliar as questões.</p>
      </v-col>
    </v-row>

    <QuestionFilters v-model="filters" @filter-change="onFilterChange" />
    <div v-if="isLoading">
      <v-row>
        <v-col class="text-center">
          <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
          <div class="mt-4 text-h6 text-style">Carregando questões...</div>
        </v-col>
      </v-row>
    </div>
    <div v-else>
      <div style="" v-if="questions.length > 0">
        <v-row>
          <v-col>
            <h2>Identificador da Questão: {{ questions[currentQuestionIndex]?.id }}</h2>
            <h2>
              Descritor:{{ questions[currentQuestionIndex]?.descriptor.name }} -
              {{ questions[currentQuestionIndex]?.descriptor.content }}
            </h2>
            <h2>
              Dificuldade:{{
                questions[currentQuestionIndex]?.difficulty === 0
                  ? 'Fácil'
                  : questions[currentQuestionIndex]?.difficulty === 1
                    ? 'Médio'
                    : 'Difícil'
              }}
            </h2>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <h2>Enunciado:</h2>
            <p>{{ questions[currentQuestionIndex]?.content.question }}</p>
            <h2>Alternativas:</h2>
            <h3
              :style="
                questions[currentQuestionIndex]?.content.answer == 'A'
                  ? 'background-color: #d4edda;'
                  : ''
              "
            >
              {{ questions[currentQuestionIndex]?.content.alternatives.split('\n')[0].trim() }}
            </h3>
            <h3
              :style="
                questions[currentQuestionIndex]?.content.answer == 'B'
                  ? 'background-color: #d4edda;'
                  : ''
              "
            >
              {{ questions[currentQuestionIndex]?.content.alternatives.split('\n')[1].trim() }}
            </h3>
            <h3
              :style="
                questions[currentQuestionIndex]?.content.answer == 'C'
                  ? 'background-color: #d4edda;'
                  : ''
              "
            >
              {{ questions[currentQuestionIndex]?.content.alternatives.split('\n')[2].trim() }}
            </h3>
            <h3
              :style="
                questions[currentQuestionIndex]?.content.answer == 'D'
                  ? 'background-color: #d4edda;'
                  : ''
              "
            >
              {{ questions[currentQuestionIndex]?.content.alternatives.split('\n')[3].trim() }}
            </h3>
            <h3
              :style="
                questions[currentQuestionIndex]?.content.answer == 'E'
                  ? 'background-color: #d4edda;'
                  : ''
              "
            >
              {{ questions[currentQuestionIndex]?.content.alternatives.split('\n')[4].trim() }}
            </h3>
            <h2>Justificativa:</h2>
            <p>{{ questions[currentQuestionIndex]?.content.justification }}</p>
          </v-col>
        </v-row>
        <v-row>
          <v-col class="text-center">
            <v-btn color="primary" size="large" @click="openRatingDialog">Avaliar Questão</v-btn>
          </v-col>
        </v-row>
      </div>
      <div v-else>
        <v-row>
          <v-col>
            <p class="text-center">
              Acabaram as questões que você não avaliou. Por favor, ajuste os filtros.
            </p>
          </v-col>
        </v-row>
      </div>
    </div>
    <!-- Dialog de Avaliação -->
    <v-dialog v-model="showRatingDialog" max-width="800px" close-on-escape>
      <v-card>
        <v-card-title class="text-h5 text-center pa-2"> Avaliação da Questão </v-card-title>

        <v-container>
          <v-row>
            <v-col cols="12">
              <h3 class="mb-3">Por favor, avalie cada aspecto da questão de 1 a 5 estrelas:</h3>
              <p class="text-caption mb-4">1 estrela = Ruim, 5 estrelas = Muito Boa</p>
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="4">
              <strong>Coerência dos enunciados:</strong>
            </v-col>
            <v-col cols="8">
              <v-rating
                v-model="rating.coherence"
                :length="5"
                color="amber"
                size="30"
                hover
              ></v-rating>
            </v-col>
          </v-row>

          <v-row class="">
            <v-col cols="4">
              <strong>Contextualização adequada:</strong>
            </v-col>
            <v-col cols="8">
              <v-rating
                v-model="rating.contextualization"
                :length="5"
                color="amber"
                size="30"
                hover
              ></v-rating>
            </v-col>
          </v-row>

          <v-row class="">
            <v-col cols="4">
              <strong>Nível de dificuldade apropriado:</strong>
            </v-col>
            <v-col cols="8">
              <v-rating
                v-model="rating.difficulty_level"
                :length="5"
                color="amber"
                size="30"
                hover
              ></v-rating>
            </v-col>
          </v-row>

          <v-row class="">
            <v-col cols="4">
              <strong>Clareza das alternativas:</strong>
            </v-col>
            <v-col cols="8">
              <v-rating
                v-model="rating.clarity"
                :length="5"
                color="amber"
                size="30"
                hover
              ></v-rating>
            </v-col>
          </v-row>

          <v-row class="">
            <v-col cols="4">
              <strong>Alinhamento com descritor:</strong>
            </v-col>
            <v-col cols="8">
              <v-rating
                v-model="rating.descriptor_alignment"
                :length="5"
                color="amber"
                size="30"
                hover
              ></v-rating>
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12">
              <v-textarea
                v-model="comment"
                label="Comentário (opcional)"
                rows="2"
                placeholder="Escreva seu comentário aqui..."
                variant="outlined"
              ></v-textarea>
            </v-col>
          </v-row>
        </v-container>

        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn color="grey" variant="text" @click="showRatingDialog = false"> Cancelar </v-btn>
          <v-btn color="primary" variant="elevated" @click="saveRating"> Salvar Avaliação </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </Toolbar>
</template>
