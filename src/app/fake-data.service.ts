import { Injectable } from '@angular/core';
import { BaseStatus, ILanguageTask, ITaskData, TaskDataDescribeItem, TaskDataRiddle, TaskPackage, TaskType } from './models';
import { faker } from '@faker-js/faker';

@Injectable({
  providedIn: 'root'
})
export class FakeDataService {

  constructor() { }

  dummyQuizPackage: TaskPackage;

  question1(index: number) {
    const taskData: TaskDataRiddle = {
      taskId: faker.string.uuid(),
      taskStatus: BaseStatus.open,
      title: "Greeting 1",
      description: "You have 2 seconds to read the keywords",
      question: "How to greet another person in the morning?",
      scoreKeywords: ["Hi", "Hello", "Good", "Morning"],
      words: ["Greet", "Morning"],
    }
    const task: ILanguageTask = {
      category: "grammar",
      description: "Create sentence from the keywords",
      title: "Grammar Task " + index,
      type: TaskType.riddle,
      taskData
    }
    return task;
  }

  question2(index: number) {
    const taskData: TaskDataDescribeItem = {
      taskId: faker.string.uuid(),
      taskStatus: BaseStatus.open,
      title: "Describe 1",
      description: "Please describe the shown item",
      scoreKeywords: ["Chair", "Red"],
      itemUrl: "/assets/red_chair.webp"
    }
    const task: ILanguageTask = {
      category: "grammar",
      description: "What is this thing?",
      title: "Describe Task " + index,
      type: TaskType.describe,
      taskData
    }
    return task;
  }

  generateQuizPackage() {
    const tasks: ILanguageTask[] = [];
    tasks.push(this.question1(1));
    tasks.push(this.question2(2));

    const dummyPackage: TaskPackage = {
      packageStatus: BaseStatus.open,
      tasks
    }

    this.dummyQuizPackage = dummyPackage;
    return dummyPackage;
  }
}
