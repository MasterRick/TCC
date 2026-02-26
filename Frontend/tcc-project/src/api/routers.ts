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
            console.error('Falha no login:', error)
        })
}

export const getQuestions = async (page: number, discipline: "MAT" | "POR" | undefined = undefined, classroom: "EF" | "EM" | undefined = undefined, year: "5ANO" | "9ANO" | "3ANO" | undefined = undefined, difficulty: 0 | 1 | 2 | undefined = undefined, descriptor_id: number | undefined = undefined) => {
    return api.get(`/questions?page=${page}` + `${discipline ? `&discipline=${discipline}` : ''}` + `${classroom ? `&classroom=${classroom}` : ''}` + `${year ? `&year=${year}` : ''}` + (difficulty !== undefined ? `&difficulty=${difficulty}` : '') + (descriptor_id ? `&descriptor_id=${descriptor_id}` : ''), {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${useAuthStore().token}`
        }
    }).then((response: {
        data: Question[]
    }) => {
        return response.data
    }).catch((error) => {
        console.error('Falha ao buscar questões:', error)
        throw error
    })
}

export const getQuestion = async (question_id: number) => {
    return api.get(`/questions/${question_id}`, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${useAuthStore().token}`
        }
    }).then((response) => {
        return response.data
    }).catch((error) => {
        console.error('Falha ao buscar questão:', error)
        throw error
    }
    )
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
        console.error('Falha ao buscar descritores:', error)
        throw error
    }
    )
}

export const setRating = async (question: number, score: {
    coherence: number,
    contextualization: number,
    difficulty_level: number,
    clarity: number,
    descriptor_alignment: number
}, comment: string) => {
    return api.post(`/ratings`, { question, ...score, comment }, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${useAuthStore().token}`
        }
    }).then((response) => {
        return response.data
    }).catch((error) => {
        console.error('Falha ao salvar avaliação:', error)
        throw error
    }
    )
}

export const createQuestions = async (difficulty: number, discipline: string, classroom: string, year: string, content: string) => {
    return api.post(`/questions/create`, {
        difficulty,
        discipline,
        classroom,
        year,
        content
    }, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${useAuthStore().token}`
        }
    }).then((response) => {
        return response.data
    }).catch((error) => {
        console.error('Falha ao criar questões:', error)
        throw error
    }
    )
}

export const createQuestion = async (question: {
    content: string,
    difficulty: 0 | 1 | 2,
    descriptor_id: number | undefined
}) => {
    if (!question.descriptor_id) {
        throw new Error('O ID do descritor é obrigatório para criar uma questão.')
    }

    return api.post(`/questions/create-single`, question, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${useAuthStore().token}`
        }
    }).then((response) => {
        return response.data
    }).catch((error) => {
        console.error('Falha ao criar questão:', error)
        throw error
    }
    )
}

export const createQuestionsGetStatus = async () => {
    return api.get(`/questions/create-status`, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${useAuthStore().token}`
        }
    }).then((response) => {
        return response.data
    }).catch((error) => {
        console.error('Falha ao obter status de criação de questões:', error)
        throw error
    }
    )
}


export const getQuestionsForExam = async (
    difficulty: 0 | 1 | 2,
    discipline: 'MAT' | 'POR',
    classroom: 'EF' | 'EM',
    year: '5ANO' | '9ANO' | '3ANO'
) => {
    return api.get(`/exam/questions/${difficulty}/${discipline}/${classroom}/${year}`, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${useAuthStore().token}`
        }
    }).then((response: {
        data: Question[]
    }) => {
        console.log('Questões para avaliação buscadas:', response.data)
        return response.data
    }).catch((error) => {
        console.error('Falha ao buscar questões para avaliação:', error)
        throw error
    })
}
