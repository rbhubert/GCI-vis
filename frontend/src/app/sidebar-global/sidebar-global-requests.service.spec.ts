import { TestBed } from '@angular/core/testing';

import { SidebarGlobalRequestsService } from './sidebar-global-requests.service';

describe('SidebarGlobalRequestsService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: SidebarGlobalRequestsService = TestBed.get(SidebarGlobalRequestsService);
    expect(service).toBeTruthy();
  });
});
