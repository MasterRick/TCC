import { defineStore } from 'pinia'
import { ref } from 'vue'

export type MessageType = 'success' | 'error' | 'warning' | 'info'

export interface Message {
    id: number
    text: string
    type: MessageType
    timeout?: number
}

export const useMessageStore = defineStore('message', () => {
    const messages = ref<Message[]>([])
    let messageIdCounter = 0

    const showMessage = (text: string, type: MessageType = 'info', timeout: number = 5000) => {
        const id = messageIdCounter++
        messages.value.push({
            id,
            text,
            type,
            timeout,
        })
        return id
    }

    const showSuccess = (text: string, timeout?: number) => {
        return showMessage(text, 'success', timeout)
    }

    const showError = (text: string, timeout?: number) => {
        return showMessage(text, 'error', timeout)
    }

    const showWarning = (text: string, timeout?: number) => {
        return showMessage(text, 'warning', timeout)
    }

    const showInfo = (text: string, timeout?: number) => {
        return showMessage(text, 'info', timeout)
    }

    const removeMessage = (id: number) => {
        const index = messages.value.findIndex((m) => m.id === id)
        if (index !== -1) {
            messages.value.splice(index, 1)
        }
    }

    return {
        messages,
        showMessage,
        showSuccess,
        showError,
        showWarning,
        showInfo,
        removeMessage,
    }
})
