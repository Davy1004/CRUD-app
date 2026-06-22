import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Task {
  id?: number;
  title: string;
  completed?: boolean;
  project_id: number;
  created_at?: string;
}

const API = 'https://crud-app-narb.onrender.com/api/tasks';
const OPTS = { withCredentials: true };

@Injectable({ providedIn: 'root' })
export class TaskService {
  constructor(private http: HttpClient) {}

  // status: 'all' | 'completed' | 'pending'
  getTasks(status: string = 'all'): Observable<Task[]> {
    let url = API;
    if (status === 'completed' || status === 'pending') {
      url = `${API}?status=${status}`;
    }
    return this.http.get<Task[]>(url, OPTS);
  }

  createTask(t: Task): Observable<any> {
    return this.http.post<any>(API, t, OPTS);
  }

  updateTask(id: number, t: Partial<Task>): Observable<any> {
    return this.http.put<any>(`${API}/${id}`, t, OPTS);
  }

  deleteTask(id: number): Observable<any> {
    return this.http.delete<any>(`${API}/${id}`, OPTS);
  }
}
