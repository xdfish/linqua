import { Component, EventEmitter, Input, Output } from '@angular/core';
import { AudioFile } from 'src/app/audio-recording.service';
import { ILanguageTask, ITaskData } from 'src/app/models';

export interface ITaskDataProcessing {
  processTaskData();
}

@Component({
  selector: 'app-base-quiz-task',
  templateUrl: './base-quiz-task.component.html',
  styleUrls: ['./base-quiz-task.component.scss']
})
export class BaseQuizTaskComponent implements ITaskDataProcessing {

  userSolution: any;
  audioFile: AudioFile;

  @Output() taskIsStarting = new EventEmitter<void>()

  _task: ILanguageTask;
  public taskData: ITaskData;

  @Input() set task(data: ILanguageTask) {
    this._task = data;
    this.taskData = data?.taskData;
    this.processTaskData();
  }
  get task() {
    return this._task;
  }

  @Output() answerQuestion = new EventEmitter<any>();

  processTaskData() {
    console.log("this function should not be called");
  }

  taskStart() {
    this.audioFile = null;
    this.taskIsStarting.emit();
  }

  /**
   * This method will be overriden by sub components
   */

  recordSolution() {
    this.userSolution = null;
  }

  sendSolution() {

  }
}
