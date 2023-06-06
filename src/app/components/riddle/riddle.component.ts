import { Component, Input } from '@angular/core';
import { BaseQuizTaskComponent } from '../base-quiz-task/base-quiz-task.component';
import { ITaskData, TaskDataRiddle, TaskType } from 'src/app/models';
import { AudioFile } from 'src/app/audio-recording.service';

@Component({
  selector: 'app-riddle',
  templateUrl: './riddle.component.html',
  styleUrls: ['./riddle.component.scss']
})
export class RiddleComponent extends BaseQuizTaskComponent {
  randomWords: string[];
  question: string;

  userSolution: string;

  show = true;

  processTaskData() {
    if (this.task.type == TaskType.riddle) {
      const data = this.taskData as TaskDataRiddle;
      this.question = data.question;
      this.randomWords = data.words;
      setTimeout(() => {
        this.show = false;
      }, 6000);
    }
  }

  answerRecorded($event: AudioFile) {
    this.audioFile = $event;
  }

  sendAnswer() {
    this.answerQuestion.emit(this.audioFile);
  }
}
