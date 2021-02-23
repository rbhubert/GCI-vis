import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AccountFollowedManagerComponent } from './account-followed-manager.component';

describe('AccountFollowedManagerComponent', () => {
  let component: AccountFollowedManagerComponent;
  let fixture: ComponentFixture<AccountFollowedManagerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AccountFollowedManagerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AccountFollowedManagerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
