<template>
    <v-card elevation=0>
        <v-btn depressed block v-if="action != ''" @click="action=''"><v-icon left>mdi-arrow-left-circle</v-icon>back</v-btn>
        <v-card-text v-if="action=='add'">
            <v-select outlined dense label='Task Type' :items="taskTypes" v-model="task.task_type"></v-select>
            <v-textarea label='Task Text' outlined dense v-model="task.text"></v-textarea>
            <v-combobox label="Static Hitwords" outlined dense clearable v-model="task.hitwords" multiple small-chips></v-combobox>
            <template v-if="task.task_type == 'TALK-AUTOGEN'" >
                <v-row class="mt-1">
                    <v-col>
                        <v-select label='Word Class' outlined dense :items="word_classes" v-model="dynWordClass" hide-details :error-messages="dynWordClassErr"></v-select>
                    </v-col>
                    <v-col>
                        <v-slider label="Word Count:" v-model="dynWordCount" thumb-label="always" min="1" max="10" hide-details></v-slider>
                    </v-col>
                    <v-col cols="1" align=right>
                        <v-btn icon large @click="addDynamicHitword" color="primary"><v-icon>mdi-plus-box</v-icon></v-btn>
                    </v-col>
                </v-row>
                <v-combobox label="Dynamic Hitwords" :disabled="true" outlined dense v-model="task.dynamic_hitwords" multiple :chips="true">
                    <template v-slot:selection="data">
                        <v-chip small>{{ data.item.class }} ({{ data.item.count }})<v-btn icon small @click="removeDynamicHitword(data.item)"><v-icon small right>mdi-close-circle</v-icon></v-btn></v-chip>
                    </template>
                </v-combobox>
            </template>
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
/**
 * Hier kann der Benutzer (Admin) eine Aufgabe definieren und in die Aufgabenliste hinzufügen.
 */
import requests from '../requests';

const task_init = () => ({
    task_type: 'DESCRIBE',
    text: 'Build a scentence with the predetermined words',
    word_count_min: 0,
    word_count_best: 25,
    word_count_max: 100,
    hitwords: [],
    dynamic_hitwords: [],
    countdown: 15,
    time_limit: 20,
})

export default {

  data: () => ({
    action: '',
    taskTypes: ['DESCRIBE', 'TALK', 'TALK-AUTOGEN'],
    task: task_init(),
    tasks: [],
    countdown_a: false,
    max_time_a: false,
    min_words_a: false,
    best_words_a: false,
    max_words_a: false,
    word_classes: [],
    dynWordClass: '',
    dynWordClassErr: '',
    dynWordCount: 1,
  }),
    methods: {
    /**
     * Eingestellte Aufgabe wird ans Backend gesendet
     */
    async addTask(){
        const info = {
            text: this.task.text,
            hitwords: this.task.hitwords,
            countdown: this.countdown_a ? this.task.countdown : 0.0,
            time_limit: this.max_time_a ? this.task.time_limit : 0.0,
            word_count_min: this.min_words_a ? this.task.word_count_min : 0,
            word_count_best: this.best_words_a ? this.task.word_count_best: 0,
            word_count_max: this.max_words_a ? this.task.word_count_max : 0,
            dynamic_hitwords: this.task.dynamic_hitwords,
        }
        const formData = new FormData()
        formData.append('task_type', this.task.task_type)
        formData.append('task_data', JSON.stringify(info))
        requests.post('/api/task/add', formData).then(() => {
            this.task.hitwords = []
            alert('Task Added')
        }).catch(error => alert(error))
        },
    /**
     * Holen der Aufgaben aus der Datenbank
     */
    async showTasks(){
        requests.get('/api/task/list').then(tasks => {
            this.tasks = tasks
            this.action = 'list'
        }).catch(err => alert(err))
        },
    /**
     * Löschen einer Aufgabe aus der Datenbank
     * @param {*} id 
     */
    async deleteTask(id){
        const formData = new FormData()
        formData.append('id', id)
        requests.post('/api/task/delete', formData).then(() => {
            this.showTasks()
            alert(`Task ${id} removed`)
        }).catch(err => alert(err))
    },
    async getWordClasses(){
        requests.get('/api/words/classes').then((classes) => {
            this.word_classes = classes
        }).catch(err => alert(err))
        },
    /**
     * Fügt dynamische Wörter zu einer Aufgabe
     */
    addDynamicHitword(){
        if (this.dynWordClass == ''){
            this.dynWordClassErr = ' '
        }else{
            this.dynWordClassErr = ''
            this.task.dynamic_hitwords.push({
                class: this.dynWordClass,
                count: this.dynWordCount,
            })
            this.dynWordClass = ''
            this.dynWordCount = 1
        }
        
    },
    removeDynamicHitword(item){
        this.task.dynamic_hitwords = this.task.dynamic_hitwords.filter(function( elem ) {
            return elem.class !== item.class && elem.count !== item.count
        });
    },
  },
  created(){
    this.getWordClasses()
  }
};
</script>