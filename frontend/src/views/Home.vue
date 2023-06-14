<template>
  <div>
    <v-card elevation=0>
      <v-card-text>Select a task to start your session</v-card-text>
    </v-card>
    <v-card class="ma-4">
      <v-row align="center" justify="center">
        <v-col>
          <v-card-title>Describe</v-card-title>
          <v-card-text>
            <v-row  align="center" class="mx-0">
              <v-rating :value="tasks[0].score" color="amber" dense half-increments readonly size="14"></v-rating>
              <div class="grey--text ms-4">Your score: {{tasks[0].score}} (5.0)</div>
            </v-row>
          </v-card-text>
        </v-col>
        <v-col cols="2">
          <v-btn color="green" outlined small fab to="/session/describe"><v-icon>mdi-play</v-icon></v-btn>
        </v-col>
      </v-row>
    </v-card>
    <v-card class="ma-4">
      <v-row align="center" justify="center">
        <v-col>
          <v-card-subtitle>More is comming soon!</v-card-subtitle>
        </v-col>
      </v-row>
    </v-card>
  </div>

</template>

<script>
export default {
  name: 'Home',
  data: () => ({
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
