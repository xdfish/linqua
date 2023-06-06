import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { TaskAnswer, TaskPackage, TaskType } from './models';
import { FakeDataService } from './fake-data.service';
import { AudioFile } from './audio-recording.service';
import { ILanguageTask } from './models';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'linqua';

  dummyQuizPackage: TaskPackage;
  TaskType = TaskType;

  taskAnswer: TaskAnswer;

  currentTaskIndex = 0;
  get currentTask() {
    return this.dummyQuizPackage?.tasks[this.currentTaskIndex % this.dummyQuizPackage.tasks.length];
  }

  previous() {
    this.taskAnswer = null;
    this.currentTaskIndex--;
  }

  next() {
    this.taskAnswer = null;
    this.currentTaskIndex++;
  }

  constructor(private http: HttpClient, private fakeDataService: FakeDataService) {
    this.dummyQuizPackage = this.fakeDataService.generateQuizPackage();
  }

  async quizAnswered($event: AudioFile, task: ILanguageTask) {
    const keywords = task.taskData.scoreKeywords;
    const formData = new FormData();
    formData.append("audio", $event.blob, "myVoice123.wav")
    formData.append("keywords", keywords.join(","));
    const result: any = await this.http.post("http://localhost:3000/solve-quiz", formData).toPromise();
    this.taskAnswer = result;
    console.log(result)
  }
}
