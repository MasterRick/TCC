export type Questions = {
    id: number
    difficulty: number
    content: {
        question: string
        alternatives: string
        answer: string
        justification: string
    }

    descriptor: Descriptors
}

export type Descriptors = {
    id: number
    name: string
    content: string
    year: string
    classroom: string
    discipline: string
}

