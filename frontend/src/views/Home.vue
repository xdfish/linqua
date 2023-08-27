<template>
  <v-sheet>

    <v-card elevation=0>
      <v-card-text>Select a task to start your session</v-card-text>
    </v-card>

    <v-card class="ma-4 mt-3" :disabled="true">
      <v-toolbar color="primary" dark dense class="mb-4">
        <v-toolbar-title>Describe</v-toolbar-title>
      </v-toolbar>
      <v-row align="center" justify="center">
        <v-col>
          <v-card-text>
            <v-row  align="center" class="mx-0">
              <v-rating :value="tasks[0].score" color="amber" dense half-increments readonly size="14"></v-rating>
              <div class="grey--text ms-4">Your avg score: {{tasks[0].score}} (5.0)</div>
              <v-spacer></v-spacer>
              <v-text-field label="Session length" v-model="lengthDescribe" outlined dense class="" type="number" style="width: 60px" hide-details></v-text-field>
            </v-row>
          </v-card-text>
        </v-col>
        <v-col cols="2">
          <v-btn color="green" outlined small fab to="/session/describe"><v-icon>mdi-play</v-icon></v-btn>
        </v-col>
      </v-row>
    </v-card>

    <v-card class="ma-4 mt-10">
      <v-toolbar color="primary" dark dense class="mb-4">
        <v-toolbar-title>Talk</v-toolbar-title>
      </v-toolbar>
      <v-row align="center" justify="center">
        <v-col>
          <v-card-text>
            <v-row  align="center" class="mx-0">
              <v-rating :value="4.92" color="amber" dense half-increments readonly size="14"></v-rating>
              <div class="grey--text ms-4">Your avg score: 4.92 / (5.0)</div>
              <v-spacer></v-spacer>
              <v-text-field label="Session length" v-model="lengthTalk" outlined dense class="" type="number" style="width: 60px" hide-details></v-text-field>
            </v-row>
          </v-card-text>
        </v-col>
        <v-col cols="2">
          <v-btn color="green" outlined small fab :to="{ name : 'task', params: { taskType: 'TALK', sessionLength: lengthTalk }}"><v-icon>mdi-play</v-icon></v-btn>
        </v-col>
      </v-row>
    </v-card>

    <v-card class="ma-4 mt-10">
      <v-toolbar color="primary" dark dense class="mb-4">
        <v-toolbar-title>Talk (Auto Generated)</v-toolbar-title>
      </v-toolbar>
      <v-row align="center" justify="center">
        <v-col>
          <v-card-text>
            <v-slider v-model="difficulty" :tick-labels="['Easy', 'Medium', 'Hard']" :min="0" :max="2" step="1" ticks="always" tick-size="1"></v-slider>
            <v-row  align="center" class="mx-0 pt-3">
              <v-rating :value="1.2 + (3.0 - difficulty)" color="amber" dense half-increments readonly size="14" class="mb-2"></v-rating>
              <div class="grey--text ms-4">Your avg score: {{1.2 + (3.0 - difficulty)}} (5.0)</div>
              <v-spacer></v-spacer>
              <v-text-field label="Session length" v-model="lengthTalkAuto" outlined dense class="" type="number" style="width: 60px" hide-details></v-text-field>
            </v-row>
          </v-card-text>
        </v-col>
        <v-col cols="2">
          <v-btn color="green" outlined small fab :to="{ name : 'task', params: { taskType: 'TALK-AUTOGEN', sessionLength: lengthTalkAuto, difficulty: difficulty}}"><v-icon>mdi-play</v-icon></v-btn>
        </v-col>
      </v-row>
    </v-card>
    
    <v-card class="ma-4" elevation="0">
      <v-row align="center" justify="center">
        <v-col>
          <v-card-subtitle>More is comming soon!</v-card-subtitle>
        </v-col>
      </v-row>
    </v-card>
  </v-sheet>

</template>

<script>
/**
 *  In Home sieht man eine kleine Übersicht über die erreichten Punkte. Man kann hier die Schwierigkeiten der Aufgaben einstellen
 * */ 
export default {
  name: 'Home',
  data: () => ({
    difficulty: 0,
    lengthDescribe: 10,
    lengthTalk: 10,
    lengthTalkAuto: 10,
    tasks: [
      {
        name: 'Describe',
        score: 3.0,
        count: 13,
        icon: 'mdi-image-text'
      }
    ]
  }),
}
</script>
