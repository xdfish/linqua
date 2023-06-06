export class ITaskProp {
    [key: string]: any;
}

export enum BaseStatus {
    open = "open",
    done = "done",
    success = "success",
    fail = "fail"
}

export enum TaskType {
    riddle = "riddle",
    completion = "completion",
    describe = "describe"
}

export interface ILanguageTask {
    category: string;
    description: string;
    title: string;
    type: TaskType;
    taskData: ITaskData;
}

export class ITaskData {
    taskId: string;
    taskStatus: BaseStatus;
    title: string;
    author?: string;
    complexity?: number;
    description?: string;
    hints?: string[];
    score?: number;
    solution?: string;
    createdAt?: Date;
    updatedAt?: Date;
    scoreKeywords: string[];
}

export class TaskDataRiddle extends ITaskData {
    words: string[];
    question: string;
}

export class TaskDataCompletionExercise extends ITaskData {
    sentence: string;
}

export class TaskDataDescribeItem extends ITaskData {
    itemDescription?: string;
    itemUrl: string;
}

export class LanguageTask implements ILanguageTask {
    constructor(
        public category: string,
        public description: string,
        public title: string,
        public type: TaskType,
        public taskData: ITaskData) { }
}

export class TaskPackage {
    packageStatus: BaseStatus;
    tasks: ILanguageTask[];
}

export class UserProfile {
    score: number;
    packages: TaskPackage[];
}

export class User {
    name: string;
    password: string;
    profile: UserProfile;
    userName: string;
}

export class TaskAnswer {
    correct_sentence: string;
    score: number;
    text: string;
}