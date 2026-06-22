import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, Router } from '@angular/router';
import { AuthService } from './services/auth.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet],
  templateUrl: './app.html'
})
export class App implements OnInit {
  constructor(public auth: AuthService, private router: Router) {}

  ngOnInit() {
    // Restore login state from the session cookie on page load.
    this.auth.checkStatus().subscribe({
      next: () => { if (this.auth.isLoggedIn()) this.router.navigate(['/dashboard']); }
    });
  }

  logout() {
    this.auth.logout().subscribe({ next: () => this.router.navigate(['/login']) });
  }
}
