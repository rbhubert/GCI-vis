import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AddVisualizationComponent } from './add-visualization.component';

describe('AddVisualizationComponent', () => {
  let component: AddVisualizationComponent;
  let fixture: ComponentFixture<AddVisualizationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AddVisualizationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AddVisualizationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
