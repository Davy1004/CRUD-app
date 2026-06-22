import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

const API = 'https://crud-app-narb.onrender.com/api/auth';
const OPTS = { withCredentials: true };

@Injectable({ providedIn: 'root' })
export class AuthService {
  // Simple reactive login flag the whole app can read.
  isLoggedIn = signal<boolean>(false);
  username = signal<string>('');

  constructor(private http: HttpClient) {}

  signup(username: string, password: string): Observable<any> {
    return this.http.post<any>(`${API}/signup`, { username, password }, OPTS).pipe(
      tap((res) => { this.isLoggedIn.set(true); this.username.set(res.username); })
    );
  }

  login(username: string, password: string): Observable<any> {
    return this.http.post<any>(`${API}/login`, { username, password }, OPTS).pipe(
      tap((res) => { this.isLoggedIn.set(true); this.username.set(res.username); })
    );
  }

  logout(): Observable<any> {
    return this.http.post<any>(`${API}/logout`, {}, OPTS).pipe(
      tap(() => { this.isLoggedIn.set(false); this.username.set(''); })
    );
  }

  // Called on app load to restore session state from the cookie.
  checkStatus(): Observable<any> {
    return this.http.get<any>(`${API}/me`, OPTS).pipe(
      tap((res) => {
        this.isLoggedIn.set(!!res.logged_in);
        this.username.set(res.username || '');
      })
    );
  }
}
