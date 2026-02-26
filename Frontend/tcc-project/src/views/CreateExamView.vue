<script setup lang="ts">
import { ref, watch } from 'vue'
import Toolbar from '../components/Toolbar.vue'
import draggable from 'vuedraggable'
import type { Descriptors, Questions } from '@/types'
import QuestionFilters from '@/components/QuestionFilters.vue'
import CardExam from '@/components/CardExam.vue'
import { getQuestion, getQuestionsForExam } from '@/api/routers'
import { useLoadingStore } from '@/stores/loadingStore'
import jsPDF from 'jspdf'

const loadingStore = useLoadingStore()

const questionsInExam = ref<Questions[]>([])
const allQuestions = ref<Questions[]>([])
const questionIdToSearch = ref<number | null>(null)
const showQuestionDialog = ref(false)
const selectedQuestion = ref<Questions | null>(null)
const studentName = ref('')
const schoolName = ref('')
const teacherName = ref('')

const filters = ref({
  descriptor: null as Descriptors | null,
  difficulty: 'Fácil' as string | null,
  discipline: 'Matemática' as string | null,
  classroom: 'Ensino Fundamental' as string | null,
  year: '5º Ano' as string | null,
})

const mapDifficulty = (difficulty: string | null): 0 | 1 | 2 | null => {
  if (difficulty === 'Fácil') return 0
  if (difficulty === 'Médio') return 1
  if (difficulty === 'Difícil') return 2
  return null
}

const mapDiscipline = (discipline: string | null): 'MAT' | 'POR' | null => {
  if (discipline === 'Matemática') return 'MAT'
  if (discipline === 'Português') return 'POR'
  return null
}

const mapClassroom = (classroom: string | null): 'EF' | 'EM' | null => {
  if (classroom === 'Ensino Fundamental') return 'EF'
  if (classroom === 'Ensino Médio') return 'EM'
  return null
}

const mapYear = (year: string | null): '5ANO' | '9ANO' | '3ANO' | null => {
  if (year === '5º Ano') return '5ANO'
  if (year === '9º Ano') return '9ANO'
  if (year === '3º Ano') return '3ANO'
  return null
}

const getFilterCodes = () => {
  const difficulty = mapDifficulty(filters.value.difficulty)
  const discipline = mapDiscipline(filters.value.discipline)
  const classroom = mapClassroom(filters.value.classroom)
  const year = mapYear(filters.value.year)

  if (difficulty === null || discipline === null || classroom === null || year === null) {
    return null
  }

  return { difficulty, discipline, classroom, year }
}

const resetQuestionLists = () => {
  allQuestions.value = []
  questionsInExam.value = []
}

const fetchQuestionsForExam = async () => {
  const filterCodes = getFilterCodes()

  if (!filterCodes) {
    resetQuestionLists()
    return
  }

  loadingStore.showLoading('Carregando questões...')
  try {
    const response = await getQuestionsForExam(
      filterCodes.difficulty,
      filterCodes.discipline,
      filterCodes.classroom,
      filterCodes.year,
    )
    questionsInExam.value = response
    allQuestions.value = []
  } catch (error) {
    console.error('Erro ao buscar questões para avaliação:', error)
    resetQuestionLists()
  } finally {
    loadingStore.hideLoading()
  }
}

const addQuestionById = async () => {
  if (questionIdToSearch.value === null || questionIdToSearch.value <= 0) {
    return
  }

  loadingStore.showLoading('Buscando questão por ID...')
  try {
    const response = await getQuestion(questionIdToSearch.value)
    const fetchedQuestion = (response?.question ?? response) as Questions

    if (!fetchedQuestion?.id) {
      return
    }

    const alreadyExistsInAllQuestions = allQuestions.value.some(
      (question) => question.id === fetchedQuestion.id,
    )
    const alreadyExistsInExamQuestions = questionsInExam.value.some(
      (question) => question.id === fetchedQuestion.id,
    )

    if (!alreadyExistsInAllQuestions && !alreadyExistsInExamQuestions) {
      allQuestions.value = [fetchedQuestion, ...allQuestions.value]
    }
    questionIdToSearch.value = null
  } catch (error) {
    console.error('Erro ao buscar questão por ID:', error)
  } finally {
    loadingStore.hideLoading()
  }
}

const openQuestionDialog = (question: Questions) => {
  selectedQuestion.value = question
  showQuestionDialog.value = true
}

const closeQuestionDialog = () => {
  showQuestionDialog.value = false
  selectedQuestion.value = null
}

const getAlternatives = (question: Questions | null) => {
  if (!question) return []
  return question.content.alternatives
    .split('\n')
    .map((alternative) => alternative.trim())
    .filter((alternative) => alternative.length > 0)
}

const openPdfInNewTab = (doc: jsPDF, fileName: string) => {
  const pdfUrl = doc.output('bloburl')
  const openedWindow = window.open(pdfUrl, '_blank')

  if (!openedWindow) {
    doc.save(fileName)
  }
}

const removeQuestionFromExam = (question: Questions) => {
  questionsInExam.value = questionsInExam.value.filter((q) => q.id !== question.id)
}

const removeQuestionFromSearched = (question: Questions) => {
  allQuestions.value = allQuestions.value.filter((q) => q.id !== question.id)
}

const createExam = () => {
  const doc = new jsPDF({ format: 'a4', unit: 'mm' })

  const pageWidth = doc.internal.pageSize.getWidth()
  const pageHeight = doc.internal.pageSize.getHeight()
  const marginX = 14
  const bottomMargin = 14
  const contentWidth = pageWidth - marginX * 2
  const lineHeight = 5.5

  const drawHeader = () => {
    doc.setFillColor(30, 64, 175)
    doc.rect(0, 0, pageWidth, 34, 'F')

    doc.setTextColor(255, 255, 255)
    doc.setFont('helvetica', 'bold')
    doc.setFontSize(16)
    doc.text('Avaliação', pageWidth / 2, 11, { align: 'center' })

    doc.setFont('helvetica', 'normal')
    doc.setFontSize(10)
    doc.text(`Aluno: ${studentName.value || '-'}`, marginX, 19)
    doc.text(`Escola: ${schoolName.value || '-'}`, marginX, 25)
    doc.text(`Professor: ${teacherName.value || '-'}`, marginX, 31)

    doc.setTextColor(0, 0, 0)
    doc.setFont('helvetica', 'normal')
    doc.setFontSize(10)
    doc.text(`Data: ${new Date().toLocaleDateString('pt-BR')}`, marginX, 42)
    doc.text(`Quantidade de questões: ${questionsInExam.value.length}`, pageWidth - marginX, 42, {
      align: 'right',
    })

    doc.setDrawColor(210, 210, 210)
    doc.line(marginX, 45, pageWidth - marginX, 45)
    return 52
  }

  let currentY = drawHeader()

  const ensureSpace = (requiredHeight: number) => {
    if (currentY + requiredHeight <= pageHeight - bottomMargin) {
      return
    }

    doc.addPage()
    currentY = drawHeader()
  }

  if (questionsInExam.value.length === 0) {
    doc.setFont('helvetica', 'italic')
    doc.setFontSize(12)
    doc.text('Nenhuma questão na avaliação.', marginX, currentY)
    openPdfInNewTab(doc, 'avaliacao.pdf')
    return
  }

  questionsInExam.value.forEach((question, index) => {
    const questionText = `${index + 1}. ${question.content.question}`
    const questionLines = doc.splitTextToSize(questionText, contentWidth - 40)
    const alternatives = question.content.alternatives
      .split('\n')
      .map((alternative) => alternative.trim())
      .filter((alternative) => alternative.length > 0)

    const alternativesHeight = alternatives.reduce((total, alternative) => {
      const alternativeLabel = `${alternative}`
      const alternativeLines = doc.splitTextToSize(alternativeLabel, contentWidth - 8)
      return total + alternativeLines.length * lineHeight + 1
    }, 0)

    const blockHeight = questionLines.length * lineHeight + alternativesHeight + 10
    ensureSpace(blockHeight)

    doc.setDrawColor(220, 220, 220)
    doc.roundedRect(marginX - 2, currentY - 4, contentWidth + 4, blockHeight, 2, 2, 'S')

    doc.setFont('helvetica', 'bold')
    doc.setFontSize(12)
    currentY += 2
    doc.text(questionLines, marginX + 2, currentY)
    currentY += questionLines.length * lineHeight + 2

    doc.setFont('helvetica', 'normal')
    doc.setFontSize(11)
    alternatives.forEach((alternative) => {
      const alternativeLines = doc.splitTextToSize(alternative, contentWidth - 8)
      ensureSpace(alternativeLines.length * lineHeight + 2)
      doc.text(alternativeLines, marginX + 4, currentY)
      currentY += alternativeLines.length * lineHeight + 1
    })

    currentY += 7
  })

  openPdfInNewTab(doc, 'avaliacao.pdf')
}

watch(filters, fetchQuestionsForExam, { deep: true, immediate: true })
</script>

<template>
  <Toolbar>
    <v-row>
      <v-col>
        <h1 class="text-center">Criar Avaliação</h1>
        <p class="text-center">Use o formulário abaixo para criar uma nova avaliação.</p>
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
      <QuestionFilters v-model="filters" @filter-change="fetchQuestionsForExam" />
    </v-row>
    <v-row class="mb-1">
      <v-col cols="12" md="4">
        <v-text-field
          v-model="studentName"
          label="Nome do aluno"
          variant="outlined"
          density="comfortable"
          hide-details
        />
      </v-col>
      <v-col cols="12" md="4">
        <v-text-field
          v-model="schoolName"
          label="Escola"
          variant="outlined"
          density="comfortable"
          hide-details
        />
      </v-col>
      <v-col cols="12" md="4">
        <v-text-field
          v-model="teacherName"
          label="Professor"
          variant="outlined"
          density="comfortable"
          hide-details
        />
      </v-col>
    </v-row>
    <v-row class="mb-2">
      <v-col cols="12" md="3">
        <v-text-field
          v-model.number="questionIdToSearch"
          label="Buscar questão por ID"
          type="number"
          min="1"
          variant="outlined"
          density="comfortable"
          hide-details
        />
      </v-col>
      <v-col cols="12" md="1" class="d-flex align-center">
        <v-btn color="primary" block @click="addQuestionById">Buscar</v-btn>
      </v-col>
      <v-col cols="12" md="8" class="d-flex justify-end align-center">
        <v-btn color="success" @click="createExam()"> Salvar Avaliação </v-btn>
      </v-col>
    </v-row>
    <v-row class="mb-1">
      <v-col>
        <p class="text-center">
          Arraste as questões entre as colunas para montar a avaliação. Você também pode clicar no
          ícone de olho para ver os detalhes de cada questão.
        </p>
      </v-col>
    </v-row>
    <v-row class="justify-space-between m-6">
      <v-col cols="10" md="4">
        <h2 class="text-h6 mb-3 text-center">Questões pesquisadas</h2>
        <draggable
          class="questions-column"
          group="items"
          v-model="allQuestions"
          item-key="id"
          animation="200"
          ghost-class="ghost"
          height="auto"
        >
          <template #item="{ element }">
            <CardExam
              :question="element"
              @view="openQuestionDialog"
              @remove="removeQuestionFromSearched"
            />
          </template>
        </draggable>
      </v-col>
      <v-col cols="10" md="7">
        <h2 class="text-h6 mb-3 text-center">Questões na avaliação</h2>
        <draggable
          class="questions-column2"
          group="items"
          v-model="questionsInExam"
          item-key="id"
          animation="200"
          ghost-class="ghost"
          height="auto"
        >
          <template #item="{ element }">
            <CardExam
              :question="element"
              @view="openQuestionDialog"
              @remove="removeQuestionFromExam"
            />
          </template>
        </draggable>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <p class="text-center mt-3">
          Depois de finalizar a avaliação, clique no botão "Salvar Avaliação" para gerar um PDF com
          as questões selecionadas.
        </p>
      </v-col>
    </v-row>
    <v-row class="d-flex justify-center">
      <v-btn color="success" @click="createExam()"> Salvar Avaliação </v-btn>
    </v-row>
    <v-dialog v-model="showQuestionDialog" max-width="900px">
      <v-card>
        <v-card-title class="text-h6">Detalhes da questão</v-card-title>
        <v-card-text v-if="selectedQuestion">
          <p><strong>ID:</strong> {{ selectedQuestion.id }}</p>
          <p>
            <strong>Descritor:</strong> {{ selectedQuestion.descriptor.name }} -
            {{ selectedQuestion.descriptor.content }}
          </p>
          <p><strong>Enunciado:</strong> {{ selectedQuestion.content.question }}</p>
          <p class="mt-3"><strong>Alternativas:</strong></p>
          <v-list density="compact">
            <v-list-item
              v-for="(alternative, index) in getAlternatives(selectedQuestion)"
              :key="`${selectedQuestion.id}-alt-${index}`"
            >
              <v-list-item-title>{{ alternative }}</v-list-item-title>
            </v-list-item>
          </v-list>
          <p><strong>Resposta:</strong> {{ selectedQuestion.content.answer }}</p>
          <p><strong>Justificativa:</strong> {{ selectedQuestion.content.justification }}</p>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="primary" variant="text" @click="closeQuestionDialog">Fechar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </Toolbar>
</template>
<style>
.ghost {
  opacity: 0.5;
}

.questions-column {
  background: #eef2ff;
  border-radius: 10px;
  padding: 16px;
  display: flex;
  flex-direction: column;
}

.questions-column2 {
  background: #c9f6cd;
  border-radius: 10px;
  padding: 16px;
  display: flex;
  flex-direction: column;
}
</style>
