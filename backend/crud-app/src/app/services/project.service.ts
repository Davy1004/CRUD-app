import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Project {
  id?: number;
  name: string;
  description?: string;
  created_at?: string;
  task_count?: number;
}

const API = 'https://crud-app-narb.onrender.com/api/projects';
const OPTS = { withCredentials: true };

@Injectable({ providedIn: 'root' })
export class ProjectService {
  constructor(private http: HttpClient) {}

  getProjects(): Observable<Project[]> {
    return this.http.get<Project[]>(API, OPTS);
  }

  createProject(p: Project): Observable<any> {
    return this.http.post<any>(API, p, OPTS);
  }

  updateProject(id: number, p: Project): Observable<any> {
    return this.http.put<any>(`${API}/${id}`, p, OPTS);
  }

  deleteProject(id: number): Observable<any> {
    return this.http.delete<any>(`${API}/${id}`, OPTS);
  }
}
