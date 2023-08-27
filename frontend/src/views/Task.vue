<template>
    <v-card width="100%" elevation="0" class="mt-2">
      <v-card height="490" v-if="isComplete" class="d-flex flex-column">
        <v-card-title>
          <v-spacer></v-spacer><h1 class="txt-final mb-10">You did it!</h1><v-spacer></v-spacer>
        </v-card-title>
        <v-spacer></v-spacer>
        <v-row>
          <v-col align="center">
              <b>{{ scoreCheer }}</b>
              <v-rating v-model="scoreProgress" :length="5" color="primary" large readonly half-increments></v-rating>
              <p v-if="scoreCheer!='-'"> You solved <b>{{ prevScores.length }}</b> tasks of type: <b>{{ taskType }}</b> with an average rating of <b>[{{ score.total.toFixed(2) }}/5]</b></p>
              <p v-if="difficulty!=undefined">Difficulty: {{ difficulty }}/2</p>
            </v-col>
        </v-row>
        <v-spacer></v-spacer>
        <v-card-actions>
          <v-spacer></v-spacer><v-btn @click="$router.go(-1)">ok</v-btn><v-spacer></v-spacer>
        </v-card-actions>
      </v-card>
      <template v-else>
        <v-card elevation="1" height="320" class="d-flex flex-column" v-if="!isLoading">
          <v-overlay :absolute="true" :value="showTaskText">
            <v-card color="transparent" elevation=0>
              <div class="ts-text ts-heading"><b>{{task.text}}</b></div>
              <div class="ts-text mt-4">The scentence must consist of at least <b><u> {{ task.minWordCount }} words </u></b></div>
              <div class="ts-text mt-2">Read the words of the task while the countdown of <b><u>{{task.countdown }} seconds</u></b>  below running down.</div>
              <div class="ts-text mt-2">You have <b><u>{{ task.timeLimit }} seconds</u></b> to say your solution scentence after the countdown ends</div>
            </v-card>
            <v-row>
              <v-col align=center>
                <v-btn @click="startCountdown" color="green" class="mt-5" v-if="!isSolved">start</v-btn>
                <v-btn @click="showTaskText=false" outlined dark class="mt-5" v-else>ok</v-btn>
              </v-col>
            </v-row>
          </v-overlay>
          <v-btn absolute right icon v-if="!showTaskText" :disabled="isCounting || isRecording"><v-icon large @click="showTaskText=true">mdi-chat-question</v-icon></v-btn>
          <v-btn absolute left text :disabled="true">task {{this.prevTasks.length + 1}} of {{this.sessionLength}}</v-btn>
          <v-card-text v-if="!showTaskText" fill-height class="mt-10">
            <v-col justify="center" align="center" v-if="!showDetails"><v-chip class="mt-2 mx-2" color="primary" outlined pill v-for="word in task.words" :key="word">{{word}}</v-chip></v-col>
            <v-col justify="center" align="center" v-else><v-chip class="mt-2 mx-2 pb-0" :color="hitwordProgress.indexOf(word) > -1 ? 'green': 'red'" outlined pill v-for="word in task.words" :key="word">{{word}}</v-chip></v-col>
            <v-col align="center" class="pt-0 pb-0" v-if="showDetails">Hitwords used: {{ hitwordProgress.length }} / {{ task.words.length }} (score: {{ score.words.toFixed(2) }} of 5)</v-col>
          </v-card-text>
          <v-spacer></v-spacer>
          <template v-if="isSolved && showDetails && !showTaskText">
            <v-card-actions class="pb-0" v-if="score.error.length > 0"><v-row><v-col align="center"><v-btn icon :disabled="grammarShow < 0" @click="--grammarShow; showGrammarText(grammarShow)"><v-icon>mdi-chevron-left-circle-outline</v-icon></v-btn><v-icon color="red">mdi-lightbulb-alert-outline</v-icon><v-btn icon :disabled="grammarShow >= score.error.length-1" @click="++grammarShow; showGrammarText(grammarShow)"><v-icon>mdi-chevron-right-circle-outline</v-icon></v-btn></v-col></v-row></v-card-actions>
            <v-card-actions class="pt-0">
              <v-row>
                <v-col align="center">
                  <v-menu offset-y v-for="txt in grammarText" :key="txt.text">
                    <template v-slot:activator="{ on, attrs }">
                      <v-chip v-on="on" v-bind="attrs" label :color="txt.err ? 'red' : ''">{{ txt.text }}</v-chip>
                    </template>
                    <v-card v-if="txt.err" elevation="0"><v-card-text>{{txt.msg}}</v-card-text></v-card>
                  </v-menu>
                    </v-col>
              </v-row>
            </v-card-actions>
            <v-card-text class="mt-0 pt-0 pb-0"><v-row><v-col align="center">Total words: {{ score.textWords.length }} / {{ task.minWordCount }} (score: {{ (score.length).toFixed(2) }} of 5)</v-col></v-row></v-card-text>
          </template>
          <v-card-actions>
            <v-row>
              <v-col align=left><v-icon>mdi-timer-sand-complete</v-icon><span>{{task.countdown}}s</span></v-col>
              <v-col align=center><v-icon>mdi-counter</v-icon> > {{task.minWordCount}} words</v-col>
              <v-col align=right><v-icon left>mdi-timer-alert-outline</v-icon><span>{{task.timeLeft.toFixed(2)}}s</span></v-col>
            </v-row>
          </v-card-actions>
        </v-card>
        <v-card elevation="1" height="320" class="d-flex flex-column" v-else :loading="isLoading"></v-card>
        <v-progress-linear :buffer-value="isRecording ? 0 : 100" :value="timeProgress" stream :color="isRecorded ? 'green' : 'primary'" height="15"></v-progress-linear>
        <v-card elevation="0">
          <audio-recorder v-if="!isRecorded" style="height: 150px; overflow: hidden; width: 100%;" ref="recorder" :after-recording="solveTask"></audio-recorder>
          <v-card height="150" v-else class="mt-3">
            <v-row>
              <v-col class="fill-height" align="center">
                <v-progress-circular :rotate="-90" :size="100" :width="15" color="green" indeterminate v-if="!isSolved" style="margin: auto;"></v-progress-circular>
                <template v-else >
                  <b>{{ scoreCheer }}</b>
                  <v-rating v-model="scoreProgress" :length="5" color="primary" large readonly half-increments></v-rating>
                  <b v-if="scoreCheer!='-'">[{{ score.total.toFixed(2) }}/5]</b>
                </template>
              </v-col>
            </v-row>
          </v-card>
          <v-btn absolute top right icon v-if="isSolved" @click="showDetails=!showDetails"><v-icon>{{showDetails ? 'mdi-eye-off':'mdi-google-analytics'}}</v-icon></v-btn>
          <v-btn absolute bottom right dark depressed rounded @click="startRecord()" :disabled="isRecording || isLoading" v-if="!isRecorded && !task.countdown" color="green">START</v-btn>
          <v-btn absolute bottom right outlined rounded @click="stopRecord()" v-if="isRecording">STOP RECORD</v-btn>
          <v-btn absolute bottom right outlined rounded @click="nextTask()" :disabled="isRecording" v-if="isRecorded && isSolved">NEXT</v-btn>
          <v-btn absolute bottom left outlined rounded :disabled="isRecording" color="red" @click="$router.go(-1)">END SESSION</v-btn>
          <v-overlay :absolute="true" :value="task.isCounting" v-if="isCounting">
            <v-row>
              <v-col cols="2"></v-col>
              <v-col align="center"><v-icon size="80">mdi-numeric-{{task.countdown}}-circle</v-icon></v-col>
              <v-col cols="2" align="right"><v-btn class="mt-6 ml-15" outlined rounded @click="task.countdown=1">SKIP</v-btn></v-col>
            </v-row>
          </v-overlay>
        </v-card>
      </template>
    </v-card>
  </template>
  

  <script>
/**
 * Hier sieht der Benutzer die Details zu einer Aufgabe z.B. Hinweise, Korrektur. Er kann Sprache aufnehmen. Er kann zur nächsten Aufgabe springen
 */
    const scoreText = ["Are you kidding?", "Don't stop practicing!", "You can do better!" , "Good job!" ,"Well done!" ,"Perfect!"]
    const difficultyFreq = [ //Min and Max Frequency of the words
      [0.8, 1.0], //EASY
      [0.3, 0.8], //MEDIUM
      [0.0, 0.3], //HARD
    ]
    import requests from '../requests';
    export default {
      props: {
        taskType: {
          type: String,
          required: true
        },
        sessionLength: {
          type: Number,
          required: true
        },
        difficulty: {
          type: Number,
          required: false
        }
      },
      data: () => ({
        task: {
          taskid: '',
          text: '',
          minWordCount: 0,
          countdown: 0,
          timeLimit: 0,
          timeLeft: 0,
          words: [],
          tmpid: undefined
        },
        score: {
          total: 0,
          length: 0,
          words: 0,
          used: [],
          text: '',
          textWords: [],
        },
        prevTasks: [],
        prevScores: [],
        timeProgress: 0,
        scoreProgress: 0.0,
        hitwordProgress: [],
        scoreCheer: '-',
        grammarShow: -1,
        grammarText: [],
        isLoading: false,
        isRecording: false,
        isRecorded: false,
        isSolved: false,
        isCounting: false,
        isComplete: false,
        updateId: null,
        showTaskText: true,
        showDetails: false,
      }),
      methods: {
        recordProgress () {
          this.timeProgress = (this.$refs.recorder.recorder.duration / this.task.timeLimit) * 100
          this.task.timeLeft = this.task.timeLeft - 0.05
          if (this.timeProgress >= 100){
            this.task.timeLeft = 0
            this.stopRecord() 
          }
        },
        /**
         * Sprache wird aufgenommen
         */
        startRecord () {
          this.$refs.recorder.toggleRecorder()
          this.isRecording = true
          if (this.task.timeLimit > 0){
            this.updateId = setInterval(this.recordProgress, 50)
          }
        },
        /**
         * Aufnahme wird gestoppt
         */
        stopRecord () {
          this.$refs.recorder.stopRecorder()
          this.isRecording = false
          this.isRecorded = true
          clearInterval(this.updateId)
        },
        startCountdown () {
          this.showTaskText = false
          this.isCounting = true
          const cuntdownId = setInterval(() => {
            this.task.countdown = this.task.countdown - 1
            if (this.task.countdown < 1){
              this.isCounting = false
              this.startRecord()
              clearInterval(cuntdownId)
            }
          }, 1000)
        },
        /**
         * Sprache wird an Backend übergeben und Aufgabe wird somit gelöst
         * @param {*} record 
         */
        async solveTask(record){
          const formData = new FormData()
          formData.append('id', this.task.taskid)
          formData.append('task_type', this.taskType)
          formData.append('record', record.blob, 'record.mp3')
          formData.append('tmpid', this.task.tmpid)           //only for tasks with tmp functionality
          requests.post('/api/task/solve', formData).then(score => {
              this.setScore(score)
              this.isSolved = true
          }).catch(err => alert(err))
        },
        /**
         * Nächste Aufgabe wird ausgewählt
         */
        nextTask () {
          this.isLoading = true
          this.showDetails = false
          if (this.task.taskid){
            this.showTaskText = false
            this.prevTasks.push(this.task.taskid)
            this.prevScores.push(this.score.total)
            if (this.prevTasks.length == this.sessionLength){
              this.showFinal()
              return
            }
          }
          const formData = new FormData()
          formData.append('task_type', this.taskType)
          formData.append('exclude_ids', JSON.stringify(this.prevTasks))
          if (this.difficulty != undefined){
            const freqData = {
              min_freq: difficultyFreq[this.difficulty][0], 
              max_freq: difficultyFreq[this.difficulty][1]
            }
            formData.append('auto_data', JSON.stringify(freqData))
          }
          requests.post('/api/task/random', formData).then(task => {
            this.setTask(task)
            const notFirstTask = this.isSolved
            this.isRecorded = false
            this.isLoading = false
            this.isSolved = false
            if (notFirstTask && this.task.countdown > 0){
              this.startCountdown()
            }
          }).catch(err => alert(err))
        },
        /**
         * Die nächste Aufgabe wird gesetzt
         * @param {*} nextTask 
         */
        setTask(nextTask){
          this.task.taskid = nextTask.taskid
          this.task.text = nextTask.text
          this.task.minWordCount = nextTask.word_count_min
          this.task.countdown = nextTask.countdown
          this.task.timeLimit = nextTask.time_limit
          this.task.timeLeft = nextTask.time_limit
          this.task.words = nextTask.hitwords
          this.task.tmpid = nextTask.tmpid
        },
        /**
         * Bewertung wird gesetzt
         * @param {*} curScore 
         */
        setScore(curScore){
          this.score.length = curScore.score.length/20
          this.score.words = curScore.score.hitwods/20
          this.score.total = (this.score.length + this.score.words)/2
          this.score.text = curScore.text_recognized
          this.score.textWords = curScore.words_recognized
          this.score.error = curScore.grammar_errors
          this.score.used = curScore.hitwords_used
          this.grammarShow = -1                     //reset displyed grammar error
          this.showGrammarText(this.grammarShow)    //grammar text setup
          this.showHitwords()
          this.animateScore()                       //
        },
        animateScore(){
          this.scoreProgress = 0
          this.scoreCheer = '-'
          this.scoreText = ''
          this.scoreCheer = scoreText[Math.round(this.score.total)]
          const scoreId = setInterval(() => {
            if (this.scoreProgress < this.score.total){
              const scoreDiff = this.score.total - this.scoreProgress
              if (scoreDiff < 1){
                this.scoreProgress = this.scoreProgress + scoreDiff
              }else{
                this.scoreProgress = this.scoreProgress + 1
              }
            }else{
              
              this.scoreText = this.score.text
              clearInterval(scoreId);
            }
          }, 300)
        },
        showHitwords(){
          this.hitwordProgress = []
          this.score.used.forEach(elem => {
            if (elem.present){
              this.hitwordProgress.push(elem.word)
            }
          })
        },
        showGrammarText(errIndex){
          if (errIndex == -1){
            this.grammarText = [{text: this.score.text, err: false}]
          }else{
            const error = this.score.error[errIndex]
            this.grammarText = []
            this.grammarText.push({text: this.score.text.substring(0, error.offset), err: false, msg: ''})
            this.grammarText.push({text: this.score.text.substring(error.offset, error.offset + error.length), err: true, msg: error.message})
            this.grammarText.push({text: this.score.text.substring(error.offset + error.length, this.score.text.length), err: false, msg: ''})
          }
        },
        showFinal(){
          this.score.total = (this.prevScores.reduce((a, b) => a + b, 0.0) / this.prevScores.length) || 0.0;
          this.isComplete = true
          this.animateScore()
        },
      },
      created () {
        this.nextTask()
      }
    }
  //TODO:
  // change '/Home' link
  // 
  </script>
  
  <style>
  .ar-recorder{
    pointer-events: none;
  }
  
  .ts-text{
    text-align: center;
  }
  .ts-heading{
    font-size: 20px;
  }
  .err-text{
    font-weight: bold;
    color: red;
  }
  </style>
  