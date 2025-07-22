import { useAuthStore } from "@/stores/authStore"
import api from "."

export const loginApi = async (email: string, password: string) => {

    const data = new URLSearchParams()
    data.append('username', email)
    data.append('password', password)

    return api
        .post('/auth', data, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        })
        .then((response) => {
            useAuthStore().login(response.data.access_token)
        })
        .catch((error) => {
            console.error('Login failed:', error)
        })
}
