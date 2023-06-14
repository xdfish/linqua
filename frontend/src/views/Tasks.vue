<template>
    <v-card elevation=0>
        <v-btn depressed block v-if="action != ''" @click="action=''"><v-icon left>mdi-arrow-left-circle</v-icon>back</v-btn>
        <v-card-text v-if="action=='add'">
            <v-select outlined dense label='Task Type' :items="taskTypes" v-model="task.task_type"></v-select>
            <v-textarea label='Task Text' outlined dense v-model="task.text"></v-textarea>
            <v-combobox label="Hitwords" outlined dense clearable v-model="task.hitwords" multiple small-chips></v-combobox>
            Min/Max word count
            <v-range-slider v-model="task.word_range" :max="25" :min="0" hide-details class="align-center">
            <template v-slot:prepend>
              <v-text-field
                :value="task.word_range[0]"
                class="mt-0 pt-0"
                hide-details
                single-line
                type="number"
                style="width: 60px"
                @change="$set(task.word_range, 0, $event)"
              ></v-text-field>
            </template>
            <template v-slot:append>
              <v-text-field
                :value="task.word_range[1]"
                class="mt-0 pt-0"
                hide-details
                single-line
                type="number"
                style="width: 60px"
                @change="$set(task.word_range, 1, $event)"
              ></v-text-field>
            </template>
          </v-range-slider>
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
    text: '',
    word_range: [0, 25],
    hitwords: []
})

export default {

  data: () => ({
    action: '',
    taskTypes: ['DESCRIBE'],
    task: task_init(),
    tasks: []
  }),
  methods: {
    async addTask(){
        const info = {
            text: this.task.text,
            word_count_min: this.task.word_range[0],
            word_count_best: this.task.word_range[1],
            hitwords: this.task.hitwords
        }
        const formData = new FormData()
        formData.append('info', JSON.stringify(info))
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