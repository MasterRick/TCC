import { useAuthStore } from "@/stores/authStore"
import api from "."
import type { Descriptors, Questions as Question } from "@/types"

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

export const getQuestions = async (page: number, discipline: "MAT" | "POR" | undefined = undefined, classroom: "EF" | "EM" | undefined = undefined, year: "5ANO" | "9ANO" | "3ANO" | undefined = undefined, descriptor_id: number | undefined = undefined) => {
    return api.get(`/questions?page=${page}` + `${discipline ? `&discipline=${discipline}` : ''}` + `${classroom ? `&classroom=${classroom}` : ''}` + `${year ? `&year=${year}` : ''}` + (descriptor_id ? `&descriptor_id=${descriptor_id}` : ''), {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${useAuthStore().token}`
        }
    }).then((response: {
        data: Question[]
    }) => {
        return response.data
    }).catch((error) => {
        console.error('Failed to fetch questions:', error)
        throw error
    })
}

export const getAllDescriptors = async (page: number) => {
    return api.get(`/descriptors?page=${page}`, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${useAuthStore().token}`
        }
    }).then((response: {
        data: Descriptors[]
    }) => {
        return response.data
    }).catch((error) => {
        console.error('Failed to fetch descriptors:', error)
        throw error
    }
    )
}
