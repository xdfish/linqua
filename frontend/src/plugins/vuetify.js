import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';
import AudioRecorder from 'vue-audio-recorder'

// Vuetify ist ein Component Framework
Vue.use(Vuetify);

// AudioRecorder wird benutzt um Sprache aufzunehmen
Vue.use(AudioRecorder)

export default new Vuetify({
});
