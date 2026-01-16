import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useLoadingStore = defineStore('loading', () => {
    const isLoading = ref(false)
    const loadingMessage = ref('')

    const showLoading = (message: string = 'Carregando...') => {
        isLoading.value = true
        loadingMessage.value = message
    }

    const hideLoading = () => {
        isLoading.value = false
        loadingMessage.value = ''
    }

    return {
        isLoading,
        loadingMessage,
        showLoading,
        hideLoading,
    }
})
