<template>
    <v-container fill-height fluid>
        <v-row align="center" justify="center">
            <v-col>
                <v-img height="150" :src="require('@/assets/logo.png')" width="100%" aspect-ratio="1"></v-img>
                <v-text-field label="username" prepend-inner-icon="mdi-account" filled rounded dense v-model="username"></v-text-field>
                <v-text-field label="password" prepend-inner-icon="mdi-lock" filled rounded dense v-model="password"></v-text-field>
                <v-btn class="mt-5" rounded outlined color="blue" width="100%" @click="login(username, password)">Login</v-btn>
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
  }),
  methods: {
    async login(username, password){
        const formData = new FormData()
        formData.append('username', username)
        formData.append('password', password)
        requests.post('/api/login', formData, false).then( () => {
           this.$router.push('/home')
        }).catch((err) => {alert(err)})
    }
  }
};
</script>