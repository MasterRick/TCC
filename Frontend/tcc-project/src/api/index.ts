import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'
import { useMessageStore } from '@/stores/messageStore'

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL
})

api.interceptors.response.use(
    (response) => response,
    (error) => {
        const messageStore = useMessageStore()

        if (error.response && error.response.status === 401) {
            // Desloga o usuário quando receber 401
            const authStore = useAuthStore()
            authStore.logout()
            messageStore.showError('Sessão expirada. Por favor, faça login novamente.')

            // Redireciona para a página de login se necessário
            if (window.location.pathname !== '/login') {
                window.location.href = '/login'
            }
        } else if (error.response) {
            // Exibe mensagem de erro genérica para outros erros HTTP
            const message = error.response.data?.message || error.response.data?.detail || 'Ocorreu um erro ao processar sua solicitação'
            messageStore.showError(message)
        } else if (error.request) {
            // Erro de rede
            messageStore.showError('Erro de conexão. Verifique sua internet e tente novamente.')
        }

        return Promise.reject(error)
    }
)

export default api