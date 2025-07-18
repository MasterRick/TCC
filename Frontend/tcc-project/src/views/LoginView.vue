<template>
  <v-app>
    <v-container class="d-flex justify-center align-center" style="height: 100vh">
      <v-card class="mx-auto" width="350" outlined>
        <v-form ref="formRef" @submit.prevent="login" class="pa-4">
          <v-text-field
            v-model="email"
            :rules="emailRules"
            label="Email"
            type="email"
            required
            prepend-icon="mdi-email"
          ></v-text-field>
          <v-text-field
            v-model="password"
            :rules="passwordRules"
            label="Password"
            type="password"
            required
            prepend-icon="mdi-lock"
          ></v-text-field>
          <div class="d-flex flex-column">
            <v-btn class="mt-4" color="primary" block type="submit"> Login </v-btn>
          </div>
        </v-form>
      </v-card>
    </v-container>
  </v-app>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const formRef = ref()
const router = useRouter()

const emailRules = [
  (v: string) => !!v || 'Email is required',
  (v: string) => /.+@.+\..+/.test(v) || 'E-mail must be valid',
]
const passwordRules = [
  (v: string) => !!v || 'Password is required',
  (v: string) => v.length >= 6 || 'Password must be at least 6 characters',
]

const login = async () => {
  await formRef.value.validate().then((result: { valid: boolean }) => {
    console.log('Form valid:', result.valid)
    if (result.valid) {
      router.push('/')
    }
  })
}
</script>
