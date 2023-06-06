import { Injectable } from '@angular/core';
import { StereoAudioRecorder } from 'recordrtc';
import { Subject } from "rxjs";

export class AudioFile {
  blob: Blob;
  title: string;
}

@Injectable({
  providedIn: 'root'
})
export class AudioRecordingService {

  constructor() { }

  isRecording = false;
  stream: MediaStream;
  recorder: StereoAudioRecorder;
  audioCreated = new Subject<any>();
  audioFile: AudioFile;

  private record() {
    this.recorder = new StereoAudioRecorder(this.stream, {
      type: 'audio',
      mimeType: 'audio/wav',
      desiredSampRate: 16000, // accepted sample rate by Azure
      timeSlice: 1000,
      numberOfAudioChannels: 1
    });
    this.recorder.record();
  }

  startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(s => {
        this.stream = s;
        this.record();
      }).catch(error => {
        console.log("Failed to record")
      });
  }

  stopRecording() {
    if (this.recorder) {
      this.recorder.stop((blob) => {
        const mp3Name = encodeURIComponent('audio_' + new Date().getTime() + '.mp3');
        this.stopMedia();
        this.audioFile = { blob: blob, title: mp3Name };
        this.audioCreated.next({ blob: blob, title: mp3Name });
      });
    }
  }

  stopMedia() {
    this.stream.getAudioTracks().forEach(track => track.stop());
    this.stream = null;
  }
}
