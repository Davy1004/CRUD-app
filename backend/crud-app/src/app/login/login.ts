import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.html'
})
export class LoginComponent {
  mode: 'login' | 'signup' = 'login';
  username = '';
  password = '';
  error = '';
  loading = false;

  constructor(private auth: AuthService, private router: Router) {}

  toggle() {
    this.mode = this.mode === 'login' ? 'signup' : 'login';
    this.error = '';
  }

  submit() {
    this.error = '';
    if (!this.username.trim() || !this.password) {
      this.error = 'Username and password are required.';
      return;
    }
    this.loading = true;
    const call = this.mode === 'login'
      ? this.auth.login(this.username.trim(), this.password)
      : this.auth.signup(this.username.trim(), this.password);

    call.subscribe({
      next: () => { this.loading = false; this.router.navigate(['/dashboard']); },
      error: (e) => {
        this.loading = false;
        this.error = e?.error?.error || 'Something went wrong. Try again.';
      }
    });
  }
}
