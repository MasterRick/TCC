import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import NotFound from '../views/NotFoundView.vue'
import LoginView from '../views/LoginView.vue'
import CreateExamView from '../views/CreateExamView.vue'
import RatingQuestionsView from '../views/RatingQuestionsView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Início',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginView,
    },
    {
      path: '/create',
      name: 'Criar Avaliação',
      component: CreateExamView,
    },
    {
      path: '/rating',
      name: 'Avaliar perguntas',
      component: RatingQuestionsView,
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'Pagina não encontrada',
      component: NotFound,
    },
  ],
})

export default router
