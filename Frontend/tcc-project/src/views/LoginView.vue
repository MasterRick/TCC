<template>
  <v-app>
    <v-container class="d-flex justify-center align-center" style="height: 100vh">
      <v-card class="mx-auto" width="350" outlined>
        <v-form ref="formRef" @submit.prevent="login" class="pa-4">
          <v-text-field
            v-model="email"
            :rules="emailRules"
            label="E-mail"
            type="email"
            required
            prepend-icon="mdi-email"
          ></v-text-field>
          <v-text-field
            v-model="password"
            :rules="passwordRules"
            label="Senha"
            type="password"
            required
            prepend-icon="mdi-lock"
          ></v-text-field>
          <div class="d-flex flex-column">
            <v-btn class="mt-4" color="primary" block type="submit"> Entrar </v-btn>
          </div>
        </v-form>
      </v-card>
    </v-container>
  </v-app>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { loginApi } from '@/api/routers'
import { useLoadingStore } from '@/stores/loadingStore'
const loadingStore = useLoadingStore()

const email = ref('')
const password = ref('')
const formRef = ref()
const router = useRouter()

const emailRules = [
  (v: string) => !!v || 'E-mail é obrigatório',
  (v: string) => /.+@.+\..+/.test(v) || 'E-mail deve ser válido',
]
const passwordRules = [
  (v: string) => !!v || 'Senha é obrigatória',
  (v: string) => v.length >= 6 || 'Senha deve ter pelo menos 6 caracteres',
]

const login = async () => {
  loadingStore.showLoading('Entrando...')
  await formRef.value.validate().then((result: { valid: boolean }) => {
    if (result.valid) {
      loginApi(email.value, password.value)
        .then(() => {
          router.push({ name: 'Início' })
        })
        .catch((error) => {
          console.error('Falha no login:', error)
        })
        .finally(() => {
          loadingStore.hideLoading()
        })
    }
  })
}
</script>
