<script setup lang="ts">
import { ref, watch } from 'vue'
import { getAllDescriptors } from '@/api/routers'
import type { Descriptors } from '@/types'

interface FilterValues {
  descriptor: Descriptors | null
  difficulty: string | null
  discipline: string | null
  classroom: string | null
  year: string | null
}

const props = defineProps<{
  modelValue: FilterValues
}>()

const emit = defineEmits<{
  'update:modelValue': [value: FilterValues]
  'filter-change': []
}>()

const descriptors = ref<Descriptors[]>([])
const disciplines = ref<string[]>(['Matemática', 'Português'])
const classrooms = ref<string[]>(['Ensino Fundamental', 'Ensino Médio'])
const years = ref<string[]>(['5º Ano', '9º Ano', '3º Ano'])
const difficulties = ref<string[]>(['Fácil', 'Médio', 'Difícil'])

const localFilters = ref<FilterValues>({
  descriptor: props.modelValue.descriptor,
  difficulty: props.modelValue.difficulty,
  discipline: props.modelValue.discipline,
  classroom: props.modelValue.classroom,
  year: props.modelValue.year,
})

const fetchDescriptors = async () => {
  try {
    descriptors.value = await getAllDescriptors(1)
  } catch (error) {
    console.error('Error fetching descriptors:', error)
  }
}

const onSelectDiscipline = (discipline: string | null) => {
  localFilters.value.discipline = discipline
  localFilters.value.descriptor = null
  emit('update:modelValue', { ...localFilters.value })
  emit('filter-change')
}

const onSelectClassroom = (classroom: string | null) => {
  localFilters.value.classroom = classroom
  localFilters.value.year = null
  localFilters.value.descriptor = null
  years.value = classroom === 'Ensino Fundamental' ? ['5º Ano', '9º Ano'] : ['3º Ano']
  emit('update:modelValue', { ...localFilters.value })
  emit('filter-change')
}

const onSelectYear = (year: string | null) => {
  localFilters.value.year = year
  localFilters.value.descriptor = null
  emit('update:modelValue', { ...localFilters.value })
  emit('filter-change')
}

const onSelectDescriptor = (descriptor: Descriptors | null) => {
  localFilters.value.descriptor = descriptor
  emit('update:modelValue', { ...localFilters.value })
  emit('filter-change')
}

const onSelectDifficulty = (difficulty: string | null) => {
  localFilters.value.difficulty = difficulty
  emit('update:modelValue', { ...localFilters.value })
  emit('filter-change')
}

function extractItemDescriptors(item: Descriptors) {
  return {
    title: item.name,
    subtitle: item.content,
  }
}

// Watch for external changes to props
watch(
  () => props.modelValue,
  (newValue) => {
    localFilters.value = { ...newValue }
  },
  { deep: true },
)

fetchDescriptors()
</script>

<template>
  <v-row>
    <v-col>
      <v-select
        clearable
        label="Descritor"
        :disabled="
          localFilters.discipline === null ||
          localFilters.classroom === null ||
          localFilters.year === null
        "
        :item-props="extractItemDescriptors"
        :model-value="localFilters.descriptor"
        :items="
          descriptors.filter((item) => {
            const classroom = localFilters.classroom === 'Ensino Fundamental' ? 'EF' : 'EM'
            const discipline = localFilters.discipline === 'Matemática' ? 'MAT' : 'POR'
            const year =
              localFilters.year === '5º Ano'
                ? '5ANO'
                : localFilters.year === '9º Ano'
                  ? '9ANO'
                  : '3ANO'

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
      <v-select
        clearable
        :model-value="localFilters.difficulty"
        label="Dificuldade"
        :items="difficulties"
        @update:model-value="onSelectDifficulty"
      ></v-select>
    </v-col>
    <v-col>
      <v-select
        clearable
        :model-value="localFilters.discipline"
        label="Disciplina"
        :items="disciplines"
        @update:model-value="onSelectDiscipline"
      ></v-select>
    </v-col>
    <v-col>
      <v-select
        clearable
        :model-value="localFilters.classroom"
        label="Turma"
        :items="classrooms"
        @update:model-value="onSelectClassroom"
      ></v-select>
    </v-col>
    <v-col>
      <v-select
        clearable
        :model-value="localFilters.year"
        label="Ano"
        :items="years"
        @update:model-value="onSelectYear"
      ></v-select>
    </v-col>
  </v-row>
</template>
