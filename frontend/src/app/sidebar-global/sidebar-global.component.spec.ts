import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SidebarGlobalComponent } from './sidebar-global.component';

describe('SidebarGlobalComponent', () => {
  let component: SidebarGlobalComponent;
  let fixture: ComponentFixture<SidebarGlobalComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SidebarGlobalComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SidebarGlobalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
