import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BaseQuizTaskComponent } from './base-quiz-task.component';

describe('BaseQuizTaskComponent', () => {
  let component: BaseQuizTaskComponent;
  let fixture: ComponentFixture<BaseQuizTaskComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [BaseQuizTaskComponent]
    });
    fixture = TestBed.createComponent(BaseQuizTaskComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
