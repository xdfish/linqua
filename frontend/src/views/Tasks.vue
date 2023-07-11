<template>
    <v-card elevation=0>
        <v-btn depressed block v-if="action != ''" @click="action=''"><v-icon left>mdi-arrow-left-circle</v-icon>back</v-btn>
        <v-card-text v-if="action=='add'">
            <v-select outlined dense label='Task Type' :items="taskTypes" v-model="task.task_type"></v-select>
            <v-textarea label='Task Text' outlined dense v-model="task.text"></v-textarea>
            <v-combobox label="Hitwords" outlined dense clearable v-model="task.hitwords" multiple small-chips></v-combobox>
            <v-row class="pb-0">
                <v-col cols=4><v-switch v-model="countdown_a" inset label="countdown (s)" hide-details></v-switch></v-col>
                <v-col class="mt-5 pb-0"><v-slider v-model="task.countdown" thumb-label="always" min="1" :disabled="!countdown_a" hide-details></v-slider></v-col>
            </v-row>
            <v-row class="pb-0">
                <v-col cols=4><v-switch v-model="max_time_a" inset label="time limit (s)" hide-details></v-switch></v-col>
                <v-col class="mt-5 pb-0"><v-slider v-model="task.time_limit" thumb-label="always" min="1" :disabled="!max_time_a" hide-details></v-slider></v-col>
            </v-row>
            <v-row class="pb-0" >
                <v-col cols=4><v-switch v-model="min_words_a" inset label="min words"  hide-details></v-switch></v-col>
                <v-col class="mt-5 pb-0"><v-slider v-model="task.word_count_min" thumb-label="always" min="1" :max="task.word_count_best-1" :disabled="!min_words_a" hide-details></v-slider></v-col>
            </v-row>
            <v-row class="pb-0" >
                <v-col cols=4><v-switch v-model="best_words_a" inset label="best words"  hide-details></v-switch></v-col>
                <v-col class="mt-5 pb-0"><v-slider v-model="task.word_count_best" thumb-label="always" :min="task.word_count_min ? task.word_count_min+1 : 1" :disabled="!best_words_a" hide-details></v-slider></v-col>
            </v-row>
            <v-row class="pb-0" >
                <v-col cols=4><v-switch v-model="max_words_a" inset label="max words"  hide-details></v-switch></v-col>
                <v-col class="mt-5 pb-0"><v-slider v-model="task.word_count_max" thumb-label="always" :min="task.word_count_min" :disabled="!max_words_a" hide-details></v-slider></v-col>
            </v-row>
          <v-btn rounded outlined color="primary" block class="mt-5" @click="addTask"> Create Task</v-btn>
        </v-card-text>
        <v-card-text v-else-if="action == 'list'">
            <v-list>
                <v-list-item v-for="id in tasks" :key="id">
                    <v-list-item-title>{{id}}</v-list-item-title>
                    <v-list-item-action>
                        <v-btn icon small color=red @click="deleteTask(id)"><v-icon>mdi-trash-can</v-icon></v-btn>
                    </v-list-item-action>
                </v-list-item>
            </v-list>
        </v-card-text>
        <v-card-text v-else>
            <v-row align="center" justify="center">
                <v-col>
                    <v-card-title>Task List</v-card-title>
                    <v-btn icon x-large fab outlined class="ml-6" @click="showTasks"><v-icon>mdi-clipboard-list</v-icon></v-btn>
                </v-col>
                <v-col>
                    <v-card-title>Add Task</v-card-title>
                    <v-btn icon x-large fab outlined class="ml-6" @click="action='add'"><v-icon>mdi-file-document-plus</v-icon></v-btn>
                </v-col>
            </v-row>
        </v-card-text>
    </v-card>
</template>

<script>
import requests from '../requests';

const task_init = () => ({
    task_type: 'DESCRIBE',
    text: 'Build a scentence with the predetermined words',
    word_count_min: 0,
    word_count_best: 25,
    word_count_max: 100,
    hitwords: [],
    countdown: 15,
    time_limit: 20
})

export default {

  data: () => ({
    action: '',
    taskTypes: ['DESCRIBE', 'TALK'],
    task: task_init(),
    tasks: [],
    countdown_a: false,
    max_time_a: false,
    min_words_a: false,
    best_words_a: false,
    max_words_a: false,
  }),
  methods: {
    async addTask(){
        const info = {
            text: this.task.text,
            hitwords: this.task.hitwords,
            countdown: this.countdown_a ? this.task.countdown : 0.0,
            time_limit: this.max_time_a ? this.task.time_limit : 0.0,
            word_count_min: this.min_words_a ? this.task.word_count_min : 0,
            word_count_best: this.best_words_a ? this.task.word_count_best: 0,
            word_count_max: this.max_words_a ? this.task.word_count_max : 0,
        }
        const formData = new FormData()
        formData.append('task_type', this.task.task_type)
        formData.append('task_data', JSON.stringify(info))
        requests.post('/api/task/add', formData).then(() => {
            this.task = task_init()
            alert('Task Added')
        }).catch(error => alert(error))
    },
    async showTasks(){
        requests.get('/api/task/list').then(tasks => {
            this.tasks = tasks
            this.action = 'list'
        }).catch(err => alert(err))
    },
    async deleteTask(id){
        const formData = new FormData()
        formData.append('id', id)
        requests.post('/api/task/delete', formData).then(() => {
            this.showTasks()
            alert(`Task ${id} removed`)
        }).catch(err => alert(err))
    }
  }
};
</script>