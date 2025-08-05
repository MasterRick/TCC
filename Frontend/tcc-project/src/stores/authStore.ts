import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: sessionStorage.getItem('token') || null
  }),
  getters: {
    isAuthenticated: (state) => !!state.token
  },
  actions: {
    login(token: string) {
      this.token = token
      sessionStorage.setItem('token', token)
    },
    logout() {
      this.token = null
      sessionStorage.removeItem('token')
    }
  }
})
