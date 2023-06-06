import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CompletionComponent } from './completion.component';

describe('CompletionComponent', () => {
  let component: CompletionComponent;
  let fixture: ComponentFixture<CompletionComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CompletionComponent]
    });
    fixture = TestBed.createComponent(CompletionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
