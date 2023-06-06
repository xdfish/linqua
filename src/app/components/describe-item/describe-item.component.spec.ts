import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DescribeItemComponent } from './describe-item.component';

describe('DescribeItemComponent', () => {
  let component: DescribeItemComponent;
  let fixture: ComponentFixture<DescribeItemComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DescribeItemComponent]
    });
    fixture = TestBed.createComponent(DescribeItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
