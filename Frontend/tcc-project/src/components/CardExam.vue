<script setup lang="ts">
import type { Questions } from '@/types'

const props = defineProps<{
  question: Questions
}>()

const emit = defineEmits<{
  view: [question: Questions]
  remove: [question: Questions]
}>()

const getQuestionRating = (question: Questions) => {
  return question.rating ?? null
}

const onViewQuestion = () => {
  emit('view', props.question)
}

const onRemoveQuestion = () => {
  emit('remove', props.question)
}
</script>

<template>
  <v-card
    :title="question.descriptor.name"
    :subtitle="question.descriptor.content"
    :text="question.content.question"
    class="mb-2 pa-3 card"
  >
    <v-card-actions>
      <v-row class="align-center" no-gutters>
        <div v-if="getQuestionRating(question) !== null" class="d-flex align-center">
          <v-rating
            :model-value="getQuestionRating(question) ?? 0"
            :length="5"
            color="amber"
            disabled
            halfIncrements
            size="30"
          >
          </v-rating>
          <div class="ml-2">{{ question.rating }}</div>
        </div>
        <div v-else><h3>Sem avaliação</h3></div>
        <v-spacer></v-spacer>
        <v-btn icon @click.stop="onViewQuestion">
          <v-icon>mdi-eye</v-icon>
        </v-btn>
        <v-btn icon @click.stop="onRemoveQuestion">
          <v-icon>mdi-delete</v-icon>
        </v-btn>
      </v-row>
    </v-card-actions>
  </v-card>
</template>

<style scoped>
.card {
  cursor: grab;
}
</style>
