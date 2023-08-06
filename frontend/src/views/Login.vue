<template>
    <v-container fill-height fluid>
        <v-row align="center" justify="center">
            <v-col>
                <v-img height="150" :src="require('@/assets/logo.png')" width="100%" aspect-ratio="1"></v-img>
                <v-form @submit="login">
                  <v-text-field label="username" prepend-inner-icon="mdi-account" filled rounded dense v-model="username" :error-messages="usernameError"></v-text-field>
                  <v-text-field label="password" prepend-inner-icon="mdi-lock" filled rounded dense v-model="password" type="password" :error-messages="passwordError"></v-text-field>
                  <v-btn class="mt-5" rounded outlined color="blue" width="100%" type="submit">Login</v-btn>
                </v-form>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import requests from '../requests.js'

export default {
  data: () => ({
    username: '',
    password: '',
    usernameError: '',
    passwordError: '',
  }),
  methods: {
    async login(){
      if (this.validate()){
        const formData = new FormData()
        formData.append('username', this.username)
        formData.append('password', this.password)
        requests.post('/api/login', formData, false).then( () => {
           this.$router.push('/home')
        }).catch((err) => {
            this.usernameError = ' '
            this.passwordError = err == 'Unauthorized' ? 'username or password incorrect' : err
          }
        )
      }
    },
    validate(){
      this.usernameError = this.username.trim().length == 0 ? 'enter username'  : ''
      this.passwordError = this.password.trim().length == 0 ? 'enter password'  : ''
      return (this.usernameError + this.passwordError).length == 0
    }
  }
};
</script>