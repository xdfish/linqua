import { Component } from '@angular/core';
import { BaseQuizTaskComponent } from '../base-quiz-task/base-quiz-task.component';
import { AudioFile } from 'src/app/audio-recording.service';
import { TaskDataDescribeItem, TaskType } from 'src/app/models';

@Component({
  selector: 'app-describe-item',
  templateUrl: './describe-item.component.html',
  styleUrls: ['./describe-item.component.scss']
})
export class DescribeItemComponent extends BaseQuizTaskComponent {

  itemUrl: string;

  processTaskData() {
    if (this.task.type == TaskType.describe) {
      this.itemUrl = (this.taskData as TaskDataDescribeItem).itemUrl;
    }

  }
  answerRecorded($event: AudioFile) {
    this.audioFile = $event;
  }

  sendAnswer() {
    this.answerQuestion.emit(this.audioFile);
  }
}
