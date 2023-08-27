<template>
    <div>
        <v-navigation-drawer v-model="drawer" app>
          <v-list>
            <v-list-item>
              <v-list-item-avatar><v-img :src=avatarUri sty></v-img></v-list-item-avatar>
              <v-list-item-content>{{this.user.role}}</v-list-item-content>
              <v-list-item-action><v-btn color="red" outlined small fab @click="logout"><v-icon>mdi-logout</v-icon></v-btn></v-list-item-action>
            </v-list-item>
            <v-list-item link :to="{name: 'profile'}">
              <v-list-item-content>
                <v-list-item-title>{{this.user.username}}</v-list-item-title>
                <v-list-item-subtitle>{{this.user.firstname}} {{this.user.lastname}}</v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <v-icon>mdi-account-wrench</v-icon>
              </v-list-item-action>
            </v-list-item>
          </v-list>
          <v-divider></v-divider>
          <v-list>
            <v-list-item link :to="{name: 'tasks'}">
              <v-list-item-icon>
                <v-icon>mdi-book-open-page-variant</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>Manage Tasks</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item link :to="{name: 'words'}">
              <v-list-item-icon>
                <v-icon>mdi-database-sync-outline</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>Manage Word DB</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item disabled>
              <v-list-item-icon>
                <v-icon>mdi-account-group</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>Manage Users</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
          <v-divider></v-divider>
          <v-list>
            <v-list-item link :to="{name: 'home'}">
              <v-list-item-icon>
                <v-icon>mdi-play</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>Start Session</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-navigation-drawer>
        <v-app-bar app>
          <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
          <v-toolbar-title>LINQUA</v-toolbar-title>
        </v-app-bar>
        <v-main>
        <router-view/>
        </v-main>
    </div>
</template>

<script>
/**
 * Hier findet eine Liste von den Links, die zu anderen Komponenten der Anwendung führen.
 */
import requests from '../requests.js'
const avatarUri = 'https://avataaars.io/?avatarStyle=Transparent&topType=ShortHairShortCurly&accessoriesType=Prescription02&hairColor=Black&facialHairType=Blank&clotheType=Hoodie&clotheColor=White&eyeType=Default&eyebrowType=DefaultNatural&mouthType=Default&skinColor=Light'
  export default {
    data: () => ({ 
      drawer: null,
      avatarUri: avatarUri,
      user: {
        username: '',
        firstname: '',
        lastname: '', 
      }
    }),
  methods: {
      /**
       * Diese Methode lädt die Details eines Benutzers
       */
      loadUserData(){
        requests.get('/api/user').then(content => {
          this.user.username = content.username
          this.user.firstname = content.first_name
          this.user.lastname = content.last_name
          this.user.email = content.email
          this.user.role = content.role
        }).catch(() => {})
    },
      /**
       * Diese Methode meldet den Benutzer ab
       */
      logout(){
        requests.post('/api/logout').then(() => {
          this.$router.push('/Login')
        }).catch((err) => alert(err))
      }
    },
    created(){
      this.loadUserData()
    }
  }
</script>
