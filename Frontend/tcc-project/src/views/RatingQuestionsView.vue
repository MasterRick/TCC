<script setup lang="ts">
import Toolbar from '../components/Toolbar.vue'
import { ref } from 'vue'
import { getAllDescriptors, getQuestions } from '@/api/routers'
import type { Descriptors, Questions } from '@/types'

const questions = ref<Questions[]>([])
const descriptors = ref<Descriptors[]>([])
const disciplines = ref<string[]>(['Matemática', 'Português'])
const classrooms = ref<string[]>(['Ensino Fundamental', 'Ensino Médio'])
const years = ref<string[]>(['5º Ano', '9º Ano', '3º Ano'])
const difficulties = ref<string[]>(['Fácil', 'Médio', 'Difícil'])

const selectedDescriptor = ref<Descriptors | null>(null)
const selectedDificulty = ref<string | null>(null)
const selectedDiscipline = ref<string | null>('Matemática')
const selectedClassroom = ref<string | null>('Ensino Fundamental')
const selectedYear = ref<string | null>('5º Ano')
const currentQuestionIndex = ref(0)
const page = ref(1)
const rating = ref(0)

const fetchQuestions = async () => {
  try {
    const discipline =
      selectedDiscipline.value === 'Matemática'
        ? 'MAT'
        : selectedDiscipline.value === 'Português'
          ? 'POR'
          : undefined

    const classroom =
      selectedClassroom.value === 'Ensino Fundamental'
        ? 'EF'
        : selectedClassroom.value === 'Ensino Médio'
          ? 'EM'
          : undefined

    const year =
      selectedYear.value === '5º Ano'
        ? '5ANO'
        : selectedYear.value === '9º Ano'
          ? '9ANO'
          : selectedYear.value === '3º Ano'
            ? '3ANO'
            : undefined

    const descriptor_id = selectedDescriptor.value ? selectedDescriptor.value.id : undefined

    questions.value = await getQuestions(page.value, discipline, classroom, year, descriptor_id)
  } catch (error) {
    console.error('Error fetching questions:', error)
  }
}

const fetchDescriptors = async () => {
  try {
    descriptors.value = await getAllDescriptors(1)
  } catch (error) {
    console.error('Error fetching descriptors:', error)
  }
}

const nextQuestion = () => {
  rating.value = 0
  if (currentQuestionIndex.value < questions.value.length - 1) {
    console.log('Current Question Index:', currentQuestionIndex.value)
    console.log('Total Questions:', questions.value.length)
    currentQuestionIndex.value++
  } else {
    page.value++
    currentQuestionIndex.value = 0
    fetchQuestions()
  }
}

const onSelectDiscipline = (discipline: string | null) => {
  selectedDescriptor.value = null
  fetchQuestions()
}

const onSelectClassroom = (classroom: string | null) => {
  selectedYear.value = null
  selectedDescriptor.value = null
  years.value = selectedClassroom.value === 'Ensino Fundamental' ? ['5º Ano', '9º Ano'] : ['3º Ano']
  fetchQuestions()
}

const onSelectYear = (year: string | null) => {
  selectedDescriptor.value = null
  fetchQuestions()
}

const onSelectDescriptor = (descriptor: Descriptors | null) => {
  selectedDescriptor.value = descriptor
  fetchQuestions()
}

function extractItemDescriptors(item: Descriptors) {
  return {
    title: item.name,
    subtitle: item.content,
  }
}

fetchQuestions()
fetchDescriptors()
</script>

<template>
  <Toolbar>
    <v-row>
      <v-col>
        <h1 class="text-center">Avaliação de Questões</h1>
        <p class="text-center">Use o formulário abaixo para avaliar as questões.</p>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-select
          clearable
          label="Descritor"
          :disabled="
            selectedDiscipline === null || selectedClassroom === null || selectedYear === null
          "
          :item-props="extractItemDescriptors"
          v-model="selectedDescriptor"
          :items="
            descriptors.filter((item) => {
              const classroom = selectedClassroom === 'Ensino Fundamental' ? 'EF' : 'EM'
              const discipline = selectedDiscipline === 'Matemática' ? 'MAT' : 'POR'
              const year =
                selectedYear === '5º Ano' ? '5ANO' : selectedYear === '9º Ano' ? '9ANO' : '3ANO'

              return (
                item.discipline === discipline && item.classroom === classroom && item.year === year
              )
            })
          "
          @update:model-value="onSelectDescriptor"
        >
        </v-select>
      </v-col>
      <v-col>
        <v-select v-model="selectedDificulty" label="Dificuldade" :items="difficulties"></v-select>
      </v-col>
      <v-col>
        <v-select
          clearable
          v-model="selectedDiscipline"
          label="Disciplina"
          :items="disciplines"
          @update:model-value="onSelectDiscipline"
        ></v-select>
      </v-col>
      <v-col>
        <v-select
          clearable
          v-model="selectedClassroom"
          label="Turma"
          :items="classrooms"
          @update:model-value="onSelectClassroom"
        ></v-select>
      </v-col>
      <v-col>
        <v-select
          clearable
          v-model="selectedYear"
          label="Ano"
          :items="years"
          @update:model-value="onSelectYear"
        ></v-select>
      </v-col>
    </v-row>
    <div style="overflow-x: hidden; overflow-y: auto; max-height: 60vh" v-if="questions.length > 0">
      <v-row>
        <v-col>
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
        <v-col>
          <v-textarea
            label="Comentário"
            rows="4"
            placeholder="Escreva seu comentário aqui..."
          ></v-textarea>
        </v-col>
        <v-col md="3">
          <h2>Avaliação da Questão</h2>
          <p>Por favor, avalie a questão de 1 a 5 estrelas.</p>
          <p>1 estrela = Ruim, 5 estrelas = Muito Boa</p>
          <v-rating v-model="rating" :length="5" color="amber" size="30" label hover></v-rating>
        </v-col>
        <v-col>
          <v-btn color="primary" @click="nextQuestion">Próxima Questão</v-btn>
        </v-col>
      </v-row>
    </div>
    <v-row v-else>
      <v-col>
        <p class="text-center">
          Acabaram as questões que você não avaliou. Por favor, ajuste os filtros.
        </p>
      </v-col>
    </v-row>
  </Toolbar>
</template>
