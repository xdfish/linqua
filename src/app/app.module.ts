import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { RiddleComponent } from './components/riddle/riddle.component';
import { DescribeItemComponent } from './components/describe-item/describe-item.component';
import { CompletionComponent } from './components/completion/completion.component';
import { BaseQuizTaskComponent } from './components/base-quiz-task/base-quiz-task.component';
import { FormsModule } from '@angular/forms';
import { RecordSolutionComponent } from './components/record-solution/record-solution.component';

import { HttpClientModule } from "@angular/common/http"

@NgModule({
  declarations: [
    AppComponent,
    RiddleComponent,
    DescribeItemComponent,
    CompletionComponent,
    BaseQuizTaskComponent,
    RecordSolutionComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
