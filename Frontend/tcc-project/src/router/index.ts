import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import NotFound from '../views/NotFoundView.vue'
import LoginView from '../views/LoginView.vue'
import CreateExamView from '../views/CreateExamView.vue'
import RatingQuestionsView from '../views/RatingQuestionsView.vue'
import CreateQuestionView from '../views/CreateQuestionView.vue'
import { useAuthStore } from '@/stores/authStore'


const routers = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Início',
      component: HomeView,
      meta: { requiresAuth: true },
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginView,
      meta: { requiresAuth: false },
    },
    {
      path: '/create',
      name: 'Criar Avaliação',
      component: CreateExamView,
      meta: { requiresAuth: true },
    },
    {
      path: '/createQuestion',
      name: 'Criar Questão',
      component: CreateQuestionView,
      meta: { requiresAuth: true },
    },
    {
      path: '/rating',
      name: 'Avaliar perguntas',
      component: RatingQuestionsView,
      meta: { requiresAuth: true },
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'Pagina não encontrada',
      component: NotFound,
    },
  ],
})

routers.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next({ name: 'Login' })
  } else if (to.name === 'Login' && auth.isAuthenticated) {
    next({ name: 'Início' })
  } else {
    next()
  }
})


export default routers
