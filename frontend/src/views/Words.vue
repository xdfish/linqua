<template>
    <v-sheet>
        <v-card elevation="0" width="400">
            <v-card-title>Update word database</v-card-title>
            <v-card-subtitle>Upload a SUBTLEX (or formatted similarly) xlsx file</v-card-subtitle>
            <v-card-text>
                <v-file-input counter outlined dense show-size v-model="wordsFile" :disabled="isUpdating" label="SUBTLEX (US) File" clearable hint="Processing may take several minutes" persistent-hint></v-file-input>
                <v-btn @click="uploadData" :disabled="!wordsFile" :loading="isUpdating" block>update</v-btn>
            </v-card-text>
        </v-card>
    </v-sheet>
</template>
    
<script>
/**
 * Man kann hier eine Subtlex Datei auswählen um die Datenbank mit Wörtern zu füllen
 */
import requests from '../requests';

export default {
    data: () => ({
        wordsFile: null,
        isUpdating: false,
    }),
    methods: {
        uploadData(){
            this.isUpdating = true
            const formData = new FormData()
            formData.append('data', this.wordsFile)
            requests.post('/api/words/update', formData).then(() => {
                alert('word db updated')
                this.wordsFile = null
                this.isUpdating = false
            }).catch(err => {
                this.wordsFile = null
                this.isUpdating = false
                alert(err)
            })
        }
    }
};
</script>