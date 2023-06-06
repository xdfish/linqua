import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RecordSolutionComponent } from './record-solution.component';

describe('RecordSolutionComponent', () => {
  let component: RecordSolutionComponent;
  let fixture: ComponentFixture<RecordSolutionComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [RecordSolutionComponent]
    });
    fixture = TestBed.createComponent(RecordSolutionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
