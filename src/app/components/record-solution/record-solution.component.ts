import { Component, EventEmitter, OnDestroy, Output } from '@angular/core';
import { AudioFile, AudioRecordingService } from 'src/app/audio-recording.service';
import { Subscription } from "rxjs"
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-record-solution',
  templateUrl: './record-solution.component.html',
  styleUrls: ['./record-solution.component.scss']
})
export class RecordSolutionComponent implements OnDestroy {

  audioFile: AudioFile;
  subscription: Subscription;
  recording: boolean;

  audioBlobUrl: SafeUrl;

  @Output() recordDone = new EventEmitter<AudioFile>()
  @Output() recordStarted = new EventEmitter<void>();

  constructor(private recordService: AudioRecordingService, private sanitizer: DomSanitizer) {
    this.subscription = this.recordService.audioCreated.subscribe(audioFile => {
      this.audioFile = audioFile;
      this.audioBlobUrl = this.sanitizer.bypassSecurityTrustUrl(URL.createObjectURL(audioFile.blob));
      this.recordDone.emit(this.recordService.audioFile);
    })
  }

  ngOnDestroy(): void {
    this.subscription.unsubscribe();
  }

  startRecording() {
    this.recording = true;
    this.audioBlobUrl = null;
    this.audioFile = null;
    this.recordService.startRecording();
    this.recordStarted.emit();
  }
  stopRecording() {
    this.recording = false;
    this.recordService.stopRecording();
  }
  playRecording() { }
}
