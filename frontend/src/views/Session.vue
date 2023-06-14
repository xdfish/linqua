<template>
    <v-card class="pa-5" height=500>
        <template v-if="this.$route.params.type == 'describe'">
            <v-row align="center" justify="center" v-if="curTask == -1">
                <v-btn class="mt-12" @click="setTask(0)">START {{this.$route.params.type}} SESSION</v-btn>
            </v-row>
            <v-row v-else>
                <v-card width=100%>
                    <v-card-subtitle>Task {{curTask + 1}} of {{maxTasks}}</v-card-subtitle>
                    <v-card-title>{{tasks[curTask].text}}</v-card-title>
                    <v-card-text>
                        <div style="width: 400px; margin: auto; text-align: center;">
                            <audio-recorder :attempts="1" :after-recording="solveTask" :show-upload-button="false"/>
                        </div>
                    </v-card-text>
                    <v-card-text v-if="nextEnabled">
                        <v-row>
                            <v-col>Recognized text:</v-col>
                            <v-col>{{score[curTask].text}}</v-col>
                        </v-row>
                        <v-row>
                            <v-col>Score for length of the scentence:</v-col>
                            <v-col>{{score[curTask].score_length}}/100</v-col>
                        </v-row>
                        <v-row>
                            <v-col>Score for used hitwords:</v-col>
                            <v-col>{{score[curTask].score_hitword}}/100</v-col>
                        </v-row>
                        <v-row>
                            <v-col>Score for grammar:</v-col>
                            <v-col>{{score[curTask].score_grammar}}/100</v-col>
                        </v-row>
                        <v-row v-for="(err, index) in score[curTask].grammar_errors" :key="index">
                            <v-col>Grammar Hint ({{index}}):</v-col>
                            <v-col>{{err.message}}</v-col>
                        </v-row>
                    </v-card-text>
                    <v-card-actions :key="nextEnabled">
                        <v-btn :disabled="!nextEnabled" @click="setTask(curTask+1)">next task</v-btn>
                    </v-card-actions>
                </v-card>
            </v-row>
        </template>
    </v-card>
</template>

<script>
import requests from '../requests';


export default {
  data: () => ({
    tasks: [null, null, null, null, null, null, null, null, null, null],
    score: [null, null, null, null, null, null, null, null, null, null],
    nextEnabled: false,
    maxTasks: 10,
    curTask: -1,
  }),
  methods: {
    async setTask(curTask){
        this.nextEnabled = false
        if (this.tasks[curTask] == null){
            const excludeIds = this.tasks.reduce((prev, curr) => {
                if (curr != null) {
                    prev.push(curr.taskid)
                }
                return prev
            }, [])
            const formData = new FormData()
            formData.append('exclude_ids', JSON.stringify(excludeIds))
            requests.post('api/task/random', formData).then(task => {
                this.tasks[curTask] = task
                this.curTask = curTask
            }).catch(err => alert(err))  
        }else{
            this.curTask = curTask
        }
    },
    async solveTask(data){
        const formData = new FormData()
        formData.append('id', this.tasks[this.curTask].taskid)
        formData.append('record', data.blob, 'record.mp3')
        requests.post('/api/task/solve', formData).then(result => {
            this.score[this.curTask] = result
            this.nextEnabled = true
        }).catch(err => alert(err))
    }
  },
  mounted(){
  },
};
</script>

<style>
h3 {
  margin: 40px 0 0;
}

.ar-records {
  display: none !important;
}

.ar-player {
  display: none !important;
}
</style>